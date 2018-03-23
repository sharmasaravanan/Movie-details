from flask import Flask, request, render_template,url_for, redirect,session
from imdbpie import Imdb
import sys,os

app = Flask(__name__)
imdb = Imdb()

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('movie.html')
    elif request.method == 'POST':
	m=request.form['m']
	det=imdb.search_for_title(m)
	id=det[0]['imdb_id']
	rate=imdb.get_title_ratings(id)
	gen=imdb.get_title_genres(id)
	sim=imdb.get_title_similarities(id)
	relea=imdb.get_title_releases(id)
	plot=imdb.get_title_plot(id)
	credit=imdb.get_title_credits(id)
	ratin=rate['rating']
	genre=gen['genres']
	similar=sim['similarities'][0]['title'].encode('UTF8')
	release=relea['releases'][0]['date'].encode('UTF8')
	plots=plot['outline']['text'].encode('UTF8')
	producer=credit['credits']['producer'][0]['name'].encode('UTF8')
	director=credit['credits']['director'][0]['name'].encode('UTF8')
	hero=credit['credits']['cast'][0]['name'].encode('UTF8')
	heroin=credit['credits']['cast'][1]['name'].encode('UTF8')
	kwargs = {
		'title':m,'date':release,'plot':plots,
		'producer':producer,'director':director,'hero':hero,'heroin':heroin,
		'genre':genre[0].encode('UTF8'),'genr':genre[1].encode('UTF8'),
		'rate': ratin,'similar':similar,
        	}
	return render_template('movie.html', **kwargs)

if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 1341))
    app.run(host=host, port=port)
