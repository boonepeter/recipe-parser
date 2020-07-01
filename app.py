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
    <h1 id="recipe-scraper-server">Recipe scraper server</h1>
<p>This is a flask server that serves an API that accepts recipe urls and returns a parsed recipe. Uses <a href="https://github.com/micahcochran/scrape-schema-recipe">scrape-schema-recipe</a> then falls back on <a href="https://github.com/hhursev/recipe-scrapers">recipe-scrapers</a>.</p>
<p>It returns an object that fits the <a href="https://schema.org/Recipe">Schema.org Recipe</a> specification.</p>
<p>You can access the API <a href="https://recipe-parser.azurewebsites.net/api">here</a></p>
<h2 id="-get-api-parse-url-your_url_here-"><code>GET /api/parse?url=[your_url_here]</code></h2>
<p>Returns the following:</p>
<pre><code class="lang-json">{
    <span class="hljs-variable">@context:</span> <span class="hljs-string">"http://schema.org"</span>,
    <span class="hljs-variable">@type</span>: <span class="hljs-string">"Recipe"</span>,
    <span class="hljs-attribute">aggregateRating</span>: {
        <span class="hljs-variable">@type:</span> <span class="hljs-string">"AggregateRating"</span>,
        <span class="hljs-attribute">ratingValue</span>: <span class="hljs-string">"5.0"</span>,
        <span class="hljs-attribute">reviewCount</span>: <span class="hljs-string">"1394"</span>
    },
    <span class="hljs-attribute">author</span>: <span class="hljs-string">"Bev I Am"</span>,
    <span class="hljs-attribute">cookTime</span>: <span class="hljs-string">"PT11M"</span>,
    <span class="hljs-attribute">datePublished</span>: <span class="hljs-string">"2002-07-30T19:48Z"</span>,
    <span class="hljs-attribute">description</span>: <span class="hljs-string">"You've made oatmeal-raisin cookies before, so why try these? Because they're moist, chewy and loaded with raisins - and they're better than any you've tried before! From Cuisine Magazine"</span>,
    <span class="hljs-attribute">image</span>: <span class="hljs-string">"https://img.sndimg.com/food/image/upload/q_92,fl_progressive,w_1200,c_scale/v1/img/recipes/35/81/3/KU3JVxMDRriISEG3KdPy_0S9A9740.jpg"</span>,
    <span class="hljs-attribute">keywords</span>: <span class="hljs-string">"Dessert,Lunch/Snacks,Cookie &amp; Brownie,&lt; 30 Mins,For Large Groups,Oven"</span>,
    <span class="hljs-attribute">mainEntityOfPage</span>: <span class="hljs-string">"true"</span>,
    <span class="hljs-attribute">name</span>: <span class="hljs-string">"Oatmeal Raisin Cookies"</span>,
    <span class="hljs-attribute">nutrition</span>: {
        <span class="hljs-variable">@type:</span> <span class="hljs-string">"NutritionInformation"</span>,
        <span class="hljs-attribute">calories</span>: <span class="hljs-string">"188.6"</span>,
        <span class="hljs-attribute">carbohydrateContent</span>: <span class="hljs-string">"30.3"</span>,
        <span class="hljs-attribute">cholesterolContent</span>: <span class="hljs-string">"23.9"</span>,
        <span class="hljs-attribute">fatContent</span>: <span class="hljs-string">"6.4"</span>,
        <span class="hljs-attribute">fiberContent</span>: <span class="hljs-string">"1.8"</span>,
        <span class="hljs-attribute">proteinContent</span>: <span class="hljs-string">"3.5"</span>,
        <span class="hljs-attribute">saturatedFatContent</span>: <span class="hljs-string">"3.5"</span>,
        <span class="hljs-attribute">sodiumContent</span>: <span class="hljs-string">"117.1"</span>,
        <span class="hljs-attribute">sugarContent</span>: <span class="hljs-string">"15.1"</span>
    },
    <span class="hljs-attribute">prepTime</span>: <span class="hljs-string">"PT15M"</span>,
    <span class="hljs-attribute">publisher</span>: {
        <span class="hljs-variable">@type:</span> <span class="hljs-string">"Organization"</span>,
        <span class="hljs-attribute">logo</span>: {
            <span class="hljs-variable">@type:</span> <span class="hljs-string">"ImageObject"</span>,
            <span class="hljs-attribute">url</span>: <span class="hljs-string">"https://geniuskitchen.sndimg.com/fdc-new/img/FDC-Logo.png"</span>
        },
        <span class="hljs-attribute">name</span>: <span class="hljs-string">"Food.com"</span>,
        <span class="hljs-attribute">url</span>: <span class="hljs-string">"https://www.food.com"</span>
    },
    <span class="hljs-attribute">recipeCategory</span>: <span class="hljs-string">"Drop Cookies"</span>,
    <span class="hljs-attribute">recipeIngredient</span>: [
        <span class="hljs-string">"2 cups all-purpose flour"</span>,
        <span class="hljs-string">"1 teaspoon baking soda"</span>,
        <span class="hljs-string">"1 teaspoon baking powder"</span>,
        <span class="hljs-string">"1 teaspoon kosher salt"</span>,
        <span class="hljs-string">"1 cup unsalted butter, softened "</span>,
        <span class="hljs-string">"1 cup sugar"</span>,
        <span class="hljs-string">"1 cup dark brown sugar, firmly packed "</span>,
        <span class="hljs-string">"2 large eggs"</span>,
        <span class="hljs-string">"2 teaspoons vanilla"</span>,
        <span class="hljs-string">"3 cups oats (not instant)"</span>,
        <span class="hljs-string">"1 1/2 cups raisins"</span>
    ],
    <span class="hljs-attribute">recipeInstructions</span>: [
            <span class="hljs-string">"Preheat oven to 350&amp;deg;."</span>,
            <span class="hljs-string">"Whisk dry ingredients; set aside."</span>,
            <span class="hljs-string">"Combine wet ingredients with a hand mixer on low."</span>,
            <span class="hljs-string">"To cream, increase speed to high and beat until fluffy and the color lightens."</span>,
            <span class="hljs-string">"Stir the flour mixture into the creamed mixture until no flour is visible."</span>,
            <span class="hljs-string">"(Over mixing develops the gluten, making a tough cookie.) Now add the oats and raisins; stir to incorporate."</span>,
            <span class="hljs-string">"Fill a #40 cookie scoop and press against side of bowl, pulling up to level dough (to measure 2 tablespoons of dough)."</span>,
            <span class="hljs-string">"Drop 2-inches apart onto baking sheet sprayed with nonstick spray."</span>,
            <span class="hljs-string">"Bake 11-13 minutes (on center rack), until golden, but still moist beneath cracks on top."</span>,
            <span class="hljs-string">"Remove from oven; let cookies sit on baking sheet for 2 minutes before transferring to a wire rack to cool."</span>
    ],
    <span class="hljs-attribute">recipeYield</span>: <span class="hljs-string">"36 cookies, 36 serving(s)"</span>,
    <span class="hljs-attribute">review</span>: [
        {
            <span class="hljs-variable">@type:</span> <span class="hljs-string">"Review"</span>,
            <span class="hljs-attribute">author</span>: <span class="hljs-string">"MizzNezz"</span>,
            <span class="hljs-attribute">datePublished</span>: <span class="hljs-string">"October 22, 2002"</span>,
            <span class="hljs-attribute">description</span>: <span class="hljs-string">"WOW!! These are the BEST oatmeal raisin cookies ever!! Soft, moist, chewy, the texture is perfect! I used unsalted butter and added 1/2 t cinnamon. These cookies are as good as any bakery sells. This will be my oatmeal cookie recipe from now on! Thanks Bev!!!"</span>,
            <span class="hljs-attribute">itemReviewed</span>: {
                <span class="hljs-variable">@type:</span> <span class="hljs-string">"Thing"</span>,
                <span class="hljs-attribute">name</span>: <span class="hljs-string">"Oatmeal Raisin Cookies"</span>
        },
        <span class="hljs-attribute">reviewRating</span>: {
            <span class="hljs-variable">@type:</span> <span class="hljs-string">"Rating"</span>,
            <span class="hljs-attribute">bestRating</span>: <span class="hljs-string">"5"</span>,
            <span class="hljs-attribute">ratingValue</span>: <span class="hljs-number">5</span>,
            <span class="hljs-attribute">worstRating</span>: <span class="hljs-string">"1"</span>
            }
        }
    ],
    <span class="hljs-attribute">totalTime</span>: <span class="hljs-string">"PT26M"</span>,
    <span class="hljs-attribute">url</span>: <span class="hljs-string">"https://www.food.com/recipe/oatmeal-raisin-cookies-35813"</span>
    }
}
</code></pre>
<p>I am using it with my <a href="https://github.com/boonepeter/some-recipes">some-recipes</a> site.</p>
<h2 id="notes">Notes</h2>
<p>I format the <code>recipeIngredients</code> and <code>author</code> so just strings are returned.</p>

    """

@app.errorhandler(404)
def not_found(error):
    return make_response('Path not found. See <a href="/api">/api</a> for more info', 404)
