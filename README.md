<b><h2>Trivia API</h2></b>

Trivia API is a RESTFUL API application that allowing the users to:<br>
<li>
  <ol>1. Display questions.</ol>
  <ol>2. Delete questions.</ol>
  <ol>3. Add questions and require that they include question and answer text.</ol>
  <ol>4. Search for questions based on a text query string.</ol>
  <ol>5. Play the quiz game, randomizing either all questions or within a specific category.</ol>
</li>
  
Pre-requisites and Local Development:<br>
To use this application you need python3, pip, Virtualenv, and node installed on your local machine.

<b>Backend</b><br>
Dependances:<br>
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running.

This will install all of the required packages we selected within the requirements.txt file.
>pip install -r requirements.txt

Database Setup
Create trivia database from Postgres and restore a database using the trivia.psql file provided. From the backend folder in terminal run: <b>psql trivia < trivia</b>

Running the server: From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:<br>
>set FLASK_APP=flaskr<br>
>set FLASK_ENV=development<br>
>flask run<br>

<b>Frontend:</b>
You should download and install Node (the download includes NPM) from https://nodejs.com/en/download.

Installing project dependencies:<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:<br>>npm install

Running Your Frontend in Dev Mode: The frontend app was built using create-react-app. In order to run the app in development mode use npm start, You can change the script in the <b>package.json</b> file.

Then open http://localhost:3000 to view it in the browser, The page will reload if you make edits.<br>
>npm start

<b>Testing</b>
To run the tests, run:<br>
>dropdb trivia_test<br>
>createdb trivia_test<br>
>psql trivia_test < trivia.psql<br>
>python test_flaskr.py

<b>API Reference</b>
Base URL: At the present this app can only be run locally and is not hosted. the backend app is hosted at http://127.0.0.1:5000/

Authentication: This version of the application doesn't require authentication or API keys.

Error Handling: Errors are returned as JSON objects in the following format.
```javascript
{
    'success': False,
    'error': 404,
    'message': "Not Found"
}
```
The API will return four error types when requests fail:<br>
  1. 404: Resource not found
  2. 400: Request failed
  3. 422: Request cannot be processed
  
<b>Endpoints:</b>
<br>GET /categories: Return all categories<br>
Sample: bash curl http://127.0.0.1:5000/categories
```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
GET /categories/int:category_id/questions: Get all questions in a specific category and success value<br>
Sample: curl http://127.0.0.1:5000/categories/1/questions
```javascript
{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true
}
```
GET /questions: Return a list of questions objecs, categories, current_category, success value and total number of questions
Result are paginated in group of 10 include a request argument to choose page number, starting from 1
Sample: bash curl http://127.0.0.1:5000/questions
```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    3, 
    4, 
    5, 
    6
  ], 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```
POST /questions: Creates a new question using question, answer, category and difficulty
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{'question': "Who is the best striker in the world?", 'answer': "Robert Lewandowski", 'difficulty': "1", 'category': 6}'
```javascript
{
  "success": true
}
```
DELETE /questions/int:question_id: Deletes the question of the given ID if it exists, Returns success value
Sample curl http://127.0.0.1:5000/questions/31 -X DELETE
```javascript
{
  "success": true
}
```
POST /quizzes: Get random question to play quiz. the question can be in a specific category
Sample:
curl -X POST \
  http://127.0.0.1:5000/quizzes \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{"previous_questions": [],
"quiz_category": {"type": "Science", "id": 1}
}'
```javascript
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```
