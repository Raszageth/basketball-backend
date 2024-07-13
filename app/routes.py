from datetime import datetime, timedelta, timezone
from flask import current_app as app, make_response
from flask import request, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.db_models import Round, User, Team, Player, UserActivity
from database.db import db


@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get("username") or not auth.get("password"):
        return abort(401, description="Missing username or password")
    user = User.query.filter_by(username=auth.get("username")).first()

    if not user or not user.check_password(auth.get("password")):  
        return abort(401, description="Invalid credentials")

    additional_claims = {
        'username': user.username,
        'role': user.role,
        'player_id': user.player_id if user.player_id else None,
        'coach_id': user.coach_id if user.coach_id else None,
        'team_id': user.team_id if user.team_id else None,
    }
    token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(minutes=30),
        additional_claims=additional_claims
    )

    login_activity = UserActivity(user_id=user.id, login_time=datetime.now(timezone.utc))
    db.session.add(login_activity)
    db.session.commit()

    response = make_response({'token': token}, 201)
    return response

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    last_activity = UserActivity.query.filter_by(
        user_id=user_id).order_by(UserActivity.login_time.desc()).first()
    if last_activity and not last_activity.logout_time:
        last_activity.logout_time = datetime.now(timezone.utc)
        db.session.commit()

    response = make_response({"msg": "Logout successful"}, 200)
    return response

@app.route('/site_statistics', methods=['GET'])
@jwt_required()
def site_statistics():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != 'admin':
        abort(403, description="Access denied")

    users = User.query.all()
    statistics = []
    for user in users:
        login_count = UserActivity.query.filter_by(user_id=user.id).count()
        total_time = sum((activity.logout_time - activity.login_time).total_seconds()
                         for activity in user.activities if activity.logout_time)
        is_online = UserActivity.query.filter_by(user_id=user.id).order_by(UserActivity.login_time.desc()).first()
        is_online = is_online and not is_online.logout_time
        statistics.append({
            'username': user.username,
            'login_count': login_count,
            'total_time': total_time,
            'is_online': is_online
        })
    
    response = make_response(jsonify(statistics), 201)
    return response

@app.route('/team/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team_details(team_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        abort(404, description="User not found")

    claims = get_jwt()
    user_role = claims.get('role')
    user_team_id = claims.get('team_id')

    if not (user_role  == 'admin' or (user_role  == 'coach' and user_team_id == team_id)):
        abort(403, description="Access denied")

    team = Team.query.get(team_id)
    if not team:
        abort(404, description="Team not found")

    players = [{
        'id': player.id,
        'name': player.name,
        'games_played': player.games_played,
        'total_score': player.total_score
    } for player in team.players]
    response = make_response(jsonify({
        'team_name': team.name,
        'coach': team.coach.name,
        'players': players
    }), 201)
    return response

@app.route('/rounds', methods=['GET'])
@jwt_required()
def get_rounds():
    rounds = Round.query.order_by(Round.round_number).all()
    
    rounds_data = []
    for round in rounds:
        round_data = {
            'round_number': round.round_number,
            'matches': []
        }
        for game in round.games:
            team1 = Team.query.get(game.team1_id)
            team2 = Team.query.get(game.team2_id)
            match_data = {
                'team1': {
                    'name': team1.name,
                    'score': game.score_team1,
                    'id': game.team1_id
                },
                'team2': {
                    'name': team2.name,
                    'score': game.score_team2,
                    'id': game.team2_id
                },
            }
            round_data['matches'].append(match_data)
            if game.winner_id:
                final_winner = Team.query.get(game.winner_id)
        
        rounds_data.append(round_data)
        
    # add the winner in another round so we can display it nicely
    if final_winner:
        winner_round = {
            'round_number': rounds[-1].round_number + 1,
            'matches': [
                {
                    'team1': {
                        'name': final_winner.name,
                        'score': None,
                        'id': final_winner.id
                    },
                    'team2': None,
                }
            ]
        }
        rounds_data.append(winner_round)
    response = make_response(jsonify(rounds_data), 201)
    return response

@app.route('/player/<int:player_id>', methods=['GET'])
@jwt_required()
def get_player_details(player_id):
    player = Player.query.get(player_id)
    if not player:
        return abort(404, description="Player not found")
    
    player_data = {
        'id': player.id,
        'name': player.name,
        'games_played': player.games_played,
        'total_score': player.total_score,
        'height': player.height,
        'team_id': player.team_id,
    }
    response = make_response(jsonify(player_data), 201)
    return response
