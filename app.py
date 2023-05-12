from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
from datetime import datetime
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__, static_url_path='/static')


# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
 
# Settings for migrations
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()


class Moview(db.Model):
    # Id : Field which stores unique id for every row in
    # database table.
    # movie_name: Used to store the name of movie
    # imdb_id: Used to store the IMDB_ID of movie
    # release_date: Used to store the date of release of movie
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(200), unique=False, nullable=False)
    imdb_id = db.Column(db.String(20), unique=False, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return self.movie_name
    

@app.route('/')
def index():
      # Query all data and then pass it to the template
    profiles = Moview.query.all()[:100]
    return render_template('index.html', profiles=profiles,spinner_url=url_for('static', filename='images/loading.gif'))


@app.route('/add_movie')
def movieadd():
    # set up the endpoint URL and the query
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """
    SELECT DISTINCT ?imdb_id (MIN(?pubdate) AS ?min_pubdate) ?itemLabel WHERE {
    ?item wdt:P31 wd:Q11424.
    ?item wdt:P577 ?pubdate.
    ?item wdt:P345 ?imdb_id.
    FILTER((?pubdate >= "2013-01-01T00:00:00Z"^^xsd:dateTime) && (STRSTARTS(STR(?imdb_id), "tt")))
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    GROUP BY ?imdb_id ?itemLabel

    """

    # create a SPARQLWrapper instance and set the query and endpoint URL
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)

    # set the return format to JSON
    sparql.setReturnFormat(JSON)

    # execute the query and convert the results to a Python object
    results = sparql.query().convert()
    db.session.query(Moview).delete()
    db.session.commit()
    movie_list = []
    for result in tqdm(results["results"]["bindings"]):
        p=Moview(movie_name=result["itemLabel"]["value"], imdb_id=result["imdb_id"]["value"], release_date=datetime.strptime(result["min_pubdate"]["value"].split("T")[0], '%Y-%m-%d'))
        movie_list.append(p)
        db.session.commit()
    # perform bulk operation to create objects of movie
    db.session.bulk_save_objects(movie_list)
    db.session.commit()
    return redirect('/')