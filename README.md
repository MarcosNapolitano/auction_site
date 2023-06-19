# <div align="center">Auctions Site</div>

This is originally a project in Harvard's CS50W course. You can visit my version [here](https://marcos-napolitano-auctions-site.up.railway.app/)! :rocket:

I wanted to build an auction commerce that had an ebay kind of feel. I ended up adding a carousel in JavaScript and several custom built components. This was a long project to do, mostly because of the user interface, as the project grows larger, everything is harder to mantain in order. Despite of the size I managed to keep everything as simple and commented as posible. Feel free to make any suggestions! 

## Tech Stack

* HTML
* CSS
* JavaScript
* Django
* Python Decouple - Stores enviroment variables securely.

## Quickview

![Screenshot of the site](https://marcosnapolitano.github.io/Assets/django_auctions.jpg)

## Quickstart

*Make sure both python and virtualenv are installed on your OS.*

1. Fork the project.
2. Clone project using `git clone git@github.com:<YOUR-USERNAME>/auctions_site.git`.
3. Run `virtualenv env` then `env\scripts\activate`.
4. Once in your virtual enviroment `(env)`, run `pip install -r "auctions_site\requirements.txt"`.
5. You need to generate a SECRET_KEY now, in order to do so you have to:
    ```
    (env)... cd auctions_site
    (env)... auctions_site\python
    
    >>> from django.core.management.utils import get_random_secret_key
    >>> SECRET_KEY = get_random_secret_key()
    >>> exit()
    ```
6. Create a `.env` file and paste `SECRET_KEY=[NEW_SECRET_KEY]`
7. Run `python manage.py runserver`

## Docs

All logic contained in `Views.py` in the `auctions` folder. There is mostly querys going on, but nothing too over the top or complicated. The comments themselves should make everything clear as to what is going on.

## Final Notes

This site was deployed using [Railway](https://railway.app/).
