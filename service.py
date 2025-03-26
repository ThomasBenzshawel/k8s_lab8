from models import ToDoModel
from models import CategoryModel

class ToDoService:
   def __init__(self):
       self.model = ToDoModel()

   def create(self, params):
       return self.model.create(params)

   def update(self, item_id, params):
       return self.model.update(item_id, params)

   def delete(self, item_id):
       return self.model.delete(item_id)

   def list(self):
       response = self.model.list_items()
       return response
  
   def get_by_id(self, item_id):
       response = self.model.get_by_id(item_id)
       return response
   
class CategoryService:
    def __init__(self):
        self.model = CategoryModel()
    
    def create(self, params):
        name = params.get("name")
        color = params.get("color", "#000000")
        
        if not name:
            return {"error": "Name is required"}, 400
            
        return self.model.create(name, color)
    
    def get_by_id(self, category_id):
        category = self.model.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}, 404
        return category
    
    def list_all(self):
        return self.model.list_all()
    
    def update(self, category_id, params):
        if not self.model.get_by_id(category_id):
            return {"error": "Category not found"}, 404
        return self.model.update(category_id, params)
    
    def delete(self, category_id):
        if not self.model.get_by_id(category_id):
            return {"error": "Category not found"}, 404
        return self.model.delete(category_id)
    
    def assign_to_todo(self, todo_id, category_id):
        # You might want to check if todo exists here
        if not self.model.get_by_id(category_id):
            return {"error": "Category not found"}, 404
        return self.model.assign_to_todo(todo_id, category_id)
    
    def remove_from_todo(self, todo_id, category_id):
        # You might want to check if todo exists here
        if not self.model.get_by_id(category_id):
            return {"error": "Category not found"}, 404
        return self.model.remove_from_todo(todo_id, category_id)
    
    def get_todos_by_category(self, category_id):
        if not self.model.get_by_id(category_id):
            return {"error": "Category not found"}, 404
        return self.model.get_todos_by_category(category_id)
    
    def get_categories_for_todo(self, todo_id):
        # You might want to check if todo exists here
        return self.model.get_categories_for_todo(todo_id)
