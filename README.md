
## Project Goal

The goal of this project is to learn and demonstrate:

- How to use OOP concepts in Python
- How request validation and response formatting work in FastAPI
- How to write basic API tests

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- HTTPX

---

## OOP Concepts Demonstrated

This project demonstrates the following Object-Oriented Programming concepts:

| OOP Concept | Where It Is Used |
|---|---|
| Class | `Product`, `ProductService`, `ProductRepository`, `InMemoryProductRepository` |
| Object | Product objects are created when a new product is added |
| Constructor | `__init__` method in service and repository classes |
| Encapsulation | Product price and stock are controlled using property methods |
| Abstraction | `ProductRepository` abstract class defines required repository behavior |
| Inheritance | `InMemoryProductRepository` inherits from `ProductRepository` |
| Polymorphism | Service depends on repository abstraction, not a fixed implementation |
| Composition | `ProductService` uses a repository object |
| Magic Method | `__str__` method in the `Product` class |

---

## Project Structure

```text
oop_demo/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       └── product_routes.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   └── product.py
│   ├── repositories/
│   │   ├── base.py
│   │   └── product_repository.py
│   ├── schemas/
│   │   └── product_schema.py
│   └── services/
│       └── product_service.py
├── tests/
│   └── test_products.py
├── requirements.txt
├── .gitignore
└── README.md

Setup Instructions
1. Clone the repository
git clone https://github.com/your-username/OOP-demo.git
2. Go inside the project folder
cd OOP-demo
3. Create virtual environment
python -m venv .venv
4. Activate virtual environment

For macOS/Linux:
source .venv/bin/activate

For Windows:
.venv\Scripts\activate

5. Install dependencies
pip install -r requirements.txt
6. Run the FastAPI server
uvicorn app.main:app --reload
7. Open API documentation

Open this URL in your browser:
http://127.0.0.1:8000/docs