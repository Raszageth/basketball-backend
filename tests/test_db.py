import unittest
from flask import Flask
from app.db_models import Player, Game, Coach, User
from app.config import Config
from database.db import db


class DatabasePopulationTest(unittest.TestCase):
    def setUp(self):
        """initialize the test app"""
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)

    def test_players_created(self):
        """test that players are created and have valid heights"""
        players = Player.query.all()
        self.assertTrue(len(players) > 0)
        for player in players:
            self.assertTrue(175 <= player.height <= 225)

    def test_teams_and_coaches_linked(self):
        """test that teams are linked to coaches correctly"""
        coaches = Coach.query.all()
        for coach in coaches:
            self.assertIsNotNone(coach.team_id)

    def test_games_and_scores(self):
        """test that games have valid scores and a winners"""
        games = Game.query.all()
        for game in games:
            self.assertTrue(game.score_team1 >= 0 and game.score_team2 >= 0)
            self.assertIsNotNone(game.winner_id)

    def test_users(self):
        """test that users are created and admin exist"""
        users = User.query.all()
        self.assertTrue(len(users) > 0)
        admin_exists = User.query.filter_by(role='admin').first()
        self.assertIsNotNone(admin_exists)


if __name__ == '__main__':
    unittest.main()
