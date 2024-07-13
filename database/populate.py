import random
from app.db_models import Team, Player, Coach, Round, Game, GamePlayer, User


# it takes around 10 seconds locally to populate the db
# due to password hashing, removןng the hashing
# will populate almost instantly
def populate_db_with_data(db):
    # generate league_admin user
    league_admin = User(username='admin', role='admin')
    league_admin.set_password('adminpassword')  # testers easy access
    db.session.add(league_admin)
    db.session.commit()

    # generate teams and choaches and user for coaches
    teams = []
    for i in range(16):
        team = Team(name=f'Team{i+1}')
        db.session.add(team)
        db.session.commit()  # commit to get team id

        coach = Coach(name=f'Coach {team.name}', team_id=team.id)
        db.session.add(coach)
        db.session.commit()  # commit to get coach id

        coach_user = User(
            username=f'coach{i+1}',
            role='coach',
            coach_id=coach.id,
            team_id=team.id
        )
        coach_user.set_password('password')  # testers easy access
        db.session.add(coach_user)
        db.session.commit()

        teams.append(team)

    # generate players and users for players
    for team in teams:
        for i in range(10):
            height = random.randint(175, 225)  # random height in CM
            player = Player(
                name=f'Player {i+1}_{team.name}',
                team_id=team.id,
                height=height
            )
            db.session.add(player)
            db.session.commit()  # commit to get player id

            player_user = User(
                username=f'player{i+1}_{team.name}',
                role='player',
                player_id=player.id,
                team_id=team.id
            )
            player_user.set_password('password')  # testers easy access
            db.session.add(player_user)
            db.session.commit()

    # generate rounds
    rounds = [Round(round_number=i) for i in range(1, 5)]
    db.session.bulk_save_objects(rounds)
    db.session.commit()

    # generate games
    current_teams = teams
    for round_number in range(1, 5):
        games = create_games_for_round(db, round_number, current_teams)
        for game in games:
            assign_player_scores(db, game)
        current_teams = get_winners(db, games)


def create_games_for_round(db, round_number, teams):
    round_obj = Round.query.filter_by(round_number=round_number).first()
    games = []
    for i in range(0, len(teams), 2):
        game = Game(
            round_id=round_obj.id,
            team1_id=teams[i].id,
            team2_id=teams[i+1].id,
            score_team1=0,
            score_team2=0,
            winner_id=None  # winner tbd after score assignments
        )
        db.session.add(game)
        games.append(game)
    db.session.commit()
    return games


def get_winners(db, games):
    winners = []
    for game in games:
        winner = db.session.get(Team, game.winner_id)
        winners.append(winner)
    return winners


def assign_player_scores(db, game):
    team1_players = Player.query.filter_by(team_id=game.team1_id).all()
    team2_players = Player.query.filter_by(team_id=game.team2_id).all()

    # assign scores to randomly selected players of each team
    # and calculate team scores
    game.score_team1 = distribute_scores(db, team1_players, game.id)
    game.score_team2 = distribute_scores(db, team2_players, game.id)

    game.winner_id = game.team1_id if game.score_team1 > game.score_team2 \
        else game.team2_id
    db.session.commit()


def distribute_scores(db, players, game_id):
    # select at least 5 players for each game
    selected_players = random.sample(
        players, k=random.randint(5, min(10, len(players)))
    )
    total_score = 0

    for player in selected_players:
        # each player scores between 2-20 points because they are not MJ
        score = random.randint(2, 20)
        total_score += score
        game_player = GamePlayer(
            game_id=game_id,
            player_id=player.id,
            score=score
        )
        player.games_played += 1
        player.total_score += score
        db.session.add(game_player)

    return total_score
