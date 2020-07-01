# Recipe scraper server

This is a flask server that serves an API that accepts recipe urls and returns a parsed recipe. Uses [scrape-schema-recipe](https://github.com/micahcochran/scrape-schema-recipe) then falls back on [recipe-scrapers](https://github.com/hhursev/recipe-scrapers).

It returns an object that fits the [Schema.org Recipe](https://schema.org/Recipe) specification.

You can access the API [here](https://recipe-parser.azurewebsites.net/api)

## `GET /api/parse?url=[your_url_here]`

Returns the following:

```json
{
    @context: "http://schema.org",
    @type: "Recipe",
    aggregateRating: {
        @type: "AggregateRating",
        ratingValue: "5.0",
        reviewCount: "1394"
    },
    author: "Bev I Am",
    cookTime: "PT11M",
    datePublished: "2002-07-30T19:48Z",
    description: "You've made oatmeal-raisin cookies before, so why try these? Because they're moist, chewy and loaded with raisins - and they're better than any you've tried before! From Cuisine Magazine",
    image: "https://img.sndimg.com/food/image/upload/q_92,fl_progressive,w_1200,c_scale/v1/img/recipes/35/81/3/KU3JVxMDRriISEG3KdPy_0S9A9740.jpg",
    keywords: "Dessert,Lunch/Snacks,Cookie & Brownie,< 30 Mins,For Large Groups,Oven",
    mainEntityOfPage: "true",
    name: "Oatmeal Raisin Cookies",
    nutrition: {
        @type: "NutritionInformation",
        calories: "188.6",
        carbohydrateContent: "30.3",
        cholesterolContent: "23.9",
        fatContent: "6.4",
        fiberContent: "1.8",
        proteinContent: "3.5",
        saturatedFatContent: "3.5",
        sodiumContent: "117.1",
        sugarContent: "15.1"
    },
    prepTime: "PT15M",
    publisher: {
        @type: "Organization",
        logo: {
            @type: "ImageObject",
            url: "https://geniuskitchen.sndimg.com/fdc-new/img/FDC-Logo.png"
        },
        name: "Food.com",
        url: "https://www.food.com"
    },
    recipeCategory: "Drop Cookies",
    recipeIngredient: [
        "2 cups all-purpose flour",
        "1 teaspoon baking soda",
        "1 teaspoon baking powder",
        "1 teaspoon kosher salt",
        "1 cup unsalted butter, softened ",
        "1 cup sugar",
        "1 cup dark brown sugar, firmly packed ",
        "2 large eggs",
        "2 teaspoons vanilla",
        "3 cups oats (not instant)",
        "1 1/2 cups raisins"
    ],
    recipeInstructions: [
            "Preheat oven to 350&deg;.",
            "Whisk dry ingredients; set aside.",
            "Combine wet ingredients with a hand mixer on low.",
            "To cream, increase speed to high and beat until fluffy and the color lightens.",
            "Stir the flour mixture into the creamed mixture until no flour is visible.",
            "(Over mixing develops the gluten, making a tough cookie.) Now add the oats and raisins; stir to incorporate.",
            "Fill a #40 cookie scoop and press against side of bowl, pulling up to level dough (to measure 2 tablespoons of dough).",
            "Drop 2-inches apart onto baking sheet sprayed with nonstick spray.",
            "Bake 11-13 minutes (on center rack), until golden, but still moist beneath cracks on top.",
            "Remove from oven; let cookies sit on baking sheet for 2 minutes before transferring to a wire rack to cool."
    ],
    recipeYield: "36 cookies, 36 serving(s)",
    review: [
        {
            @type: "Review",
            author: "MizzNezz",
            datePublished: "October 22, 2002",
            description: "WOW!! These are the BEST oatmeal raisin cookies ever!! Soft, moist, chewy, the texture is perfect! I used unsalted butter and added 1/2 t cinnamon. These cookies are as good as any bakery sells. This will be my oatmeal cookie recipe from now on! Thanks Bev!!!",
            itemReviewed: {
                @type: "Thing",
                name: "Oatmeal Raisin Cookies"
        },
        reviewRating: {
            @type: "Rating",
            bestRating: "5",
            ratingValue: 5,
            worstRating: "1"
            }
        }
    ],
    totalTime: "PT26M",
    url: "https://www.food.com/recipe/oatmeal-raisin-cookies-35813"
    }
}
```

I am using it with my [some-recipes](https://github.com/boonepeter/some-recipes) site.

## Notes

I format the `recipeIngredients` and `author` so just strings are returned.
