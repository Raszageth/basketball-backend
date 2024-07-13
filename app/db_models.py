from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    player_id = db.Column(
        db.Integer, db.ForeignKey('player.id'),
        nullable=True
    )
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    coach = db.relationship('Coach', backref='team', lazy=True, uselist=False)
    players = db.relationship('Player', backref='team', lazy=True)


class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user = db.relationship('User', backref='player', uselist=False)
    games_played = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer)  # CM

    @property
    def average_score(self):
        if self.games_played > 0:
            return self.total_score / self.games_played
        return 0


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False, unique=True)
    games = db.relationship('Game', backref='round', lazy=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    players = db.relationship('GamePlayer', backref='game', lazy=True)
    score_team1 = db.Column(db.Integer, nullable=False)
    score_team2 = db.Column(db.Integer, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)


class GamePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(
        db.Integer, db.ForeignKey('player.id'),
        nullable=False
    )
    score = db.Column(db.Integer, nullable=False)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    logout_time = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', backref='activities')