# A noun symbol parser
I needed some symbols to use for a machine learning project and found out that thenounproject stores all their previews in svg format as base64 encoded strings.
The pages seems to be rendered with react which makes scraping harder. This project uses the pypputeer framework, which is an unofficial python port of the javascript framework pupputeer.

I have always wanted to try the new async module in python, so I figured, this would be the perfect time.

## Current state
It now reads 6 urls at a time, using an ansynchronos queue to keep track of the handled urls.

Only tested with python 3.7

## TODO
Create a check for page not found
Learn proper async

