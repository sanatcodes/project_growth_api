
# 🌐 Project Growth API
This API allows you to send and receive data to and from MongoDB. The API is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python.

## 🚀 Getting Started
To get started with this API, you'll need to install Python and the required packages.

## 🛠️ Installation
Clone the repository: git clone https://github.com/sant_codes/mongodb-api.git
Install the required packages: pip install -r requirements.txt
Run the application: uvicorn main:app --reload

## 📚 API Endpoints
GET /category
Returns a list of all categories in the database.

POST /category
Creates a new category in the database. The request body must contain a JSON object with the following properties: trending_date, category_id, views, likes, comment_count, and videos.

GET /category/{trending_date}
Returns the category with the specified trending_date. If the category does not exist, a 404 error is returned.

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for more information.
