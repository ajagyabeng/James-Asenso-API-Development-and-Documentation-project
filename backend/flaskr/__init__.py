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

def categories_dict():
    """querries databse and return category data as a dictionary"""
    categories = [category.format() for category in Category.query.all()]
    categories_dict = {category['id']: category['type'] for category in categories}
    return categories_dict

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
        categories = categories_dict()
        
        return jsonify({
            'success': True,
            'categories': categories, 
            'total_categories': len(Category.query.all())
        })

    @app.route('/questions')
    def get_paginated_questions():
        current_category = request.args.get('category', 1, type=int) # TODO: FIX THIS
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)
        categories = categories_dict()

        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories,
            'current_category': current_category
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """Deletes a question with a provided id. Returns a json object"""
        try:
            question = Question.query.filter(Question.id == question_id).first()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection)
            })
        except LookupError:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        """adds a new question to the database"""
        body = request.get_json()

        # get hold of values passed into the request individually
        new_question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)
        query = body.get("query", None)

        try:
            if query:
                selection = Question.query.filter(Question.question.ilike(f"%{query}%")).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })
            else:
                # create new question and insert it into database
                question = Question(
                    question=new_question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category
                )
                question.insert()

                # select and return questions
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                })
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id).all()
            if selection is None:
                abort(404)
            current_questions = paginate_questions(request, selection)

            categories = categories_dict()
            current_category = categories[category_id]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(Question.query.all()),
                'currentCategory': current_category
            })
        except:
            abort(422)

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

    # ----------ERROR HANDLERS-----------------

    @app.errorhandler(400)
    def invalid(error):
        """handles 400 errors"""
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        """handles 404 errors"""
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        """handles 405 errors"""
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        """handles 422 errors"""
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
            }), 422

    return app

