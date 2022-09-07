import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    """paginates the shows the number of items to display at a time"""
    page = request.args.get('page', 1, type=int) 
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """Set up CORS"""
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response

    @app.route('/categories')
    def get_categories():
        """fetches all the categories available"""
        response = Category.query.all()
        categories = [category.format() for category in response]
        
        return jsonify({
            'success': True,
            'categories': categories, 
            'total_categories': len(Category.query.all())
        })

    @app.route('/questions')
    def get_paginated_questions():
        current_category = request.args.get('category', 1, type=int)
        response = Question.query.all()
        current_questions = paginate_questions(request, response)
        categories = [category.format() for category in Category.query.all()]

        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories,
            'current_category': current_category
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).first()
            if question is None:
                abort(404)
            question.delete()
            response = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, response)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(response)
            })
        except LookupError:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    # ----------ERROR HANDLERS-----------------

    @app.errorhandler(404)
    def not_found(error):
        """handles 404 errors"""
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """handles 422 errors"""
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
            }), 422

    return app

