from flask import Flask, request, make_response
from recipe_scrapers import scrape_me
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/parse', methods=["GET"])
def parse_recipe():
    try:
        recipe_url = request.args.get('url')
    except:
        return make_response('Need a url in parameters. See <a href="/api">/api</a> for more info', 404)
    try:
        recipe = scrape_me(recipe_url)
        to_return = {
            "link": recipe_url,
            "ingredients": recipe.ingredients(),
            "directions": [i for i in recipe.instructions().split('\n') if i != ""],
            "reviews": recipe.reviews(),
            "ratings": recipe.ratings(),
            "total_time": recipe.total_time(),
            "yields": recipe.yields(),
            "image": recipe.image()
        }
        return to_return
    except Exception as e:
        return make_response(f'Error processing request. That domain might not be in the list\
             See <a href="/api">/api</a> for more info. Error: {e.args}', 404)

@app.route('/api', methods=['GET'])
def about_api():
    return """
        <h1>Recipe Parser API</h1>
        <p>
        This API accepts a url to a recipe and returns the recipe info as JSON.
        </p>
        <p>
        I use <a href="https://github.com/hhursev/recipe-scrapers">recipe-scrapers</a> to do the scraping.
        </p>

        <h2>
        <strong><code>GET /api/parse?url=[your_url_here]</code></strong>
        </h2>
        <p>
        If successfully parsed, it will return the following:
        </p>
        <code>
            {
                "link": "",
                "ingredients": [],
                "directions": [],
                "reviews": int,
                "ratings": float,
                "total_time": int,
                "yields": "n serving(s)",
                "image": ""
            }
        </code>

    """

@app.errorhandler(404)
def not_found(error):
    return make_response('Path not found. See <a href="/api">/api</a> for more info', 404)
