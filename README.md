# A noun symbol parser
I needed some symbols to use for a machine learning project and found out that thenounproject stores all their previews in svg format as base64 encoded strings.
The pages seems to be rendered with react which makes scraping harder. This project uses the pypputeer framework, which is an unofficial python port of the javascript framework pupputeer.

I have always wanted to use the fairly new async stuff in python so I figured, this would be the perfect time

## Current state
It now reads 5 urls at a time, using a syncronous blocking for-loop to avoid timeouts. This should not be there. I just can't figure out how to remove it. At the moment.

Only tested with python 3.7

## TODO
Figure out how to not call everything at once
Learn proper async
