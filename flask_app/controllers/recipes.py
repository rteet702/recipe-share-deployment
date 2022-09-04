from flask import render_template, redirect, session, request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app import app

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/')

    active_data = {'id': session['user_id']}
    active_user = User.get_by_id(active_data)
    users_with_recipies = Recipe.get_all_users_with_recipes()
    for user in users_with_recipies:
        print(user.id)

    return render_template('recipes.html', user=active_user, uwr=users_with_recipies)


@app.route('/recipes/create')
def r_create_recipies():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html', user=session['user_id'])


@app.route('/recipes/submit', methods=['POST'])
def f_create_recipies():
    recipe_data = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'instructions': request.form.get('instructions'),
        'date_cooked': request.form.get('date_cooked'),
        'under_30': request.form.get('under_30'),
        'user_id': request.form.get('user_id')
    }

    if not Recipe.validate_recipe(recipe_data):
        return redirect('/recipes/create')

    Recipe.create_recipe(recipe_data)
    return redirect('/recipes')


@app.route('/recipes/<int:id>/edit')
def r_edit_recipes(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_data = {'id' : id}
    recipe = Recipe.find_by_id(recipe_data)
    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/recipes/edit', methods=['POST'])
def f_edit_recipes():
    recipe_data = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'instructions': request.form.get('instructions'),
        'date_cooked': request.form.get('date_cooked'),
        'under_30': request.form.get('under_30'),
        'id': request.form.get('id')
    }

    id = recipe_data.get('id')
    if not Recipe.validate_recipe(recipe_data):
        return redirect(f'/recipes/{id}/edit')

    Recipe.update_recipe(recipe_data)
    return redirect('/recipes')


@app.route('/recipes/<int:id>')
def r_view_recipes(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_data = {'id' : id}
    user_data = {'id': session['user_id'] }

    recipe = Recipe.find_by_id(recipe_data)
    active_user = User.get_by_id(user_data)
    author = User.get_user_by_recipe(recipe_data)
    return render_template('view_recipe.html', recipe=recipe, user=active_user, author=author)


@app.route('/recipes/<int:id>/delete')
def f_delete_recipe(id):
    data = {'id' : id}
    Recipe.delete_recipe(data)
    return redirect('/recipes')