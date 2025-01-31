from flask import request
from flask_restful import Resource
from models import db, Recipe

class RecipeResource(Resource):
    # Get all recipes or a specific recipe by ID
    def get(self, recipe_id=None):
        if recipe_id:
            recipe = Recipe.query.get_or_404(recipe_id)
            return recipe.to_dict()
        else:
            recipes = Recipe.query.all()
            return [recipe.to_dict() for recipe in recipes], 200

    # Create a new recipe
    def post(self):
        data = request.get_json()

        # Validate required fields
        if not data or 'title' not in data or 'description' not in data or 'user_id' not in data:
            return {"message": "Missing required fields"}, 400

        # Create new recipe
        new_recipe = Recipe(
            title=data['title'],
            description=data['description'],
            user_id=data['user_id']
        )
        db.session.add(new_recipe)
        db.session.commit()

        return new_recipe.to_dict(), 201  # Created

    # Update an existing recipe
    def put(self, recipe_id):
        data = request.get_json()
        recipe = Recipe.query.get_or_404(recipe_id)

        # Update only if fields are provided
        if 'title' in data:
            recipe.title = data['title']
        if 'description' in data:
            recipe.description = data['description']
        if 'user_id' in data:
            recipe.user_id = data['user_id']

        db.session.commit()
        return recipe.to_dict(), 200  # OK

    # Delete a recipe
    def delete(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted"}, 204  # No Content
