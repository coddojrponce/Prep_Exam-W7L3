from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Item:
    DB = "exam_prep"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.img_url = data['img_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner=None 
        self.likes=[]
        
    # the save method will be used when we need to save a new friend to our database
    @classmethod
    def save(cls, data):
        query = """INSERT INTO items (name, description,price,img_url,user_id)
    		VALUES (%(name)s, %(description)s, %(price)s,%(img_url)s,%(user_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, item_id):
        query  = """
            SELECT * FROM items 
            LEFT JOIN likes 
            ON items.id = likes.item_id 
            LEFT JOIN users 
            ON likes.user_id = users.id 
            WHERE items.id = %(id)s;        
        
        """
        data = {'id': item_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        if not results:
            return None
        this_item = cls(results[0])
        for item in results:
            if not item["likes.user_id"] == None:
                data={
                    "id":item["users.id"],
                    "first_name":item["first_name"],
                    "last_name":item["last_name"],
                    "email":item["email"],
                    "password":item["password"],
                    "created_at":item["users.created_at"],
                    "updated_at":item["users.updated_at"]
                }

                this_item.likes.append(user.User(data))

        return this_item

    # @classmethod
    # def get_all(cls):
    #     query = """
    #     SELECT * FROM items
    #     LEFT JOIN users
    #     ON items.user_id = users.id
        
    #     ;
        
    #     """
    #     results = connectToMySQL(cls.DB).query_db(query)
    #     if not results:
    #         return []
    #     items = []
    #     for item in results:
    #         this_item = cls(item)
    #         data={
    #             "id":item["users.id"],
    #             "first_name":item["first_name"],
    #             "last_name":item["last_name"],
    #             "email":item["email"],
    #             "password":item["password"],
    #             "created_at":item["users.created_at"],
    #             "updated_at":item["users.updated_at"]
    #         }

    #         this_item.owner = user.User(data)
    #         items.append(this_item)


    #     return items
    
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM items
        LEFT JOIN users
        ON items.user_id = users.id
        LEFT JOIN likes
        ON items.id = likes.item_id
        LEFT JOIN users as liked_by
        ON likes.user_id = liked_by.id
        ;
        
        """
        results = connectToMySQL(cls.DB).query_db(query)
        this_item=None
        if not results:
            return []
        items = []
        print("Here are the results")
        # for x in results:
        #     print(x.keys())
        for item in results:
            if this_item == None:
                this_item = cls(item)
                items.append(this_item)
            elif not this_item.id == item['id']:
                this_item = cls(item)
                items.append(this_item)
            data={
                "id":item["users.id"],
                "first_name":item["first_name"],
                "last_name":item["last_name"],
                "email":item["email"],
                "password":item["password"],
                "created_at":item["users.created_at"],
                "updated_at":item["users.updated_at"]
            }
            this_item.owner = user.User(data)

            if not item["likes.user_id"] == None:
                data={
                    "id":item["liked_by.id"],
                    "first_name":item["liked_by.first_name"],
                    "last_name":item["liked_by.last_name"],
                    "email":item["liked_by.email"],
                    "password":item["liked_by.password"],
                    "created_at":item["liked_by.created_at"],
                    "updated_at":item["liked_by.updated_at"]
                }
                this_item.likes.append(user.User(data))
            

        return items

    @classmethod
    def update(cls,data):
        query = """UPDATE items 
                SET name=%(name)s,description=%(description)s,img_url=%(img_url)s, price=%(price)s 
                WHERE id = %(id)s AND items.user_id = %(user_id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def delete(cls, id,user_id):
        query  = "DELETE FROM items WHERE id = %(id)s AND user_id = %(user_id)s;"
        data = {"id": id,"user_id":user_id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def like(cls,id,user_id):
        query  = "INSERT INTO likes(user_id,item_id) VALUES(%(user_id)s,%(id)s);"
        data = {"id": id,"user_id":user_id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def unlike(cls,id,user_id):
        query  = "DELETE FROM likes WHERE likes.user_id = %(user_id)s AND id = %(id)s;"
        data = {"id": id,"user_id":user_id}
        return connectToMySQL(cls.DB).query_db(query, data)

        
    @staticmethod
    def validate_item(data):
        is_valid = True # we assume this is true
        if len(data['name']) == 0:
            flash("Name must not be blank")
            is_valid = False
        elif len(data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(data['price']) == 0:
            flash("Price must not be blank.")
            is_valid = False
        elif float(data['price']) < 1:
            flash("Price must be 1 dollar or greater.")
            is_valid = False
        if len(data['img_url']) < 3:
            flash("Url be at least 3 characters.")
            is_valid = False
        return is_valid