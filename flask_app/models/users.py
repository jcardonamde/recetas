from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data ['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result
    
    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        # Siempre que hacemos un SELECT recibimos una lista
        if len(result) < 1:
            return False
        else:
            user = cls(result[0]) #Haciendo una instancia de User -> CON los datos que recibimos de la base de datos
            return user
        
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario) #Select recibe lista
        user = cls(result[0])
        return user
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('esquema_recetas').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @staticmethod
    def validate_user(formulario):
        is_valid = True
        
        #Validar que mi nombre tenga más de 2 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe de tener al menos 3 caracteres', 'registro')
            is_valid = False
            
        if len(formulario['last_name']) < 3:
            flash('Apellido debe de tener al menos 3 caracteres', 'registro')
            is_valid = False
        
        #valido email con expresiones regulares
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email invalido', 'registro')
            is_valid = False
            
        if len(formulario['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            is_valid = False
            
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coinciden', 'registro')
            is_valid = False
            
        #Consultar si YA existe el correo
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_recetas').query_db(query, formulario)
        if len(results) >= 1:
            flash('Email registrado previamente', 'registro')
            is_valid = False
            
        return is_valid
