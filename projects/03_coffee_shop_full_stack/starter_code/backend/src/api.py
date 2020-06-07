import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@(DONE) uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@(DONE) implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def retrieve_drinks():
    all_drinks = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short() for drink in all_drinks]

    if len(drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@(DONE) implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_details(jwt):
    if jwt is not None:
        all_drinks = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in all_drinks]

        if len(drinks) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'drinks': drinks
        })

    else:
        abort(401)


'''
@(DONE) implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    if jwt is not None:
        body = request.get_json()

        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)  # recipe value must be a string

        try:
            new_drink = Drink(title=new_title, recipe=new_recipe)
            new_drink.insert()
            drink = [new_drink.long()]

            return jsonify({
                'success': True,
                'drinks': drink
            })

        except:
            abort(422)

    else:
        abort(401)


'''
@(DONE) implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    if jwt is not None:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)

        body = request.get_json()
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)  # recipe value must be a string

        if new_title is not None:
            drink.title = new_title
        if new_recipe is not None:
            drink.recipe = new_recipe

        try:
            drink.update()
            updated_drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink = [updated_drink.long()]

            return jsonify({
                'success': True,
                'drinks': drink
            })
        except:
            abort(422)

    else:
        abort(401)


'''
@(DONE) implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    if jwt is not None:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)

        try:
            drink.delete()

            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)

    else:
        abort(401)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@(DONE) implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@(DONE) implement error handler for 404
    error handler should conform to general task above 
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "resource not found"
    }), 404


'''
@(DONE) implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code
