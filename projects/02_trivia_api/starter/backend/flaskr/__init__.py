import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def filter_question(min_id, max_id, all_questions):
    if max_id < min_id:
        max_id = min_id
    question_index = random.randint(min_id, max_id)
    next_question = None
    if all_questions is not None:
        next_question = list(
            filter(lambda q: q.id == question_index, all_questions))
    return next_question, question_index


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # @(DONE): Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={r"/(categories|questions)*": {'origins': '*'}})

    '''
  @(DONE): Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE')
        return response

    '''
  @(DONE): 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/')
    @app.route('/categories')
    def retrieve_categories(jsonResponse=True):
        categories = Category.query.order_by(Category.id).all()
        current_categories = [category.format() for category in categories]
        category_types = [category['type'] for category in current_categories]

        if len(current_categories) == 0:
            abort(404)
        # else:
        #   print(current_categories)

        if jsonResponse:
            return jsonify({
                'success': True,
                'categories': current_categories,
                'total_categories': len(current_categories)
            })
        else:
            return category_types

    '''
  @(DONE): 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions')
    def retrieve_all_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)
        # else:
        #   print(current_questions)

        category = current_questions[0]['category']
        categories = retrieve_categories(jsonResponse=False)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'current_category': category,
            'categories': categories
        })

    '''
  @(DONE): 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(422)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except:
            abort(422)

    '''
  @(DONE): 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    '''
  @(DONE): 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection.all())
                })

            else:  # create a new question
                question = Question(question=new_question, answer=new_answer,
                                    category=new_category, difficulty=new_difficulty)
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id
                })

        except:
            abort(422)  # unprocessable

    '''
  @(DONE): 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if category is not None:
            category = category.type
        else:
            abort(404)

        selection = Question.query.filter(
            Question.category == category_id).order_by(Question.id)
        current_questions = paginate_questions(request, selection)

        # if len(current_questions) == 0:
        #   abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'current_category': category
        })

    '''
  @(DONE): 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_next_quiz():
        category_id = -1
        previous_questions = []
        body = request.get_json()

        if body is not None:
            previous_questions = body.get('previous_questions', [])
            category_id = body.get('quiz_category', -1)

        if category_id != -1:
            all_questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()
        else:
            all_questions = Question.query.order_by(Question.id).all()

        questions_count = len(all_questions)
        if questions_count == 0:
            abort(404)

        no_question_left = False
        min_id = all_questions[0].id
        max_id = all_questions[questions_count - 1].id
        question_ids = [q.id for q in all_questions]

        if question_ids == sorted(previous_questions):
            no_question_left = True
        else:
            count = 1
            num_tries = questions_count * 5
            next_question, question_index = filter_question(
                min_id, max_id, all_questions)

            while ((len(next_question) == 0) or (question_index in previous_questions)):
                next_question, question_index = filter_question(
                    min_id, max_id, all_questions)
                count += 1
                if count > num_tries:
                    abort(422)

        if no_question_left:
            return jsonify({
                'success': True,
                'question': None
            })
        else:
            return jsonify({
                'success': True,
                'question': next_question[0].format()
            })

    '''
  @(DONE): 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(405)
    def unallowed_method(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "server error"
        }), 500

    return app
