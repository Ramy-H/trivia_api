import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category
import sys

QUESTIONS_PER_PAGE = 10

def paginate(request, data):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  
  data = data[start:end]
  return data

def formatt(data):
  ### format the data
  data = [datum.format() for datum in data]

  return data

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # Set up cors and allow '*' for origins
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET, PUT, POST, DELETE, OPTIONS')
    return response

  # GET requests for all available categories.
  @app.route('/api/categories')
  @cross_origin()
  def get_all_categories():
    categories = Category.query.all()
    if len(categories) == 0:
      abort(404)
    try:
      categories = paginate(request, categories)
      categories = formatt(categories)
      return jsonify({
        'success': True,
        'categories': categories
        }), 200
    except:
      abort(400)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/api/questions')
  @cross_origin()
  def get_all_questions():
    categories = Category.query.order_by(Category.id).all()
    questions = Question.query.all()

    if len(questions) == 0:
      abort(404)
    elif len(categories) == 0:
      abort(404)
    try:
      questions = formatt(questions)
      data = paginate(request, questions)
      
      if len(questions) < 1:
        abort(404)
      else:
        return jsonify({
          'count': len(questions),
          'questions': data,
          'categories': formatt(categories),
          'success': True
          }), 200
    except:
      abort(400)

  ### DELETE question using a question ID.

  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  @cross_origin()
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question is None:
      abort(404)
    try:
      question.delete()
      categories = Category.query.order_by(Category.id).all()
      questions = Question.query.all()
      questions = formatt(questions)
      questions = paginate(request, questions)
      return jsonify({
        'count': len(questions),
        'questions': questions,
        'categories': formatt(categories),
        'success': True
        })
    except:
      abort(400)


  ### POST a new question, which will require the question and answer text, category, and difficulty score.
  @app.route('/api/questions', methods=['POST'])
  @cross_origin()
  def post_question():
    error = False
    data = request.get_json()
    # set question variable equal to corresponding model class,
    # ready for adding to the session
    question = Question(
      question=data.get('question', None),
      answer=data.get('answer', None),
      difficulty=data.get('difficulty', None),
      category=data.get('category', None)
      )

    if not question.question:
      abort(404)
    try:
      db.session.add(question)
      db.session.commit()
    except:
      error = True
      print("Error:",sys.exc_info())
      abort(400)

    categories = Category.query.order_by(Category.id).all()
    questions = Question.query.all()
    questions = formatt(questions)
    questions = paginate(request, questions)
      
    return jsonify({
      'count': len(questions),
      'questions': questions,
      'categories': formatt(categories),
      'success': True
      }), 200


  ### Get questions based on a search term.
  @app.route('/api/questions/search', methods=['POST'])
  @cross_origin()
  def search_question():
    try:
      # get search term
      term = request.get_json().get('searchTerm', None)

      # query the database for like results and send the response
      questions = Question.query.filter(Question.question.like('%'+term+'%')).all()
      questions = formatt(questions)

      if(questions is None):
        abort(404)
      return jsonify({
        'total_questions': len(questions),
        'questions': questions,
        'success': True
        }), 200
    except:
      abort(400)
 
  ### get questions based on category.

  @app.route('/api/categories/<int:category_id>/questions')
  @cross_origin()
  def search_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    try:
      # query the database for like results and send the response
      questions = formatt(questions)
      questions = paginate(request, questions)
      
      if len(questions) == 0:
        abort(404)
        
      return jsonify({
        'total_questions': len(questions),
        'questions': questions,
        'success': True
        }), 200
    except:
      abort(400)


   
  ### Create a POST endpoint to get questions to play the quiz.
  @app.route('/api/quizzes', methods=['POST'])
  def random_questions():
    previous_questions = request.get_json().get('previous_questions')
    quiz_category = request.get_json().get('quiz_category')
    try:
      if(quiz_category['id'] == 0):
        questions_by_category = Question.query.all()
      else:
        questions_by_category = Question.query.filter_by(category=quiz_category['type']['id']).all()
      
      random_num = random.randint(0, len(questions_by_category)-1)
      question = questions_by_category[random_num]

      selected = False
      count = 0
      
      while selected is False:
        if(question.id in previous_questions):
          random_num = random.randint(0, len(questions_by_category)-1)
          question = questions_by_category[random_num]
        else:
          selected = True

      count += 1
      question = question.format()
      
      return jsonify({
        'success': True,
        'question': question
        }), 200
    except:
      abort(422)
  
  # Error handlers for all expected errors including 404 and 422.
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404
    
  @app.errorhandler(422)
  def not_processed(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Request cannot be processed"
      }), 404

  @app.errorhandler(400)
  def not_successful(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Request failed"
      }), 400
  
  return app