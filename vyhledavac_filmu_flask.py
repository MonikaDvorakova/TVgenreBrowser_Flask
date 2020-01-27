# It filters movies, series or documentary. It finds some info about it on csfd.cz
# and it prints everything out.

from CT_functions import (download_TVlisting_xml, max_date_calculation, find_shows_genre,
                         find_hyperlink, csfd_redirect, ask_csfd, date_reformat)
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True
app.static_folder = 'static'


url = "https://www.ceskatelevize.cz/services-old/programme/xml/schedule.php"


@app.route('/', methods=["GET", "POST"])
def index():
    max_date = max_date_calculation()
    if request.method == "GET":
        return render_template("index.html", max_date=max_date)
    else:
        genre = request.form['genre']
        date = date_reformat(request.form['date'])
        channels = request.form.getlist('channel')
        xml_roots = download_TVlisting_xml(date, channels, url)
        searched_shows = find_shows_genre(xml_roots, genre)
        if not searched_shows:
            return f'Pro zvolený den a ČT kanály nejsou ve vysílání žádné {genre.lower()}.'
        else:
            searched_shows_with_description = ask_csfd(searched_shows)
            return render_template("results.html", results=searched_shows_with_description)


if __name__ == '__main__':
    app.run()