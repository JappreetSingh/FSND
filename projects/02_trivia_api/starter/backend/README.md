# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT (DONE: Documentation)
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 
```

The API provides following Endpoints:
GET '/categories'
GET '/questions'
GET '/categories/<id>/questions'
POST '/questions'
DELETE '/questions/<id>'
POST '/quizzes'


GET '/categories'
- Fetches a list of categories
- Request Arguments: None
- Returns: 
    A list of categories, with each category a dictionary with two keys: id (with value as ID of the category) and type (with value as the corresponding string of the category)
- Example Response:
    [{'id': 1, 'type': 'Science'}, {'id': 2, 'type': 'Art'}, {'id': 3, 'type': 'Geography'}, {'id': 4, 'type': 'History'}, {'id': 5, 'type': 'Entertainment'}, {'id': 6, 'type': 'Sports'}]
- Error Response: 
    Returns 404 if no categories are found


GET '/questions'
- Fetches a list of questions across all categories
- Request Arguments: None
- Returns: A list of questions
- Example Response:
    [{'id': 2, 'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 'answer': 'Apollo 13', 'category': 5, 'difficulty': 4}, {'id': 4, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 'answer': 'Tom Cruise', 'category': 5, 'difficulty': 4}...... ]
- Error Response:
    Returns 404 if no questions are found


GET '/categories/<id>/questions'
- Fetches a list of questions for a particular category
- Request Arguments: 
    Query parameter "id" of type int denoting the category id
- Returns: A list of questions
- Example Response:
    [{'id': 2, 'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 'answer': 'Apollo 13', 'category': 5, 'difficulty': 4}, {'id': 4, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 'answer': 'Tom Cruise', 'category': 5, 'difficulty': 4}...... ]
- Error Response:
    Returns 404 if the category with that id is not found or no questions are found for the category specified


POST '/questions'
- Creates and posts a new question or searches for a question
- Request Arguments: 
    No query parameter; however a JSON body is needed.
- Request Body:
    Provide key 'searchTerm' in the JSON body to exercise the search function. 
    If you do not provide that key, a new question will be created based on the key-value pairs provided in the JSON body of the request.
- Example Request Body: 
    (For creation)
        {
            'question': 'Which character and movie did Heath Ledger get a posthumous oscar for?',
            'answer': 'Joker, The Dark Knight',
            'category': 5,
            'difficulty': 2
        }
    (For search)
        {
            'searchTerm': 'artist'
        }
- Returns: 
    (creation) The ID of the newly posted question
    (search) A list of questions having the search term in the question text
- Error Response:
    Returns 422 if unsuccessful


DELETE '/questions/<id>'
- Deletes a question with the provided ID
- Request Arguments: Query parameter "id" of type int denoting the question id
- Returns: 
    The ID of the deleted question
- Error Response:
    422 if the question id is not found


POST '/quizzes'
- Use this endpoint to play the quiz game, in order to retrieve a random question (within a given category, if provided,) that is not one of the previous questions already played
- Request Arguments: 
    No query parameter; however an optional JSON body may be provided.
- Request Body:
    A key 'previous_questions' with value as list of question IDs already played
    A key 'quiz_category' with value as the ID of the category being played
- Example Request Body:
    {
        'previous_questions': [20], 
        'quiz_category': 5
    }
- Returns: 
    An object representing a random question from the database of questions, that belongs to the given category (if provided) and is not one of the previous questions in the list (if provided)
- Example Response:
    { 'id': 2, 'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 'answer': 'Apollo 13', 'category': 5, 'difficulty': 4 }
- Error Response:
    Returns 404 or 422 if unsuccessful


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```