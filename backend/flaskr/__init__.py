import os
from zoneinfo import available_timezones
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
    page = request.args.get('page',1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/api/categories',  methods=["GET"])
    def retrive_all_categories():
        categories = Category.query.order_by(Category.type).all()
        if not categories:
            abort(404)
        else:    
            return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        }) 

    
    @app.route('/api/questions',  methods=["GET"])
    def retrive_all_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request,questions)
        categories = Category.query.order_by(Category.type).all()

        if not questions:
            abort(404)
        else:    
            return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions':len(questions),
            'categories': {category.id: category.type for category in categories},
            'current category': None
        })   
         
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404)
        else:   
                question.delete()
                return jsonify({
                    'success': True,
                    'deleted': question_id
            }) 
           

    @app.route('/api/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if not new_question or not new_answer or not new_category or not new_difficulty:
            abort(400)

        question = Question(new_question,new_answer,new_category,new_difficulty)

        try:
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            })

        except:
            abort(422)    

    @app.route('/api/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            matched_questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            questions = paginate_questions(request, matched_questions)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(matched_questions),
                'current_category': None
            })
        abort(404)    


    @app.route('/api/category/<int:id>/questions', methods=['GET'])   
    def search_questions_categorically(id):
            category = Category.query.filter_by(id=id).one_or_none()
            if category is None:
                abort(404)
            else:
                questions = Question.query.filter_by(category=category.id).all()
                questions = paginate_questions(request, questions)

                return jsonify({
                'success': True,
                'questions':questions,
                'total_questions':len(questions),
                'category': category.type,
            })



    @app.route('/api/quizzes', methods=['POST'])
    def play_game():
            body = request.get_json()
            category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)


            if category is None:
                abort(400)

            category_id = category['id']
            all_questions = Question.query.all()
            category_questions = Question.query.filter(Question.category == category_id ).all()

            if category_id == 0:
                questions =  [question.format() for question in all_questions]
            else:
                questions = [question.format() for question in category_questions]  

            while True:
                    next_pick = random.choice(questions)
                    if next_pick['id'] not in previous_questions:
                        break
                    else:
                        return jsonify({
                            "question":None
        })
                
            return jsonify({
                    'question': next_pick,
                    'success': True,
                })


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app

