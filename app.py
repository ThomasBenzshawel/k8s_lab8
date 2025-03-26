from flask import Flask, request, jsonify
from service import ToDoService
from models import Schema
from service import CategoryService

import json

app = Flask(__name__)

Schema()


@app.after_request
def add_headers(response):
   response.headers['Access-Control-Allow-Origin'] = "*"
   response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
   response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
   return response

@app.route("/")
def hello():
   return "Hello World!"


@app.route("/<name>")
def hello_name(name):
   return "Hello " + name


@app.route("/todo", methods=["GET"])
def list_todo():
   return jsonify(ToDoService().list())


@app.route("/todo", methods=["POST"])
def create_todo():
   return jsonify(ToDoService().create(request.get_json()))


@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
   return jsonify(ToDoService().update(item_id, request.get_json()))

@app.route("/todo/<item_id>", methods=["GET"])
def get_item(item_id):
   return jsonify(ToDoService().get_by_id(item_id))

@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
   return jsonify(ToDoService().delete(item_id))

# Category-related endpoints
@app.route("/categories", methods=["GET"])
def list_categories():
    return jsonify(CategoryService().list_all())

@app.route("/categories", methods=["POST"])
def create_category():
    return jsonify(CategoryService().create(request.get_json()))

@app.route("/categories/<category_id>", methods=["GET"])
def get_category(category_id):
    return jsonify(CategoryService().get_by_id(category_id))

@app.route("/categories/<category_id>", methods=["PUT"])
def update_category(category_id):
    return jsonify(CategoryService().update(category_id, request.get_json()))

@app.route("/categories/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    return jsonify(CategoryService().delete(category_id))

@app.route("/categories/<category_id>/todos", methods=["GET"])
def get_todos_by_category(category_id):
    return jsonify(CategoryService().get_todos_by_category(category_id))

@app.route("/todo/<todo_id>/categories", methods=["GET"])
def get_categories_for_todo(todo_id):
    return jsonify(CategoryService().get_categories_for_todo(todo_id))

@app.route("/todo/<todo_id>/categories", methods=["POST"])
def assign_category_to_todo(todo_id):
    category_id = request.get_json().get("category_id")
    if not category_id:
        return jsonify({"error": "category_id is required"}), 400
    return jsonify(CategoryService().assign_to_todo(todo_id, category_id))

@app.route("/todo/<todo_id>/categories/<category_id>", methods=["DELETE"])
def remove_category_from_todo(todo_id, category_id):
    return jsonify(CategoryService().remove_from_todo(todo_id, category_id))

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)
