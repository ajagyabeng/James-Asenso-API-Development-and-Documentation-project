import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flaskr import create_app
from models import setup_db, Question, Category

load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URL')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f"{DATABASE_URI}/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # create new question data
        self.new_question = {
            "question": "Who won the Balon dor award in the year 2018",
            "answer": "Luka Modric",
            "difficulty": 2,
            "category": 3
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertEqual(data['success'], False)

    # -------------DELETE QUESTION--------------
    def test_delete_questions(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 23).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 23)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    # -----ABOVE COMMENTED OUT ON PURPOSE----------

    def test_404_for_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertEqual(data['success'], False)

    # ------------ADD NEW QUESTION-------------
    def test_add_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_405_for_if_add_question_not_allowed(self):
        res = self.client().post('/questions/4', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # ----------SEARCH FOR QUESTION-------------
    def test_search_question_with_result(self):
        res = self.client().post('/questions', json={"searchTerm": "Invent"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertTrue(data['total_questions'])
    
    def test_search_question_without_result(self):
        res = self.client().post('/questions', json={"searchTerm": "asenso"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertTrue(data['total_questions'])

    # --------QUESTION BASED ON CATEGORY--------------
    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['currentCategory'], "History")
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions']) 

    def test_422_if_request_unprocessable(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertEqual(data['success'], False)

        
    # --------------GET QUIZ QUESTIONS-------------
    def test_get_quiz_question(self):
        trivia_request = {'quiz_category': {'id': '3'}, 'previous_questions':[]
        }
        res = self.client().post('/quizzes', json=trivia_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_500_if_request_parameter_not_present(self):
        trivia_request = {'quiz_category': {'id': '3'}}
        res = self.client().post('/quizzes', json=trivia_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['message'], 'Internal Server Error')
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()