# Flask CRUD API with Unit Tests

This is a simple Flask web application that provides a full RESTful API for managing a list of items. It includes unit tests and is ideal for learning how to structure a basic Flask project with CRUD operations and automated testing.

## Project Structure

flask_crud_app/
├── app/
│   └── routes.py         # Flask routes with full CRUD support
├── tests/
│   └── test_app.py       # Unit tests for the Flask app
├── run.py                # Entry point to run the Flask app
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

## Getting Started

Follow these steps to set up and run the application locally:

### 1. Clone the Repository

    git clone <repository_url>
    cd flask_crud_app

### 2. Set Up a Virtual Environment (Recommended)

    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Unix or MacOS:
    source venv/bin/activate

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Run the Flask Application

    python run.py

The app will run at [http://localhost:5000](http://localhost:5000).

### 5. Run the Unit Tests

    python -m unittest discover tests

This will discover and run all unit tests in the `tests/` directory.

---

## API Endpoints

| Method | Endpoint         | Description                      |
|--------|------------------|---------------------------------|
| GET    | `/`              | Returns a greeting message       |
| GET    | `/items`         | Retrieves all items              |
| GET    | `/items/<id>`    | Retrieves a specific item by ID  |
| POST   | `/items`         | Adds a new item (expects JSON)   |
| PUT    | `/items/<id>`    | Updates an existing item         |
| DELETE | `/items/<id>`    | Deletes an item by ID            |

Example `POST /items` JSON body:

    {
      "name": "Item 1"
    }

---

## Testing

Unit tests are located in `tests/test_app.py`. They cover:

- Greeting route
- Item addition
- Item retrieval (existing and non-existing)
- Item update
- Item deletion

Run tests using:

    python -m unittest discover tests

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Contribute

Feel free to fork this repository and submit pull requests. Bug fixes, suggestions, and improvements are welcome!

---

## Author

- Patricia Marie (modified from original version by Pan Luo)

---

## Acknowledgments

- Based on an educational Flask sample project.
- Inspired by the Flask community and best practices.

---

Happy coding! 🎉
