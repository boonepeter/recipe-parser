# Recipe scraper server

This is a flask server that serves an API that accepts recipe urls and returns a parsed recipe. Uses [recipe-scrapers](https://github.com/hhursev/recipe-scrapers)

You can access the API [here](https://recipe-parser.azurewebsites.net/api)

## `GET /api/parse?url=[your_url_here]`

Returns the following:

```json
{
    link: "recipe url",
    ingredients: ["strings"],
    directions: ["strings"],
    reviews: int,
    ratings: float,
    total_time: int,
    yields: "n serving(s)",
    image: "image url" 
}
```

I am using it with my [some-recipes](https://github.com/boonepeter/some-recipes) site.
