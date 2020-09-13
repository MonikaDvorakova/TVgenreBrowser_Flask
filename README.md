# TVgenreBrowser_Flask

The program is a web application.

The aim of the program is to find out all TV shows of specific genre (films, series, documentary) for selected day and 
TV channels of Česká televize and to show the final list of the shows with the corresponding information about particular show
(time and channel of broadcasting, its short description, rating in the CSFD movie database (https://www.csfd.cz/)...).
The TV listing is provided by Česká televize in XML format on webpage https://www.ceskatelevize.cz/xml/tv-program/
after registration.

## Requirements
* Python 3
* requests library
```
python -m pip install requests
```
* Beautiful Soup library
```
python -m pip install beautifulsoup4
```
* flask library
```
python -m pip install flask
```
## Authentication
All requests to the program must be authenticated using your username (registration here:
https://www.ceskatelevize.cz/xml/tv-program/registrace/).

## How to use it
* Register here: https://www.ceskatelevize.cz/xml/tv-program/registrace/.
* Create login.txt file and save there your username.
* Use vyhledavac_filmu_flask.py to run the program.
