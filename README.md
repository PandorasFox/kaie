# kaie
## A collection of tools around NTWEWY enemy data.

Currently just the main Noise Report (enemy number: days available, drop #s and %xs) as a pretty-printed json blob, and a collection of scripts to render it to markdown.

There is a large collection of data in parsing/, with most of it exposed via python objects in parsing.py. This is still currently a WIP, but the basic pin data (name, ID, sprite name) and noise data (number, drops, most stats) are exposed, as well as a lot of localization data.

Currently there's also data for pretty much everything you can think of available, I'm just still glueing it all together.

---

I am releasing the python tooling into the public domain as they are fairly trivial. Do what you want!


### TODO:

* Finish parsing all the data I have (see parsing/parsing.py for a todo list there)
* Serialize data to a more convenient format for parsing once finalized
* Probably write some rust tools around that data for templating for export to wikis
