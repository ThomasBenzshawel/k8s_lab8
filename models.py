import sqlite3


class Schema:
    def __init__(self):
       self.conn = sqlite3.connect('todo.db')
       self.create_user_table()
       self.create_to_do_table()
       self.create_category_table()
       self.create_todo_category_table()


    def __del__(self):
       # body of destructor
       self.conn.commit()
       self.conn.close()

    def create_to_do_table(self):

       query = """
       CREATE TABLE IF NOT EXISTS "Todo" (
         id INTEGER PRIMARY KEY,
         Title TEXT,
         Description TEXT,
         _is_done boolean DEFAULT 0,
         _is_deleted boolean DEFAULT 0,
         CreatedOn Date DEFAULT CURRENT_DATE,
         DueDate Date,
         UserId INTEGER FOREIGNKEY REFERENCES User(_id)
       );
       """

       self.conn.execute(query)

    def create_user_table(self):
       query = """
       CREATE TABLE IF NOT EXISTS "User" (
       _id INTEGER PRIMARY KEY AUTOINCREMENT,
       Name TEXT NOT NULL,
       Email TEXT,
       CreatedOn Date default CURRENT_DATE
       );
       """
       self.conn.execute(query)
    
    def create_category_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Category" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Color TEXT DEFAULT '#000000',
            CreatedOn Date DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)
        
    def create_todo_category_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "TodoCategory" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TodoId INTEGER,
            CategoryId INTEGER,
            FOREIGN KEY (TodoId) REFERENCES Todo(id),
            FOREIGN KEY (CategoryId) REFERENCES Category(id)
        );
        """
        self.conn.execute(query)

class ToDoModel:
   TABLENAME = "Todo"

   def __init__(self):
       self.conn = sqlite3.connect('todo.db')
       self.conn.row_factory = sqlite3.Row

   def __del__(self):
       # body of destructor
       self.conn.commit()
       self.conn.close()

   def get_by_id(self, _id):
       where_clause = f"AND id={_id}"
       return self.list_items(where_clause)

   def create(self, params):
       print (params)
       query = f'insert into {self.TABLENAME} ' \
               f'(Title, Description, DueDate, UserId) ' \
               f'values ("{params.get("Title")}","{params.get("Description")}",' \
               f'"{params.get("DueDate")}","{params.get("UserId")}")'

       """insert into todo (Title, Description, DueDate, UserId) values ("todo1","todo1", "2018-01-01", 1)"""
      
       result = self.conn.execute(query)
       return self.get_by_id(result.lastrowid)

   def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted = {1} " \
                f"WHERE id = {item_id}"
        print(query)
        self.conn.execute(query)
        return self.list_items()

   def update(self, item_id, update_dict):
       """
       column: value
       Title: new title
       """
       set_query = ", ".join([f'{column} = "{value}"'
                    for column, value in update_dict.items()])

       query = f"UPDATE {self.TABLENAME} " \
               f"SET {set_query} " \
               f"WHERE id = {item_id}"
  
       self.conn.execute(query)
       return self.get_by_id(item_id)

   def list_items(self, where_clause=""):
        query = f"SELECT id, Title, Description, DueDate, _is_done " \
                f"FROM {self.TABLENAME} " \
                f"WHERE _is_deleted != {1} {where_clause}"
        print(query)
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        
        # Handle empty result sets
        if not result_set:
            return []
            
        result = [{column: row[i]
                for i, column in enumerate(result_set[0].keys())}
                for row in result_set]
        return result
   

class CategoryModel:
    TABLENAME = "Category"
    
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row
        
    def __del__(self):
        self.conn.commit()
        self.conn.close()
        
    def create(self, name, color="#000000"):
        query = "INSERT INTO Category (Name, Color) VALUES (?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(query, (name, color))
        self.conn.commit()
        return {"id": cursor.lastrowid, "name": name, "color": color}
    
    def get_by_id(self, category_id):
        query = f"SELECT id, Name, Color, CreatedOn FROM {self.TABLENAME} WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (category_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        return {
            "id": row["id"],
            "name": row["Name"],
            "color": row["Color"],
            "created_on": row["CreatedOn"]
        }
    
    def list_all(self):
        query = f"SELECT id, Name, Color, CreatedOn FROM {self.TABLENAME}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "name": row["Name"],
                "color": row["Color"],
                "created_on": row["CreatedOn"]
            })
            
        return result
    
    def update(self, category_id, params):
        valid_fields = ["Name", "Color"]
        updates = []
        values = []
        
        for field in valid_fields:
            if field.lower() in [k.lower() for k in params.keys()]:
                key = next(k for k in params.keys() if k.lower() == field.lower())
                updates.append(f"{field} = ?")
                values.append(params[key])
        
        if not updates:
            return self.get_by_id(category_id)
            
        query = f"UPDATE {self.TABLENAME} SET {', '.join(updates)} WHERE id = ?"
        values.append(category_id)
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        return self.get_by_id(category_id)
    
    def delete(self, category_id):
        # First, delete all associations
        assoc_query = "DELETE FROM TodoCategory WHERE CategoryId = ?"
        self.conn.execute(assoc_query, (category_id,))
        
        # Then delete the category
        query = f"DELETE FROM {self.TABLENAME} WHERE id = ?"
        self.conn.execute(query, (category_id,))
        self.conn.commit()
        
        return {"success": True, "message": f"Category {category_id} deleted"}
    
    def assign_to_todo(self, todo_id, category_id):
        # Check if association already exists
        check_query = "SELECT id FROM TodoCategory WHERE TodoId = ? AND CategoryId = ?"
        cursor = self.conn.cursor()
        cursor.execute(check_query, (todo_id, category_id))
        if cursor.fetchone():
            return {"success": True, "message": "Association already exists"}
            
        query = "INSERT INTO TodoCategory (TodoId, CategoryId) VALUES (?, ?)"
        self.conn.execute(query, (todo_id, category_id))
        self.conn.commit()
        
        return {"success": True, "message": "Category assigned to task"}
    
    def remove_from_todo(self, todo_id, category_id):
        query = "DELETE FROM TodoCategory WHERE TodoId = ? AND CategoryId = ?"
        self.conn.execute(query, (todo_id, category_id))
        self.conn.commit()
        
        return {"success": True, "message": "Category removed from task"}
    
    def get_todos_by_category(self, category_id):
        query = """
        SELECT t.id, t.Title, t.Description, t.DueDate, t._is_done 
        FROM Todo t
        JOIN TodoCategory tc ON t.id = tc.TodoId
        WHERE tc.CategoryId = ? AND t._is_deleted != 1
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (category_id,))
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "title": row["Title"],
                "description": row["Description"],
                "due_date": row["DueDate"],
                "is_done": bool(row["_is_done"])
            })
            
        return result
        
    def get_categories_for_todo(self, todo_id):
        query = """
        SELECT c.id, c.Name, c.Color
        FROM Category c
        JOIN TodoCategory tc ON c.id = tc.CategoryId
        WHERE tc.TodoId = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (todo_id,))
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "name": row["Name"],
                "color": row["Color"]
            })
            
        return result


class User:
   TABLENAME = "User"

   def create(self, name, email):
       query = f'insert into {self.TABLENAME} ' \
               f'(Name, Email) ' \
               f'values ({name},{email})'
       result = self.conn.execute(query)
       return result
