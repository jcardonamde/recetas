from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) #Inicializando instancia de Bcrypt


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password'])
    formulario = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pwd
    }
    
    id  = User.save(formulario) #Guardando a mi usuario y recibo el ID del nuevo registro
    session['usuario_id'] = id #Guardando en sesion el identificador
    return redirect ('/recipes')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user: #si user=False
        flash("E-mail no encontrado", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", "login")
        return redirect('/')
    
    session['usuario_id'] = user.id
    return redirect('/recipes')

@app.route('/recipes')
def recipes():
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario = {
        "id": session['usuario_id']
    }
    user = User.get_by_id(formulario) #El usuario que inicio sesión
    recipes = Recipe.get_all() #Lista de todas las recetas
    
    return render_template('recipes.html', user = user, recipes = recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')