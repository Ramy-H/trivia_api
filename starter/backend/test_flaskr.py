import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = 'postgres://postgres@localhost:5432/trivia'
        setup_db(self.app, self.database_path)

        self.new_question = {
            "answer": "Jamie",
            "category": 2,
            "difficulty": 3,
            "id": 18,
            "question": "What is Carragher's last name?"
        }

        self.data = {
            'previous_questions': [],
            'quiz_category': {
                'type': {
                    'id': 2,
                    'type': 'Art'
                },
                'id': 1
            }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET requests for all available categories.
    def test_get_all_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET requests for all available questions.
    def test_get_all_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE request for single question.
    def test_delete_a_question(self):
        res = self.client().delete('/api/questions/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # POST request for single question.
    def test_post_a_question(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # POST request for searching questions.
    def test_search_a_question(self):
        res = self.client().post('/api/questions/search',json={'searchTerm': 'who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET requests for all available questionss by category id.
    def test_get_all_categories_by_id(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle the quiz section test.
    def test_quizz(self):
        res = self.client().post('/api/quizzes', json=self.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
