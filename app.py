from flask import Flask, request, make_response
from recipe_scrapers import scrape_me
import scrape_schema_recipe
from flask_cors import CORS
from recipe_scrapers._utils import get_minutes
import html

app = Flask(__name__)
CORS(app)

@app.route('/api/parse', methods=["GET"])
def parse_recipe():
    try:
        recipe_url = request.args.get('url')
    except:
        return make_response('Need a url in parameters. See <a href="/api">/api</a> for more info', 404)
    try:
        recipes = scrape_schema_recipe.scrape_url(recipe_url)
        if len(recipes) == 1 and recipes[0] is not None:
            recipe = recipes[0]
            if 'recipeInstructions' in recipe:
                ins = recipe['recipeInstructions']
                if type(ins) == str:
                    recipe['recipeInstructions'] = [html.escape(ins)]
                elif type(ins) == list and len(ins) > 0:
                    if type(ins[0]) == dict:
                        recipe['recipeInstructions'] = []
                        for item in ins:
                            for k, v in item.items():
                                if k == 'text':
                                    recipe['recipeInstructions'].append(html.escape(v))
                    else:
                        recipe['recipeInstructions'] = [html.escape(i) for i in recipe['recipeInstructions']]
            if 'keywords' in recipe:
                recipe['keywords'] = [html.escape(i.strip()) for i in recipe['keywords'].split(',')]
            if 'image' in recipe:
                if type(recipe['image']) == dict:
                    if 'url' in recipe['image']:
                        recipe['image'] = recipe['image']['url']
            if 'image' in recipe:
                if type(recipe['image']) == list:
                    recipe['image'] = recipe['image'][-1]
            if 'author' in recipe:
                if type(recipe['author']) == dict and 'name' in recipe['author']:
                    recipe['author'] = html.escape(recipe['author']['name'])
            if 'recipeYield' in recipe:
                rYield = recipe['recipeYield']
                if type(rYield) == str:
                    recipe['recipeYield'] = [i.strip() for i in rYield.split(',')][0]
                if type(rYield) == list and len(rYield) > 0:
                    recipe['recipeYield'] = rYield[0]
            if 'cookTime' in recipe:
                recipe['cookTime'] = get_minutes(recipe['cookTime'])
            if 'prepTime' in recipe:
                recipe['prepTime'] = get_minutes(recipe['prepTime'])
            if 'totalTime' in recipe:
                recipe['totalTime'] = get_minutes(recipe['totalTime'])
            return recipe
    except Exception as e:
        print(e.args)
        pass
    
    try:
        recipe = scrape_me(recipe_url)
        to_return = {
            "@type": "noSchema",
            "name": recipe.title(),
            "url": recipe.url(),
            "recipeIngredients": recipe.ingredients(),
            "recipeInstructions": [i for i in recipe.instructions().split('\n') if i != ""],
            "review": recipe.reviews(),
            "aggregateRating": recipe.ratings(),
            "totalTime": recipe.total_time(),
            "recipeYield": recipe.yields(),
            "image": recipe.image()
        }
        return to_return
    except Exception as e:
        return make_response(f'Error processing request. That domain might not be in the list\
             See <a href="/api">/api</a> for more info. Error: {e.args}', 500)

@app.route('/api', methods=['GET'])
def about_api():
    return """
        <h1>Recipe Parser API</h1>
        <p>
        This API accepts a url to a recipe and returns the recipe info as JSON.
        </p>
        <p>
        I use <a href="https://github.com/micahcochran/scrape-schema-recipe">scrape-schema-recipe</a>
        first, then <a href="https://github.com/hhursev/recipe-scrapers">recipe-scrapers</a> to do the scraping.
        </p>

        <h2>
        <strong><code>GET /api/parse?url=[your_url_here]</code></strong>
        </h2>
        <p>
        If successfully parsed, it will return a <a href="https://schema.org/Recipe">Schema.org Recipe</a>. If it has to fall back to recipe-scrapers, it will note the "@type" as "noSchema"
        </p>
    """

@app.errorhandler(404)
def not_found(error):
    return make_response('Path not found. See <a href="/api">/api</a> for more info', 404)
