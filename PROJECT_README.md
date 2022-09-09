# API Reference

# Getting Started

- Base Url: At the moment the app is not hosted as a base url but runs locally. The backend is hosted at `http://127.0.0.1:5000/`.

- Authentication: This version of the application does not require authentication or API keys.

# Error Handling

Errors are returned as JSON objects in like below:

```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API returns the following errors when a request fails:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

# Endpoints

## GET /categories

- General:
  - Returns an object with a single key, categories, which contains an object of `id: category_string` key:value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

## GET /questions

- General:
  - Request Arguments: page number - integer
  - Fetches a paginated set of questions. Returns and object with 10 paginated questions, total questions, object including all categories, and current category string.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

```{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History",
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
      "question": "What movie earned Tom Hanks his third straight Oscar nomination,
in 1996?"
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
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "total_questions": 17
}
```

## GET /categories/{id}/questions

- General:
  - Fetches questions for a category specified by id request argument
  - Request Arguments: category id - integer
  - Returns as object with questions for the specified category, total questions and category string
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```{
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 17
}
```

## DELETE /questions/{id}

- General:
  - Deletes a specified question using it's id.
  - Request Arguments: question id - integer
  - Returns nothing
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`

## POST /questions

- General: - Sends a post request to add a new question
  - Request Body: {
    'question': 'Which football player has the most Balon dors',
    'answer': 'Lionel Messi',
    'difficulty': 3,
    'category': 6,
    }
  - Returns: Does not return any new data
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "Which football player has the most Balon dors", "answer": "Lionel Messi", "difficulty": 3, "category": 6}'`

## POST /questions

- General: Sends a post request to search for a specific question by a search term.
  - Request Body: {
    'searchTerm': 'Balon dor'
    }
  - Returns: returns any list of questions, number of total questions that matched the search term and the current category string
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "Balon dor"}'`

```{
  "currentCategory": [
    "Geography"
  ],
  "questions": [
    {
      "answer": "Luka Modric",
      "category": 3,
      "difficulty": 2,
      "id": 24,
      "question": "Who won the Balon dor award in the year 2018"
    }
  ],
  "success": true,
  "total_questions": 17
}
```

## POST /quizzes

- General:
  - Sends a post request to get the next question.
  - Request body sends a list of ids of previous questions and the quiz category: {
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
    }
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"previous_questions": [1, 4], "quiz_category": 3}'`
