from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data ['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
        self.first_name = data['first_name']
        
    @staticmethod
    def validate_recipe(formulario):
        is_valid = True
        
        if len(formulario['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', "receta")
            is_valid = False
            
        if len(formulario['description']) < 3:
            flash('La descripción de la receta debe tener al menos 3 caracteres', "receta")
            is_valid = False

        if len(formulario['instructions']) < 3:
            flash('Las instructiones de la receta deben tener al menos 3 caracteres', "receta")
            is_valid = False
            
        if formulario['date_made'] == "":
            flash("por favor ingrese una fecha", "receta")
            is_valid = False
            
        return is_valid
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, %(user_id)s)"
        newId = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return newId
    
    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL('esquema_recetas').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s" #LEFT JOIN users
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        recipe = cls(result[0]) #Creamos una instancia de receta
        return recipe
    
    @classmethod
    def update(cls, formulario): #Recibir el formulario. OJO con todo y el ID de la receta
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under30 = %(under30)s WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result
    
    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result