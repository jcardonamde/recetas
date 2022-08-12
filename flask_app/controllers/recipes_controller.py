from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.recipes import Recipe
from flask_app.models.users import User


@app.route('/new/recipe')
def new_recipe():
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }
    user = User.get_by_id(formulario)
    
    return render_template('new_recipe.html', user = user)

@app.route('/create/recipe', methods = ['POST'])
def create_recipe():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    
    Recipe.save(request.form)
    return redirect('/recipes')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario = {
        "id": session['usuario_id']
    }
    user = User.get_by_id(formulario)
    
    formulario_receta = { "id": id }
    recipe = Recipe.get_by_id(formulario_receta) #llamar a una función y debo de recibir la receta
    
    return render_template('edit_recipe.html', user = user, recipe = recipe)    

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit/recipe/'+request.form['id']) #/edit/recipe/1
    Recipe.update(request.form)

    return redirect('/recipes')

@app.route('/show/recipe/<int:id>') #A través de la URL recibimos el ID de la receta
def show_recipe(id):
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }
    user = User.get_by_id(formulario) #Usuario que inició sesión

    formulario_receta = { "id": id }
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user = user, recipe = recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = { "id": id }
    Recipe.delete(formulario)

    return redirect('/recipes')