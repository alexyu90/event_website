#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
Flask, render_template, request, Response, flash, redirect, url_for)
from flask_moment import Moment
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from itertools import groupby
from models import db, Venue, Artist, Show
# models are declared in a seperate file following separation of concerns.

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

# a helper function to load object into dictionary
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
    for c in inspect(obj).mapper.column_attrs}
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    locals = []
    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).all()

    for place in places:
        locals.append({
            'city': place.city,
            'state': place.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
            } for venue in venues if
                venue.city == place.city and venue.state == place.state]
        })
    return render_template('pages/venues.html', areas=locals)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term=request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
    response = {}
    response["count"] = len(venues)
    data = []
    for venue in venues:
        venue_dict = {}
        venue_dict["id"] = venue.id
        venue_dict["name"] = venue.name
        data.append(venue_dict)
    response["data"] = data
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
    venue = Venue.query.filter_by(id=venue_id).one()
    # basic info
    data = object_as_dict(venue)
    data["genres"] = venue.genres.replace("{","").replace("}", "").replace(",", " ").split()
    # show part
    def show_info_extract(query):
        show_list = []
        show_count = query.count()
        for show in query.all():
            artist_dict = {}
            start_time = show.start_time
            artist_dict['artist_id'] = show.artist_id
            artist_dict['artist_name'] = show.artist.name
            artist_dict['artist_image_link'] = show.artist.image_link
            artist_dict['start_time'] = str(start_time)
            show_list.append(artist_dict)
        return show_list, show_count

    past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<=datetime.now())
    past_shows, past_shows_count = show_info_extract(past_shows_query)
    upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now())
    upcoming_shows, upcoming_shows_count = show_info_extract(upcoming_shows_query)
    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows
    data["past_shows_count"] = past_shows_count
    data["upcoming_shows_count"] = upcoming_shows_count
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    try:
        venue = Venue()
        form.populate_obj(venue)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('Error! Venue ' + request.form['name'] + ' was not listed!')
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue_name = Venue.query.filter_by(id=venue_id).one().name
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue ' + venue_name + ' was successfully deleted!')
    except:
        db.session.rollback()
        flash('Error! Venue ' + venue_name + ' was not deleted!')
    finally:
        db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.order_by('id').all()
    data = []
    for artist in artists:
        artist_dict = {}
        artist_dict["id"] = artist.id
        artist_dict["name"] = artist.name
        data.append(artist_dict)
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
    response = {}
    response["count"] = len(artists)
    data = []
    for artist in artists:
        artist_dict = {}
        artist_dict["id"] = artist.id
        artist_dict["name"] = artist.name
        data.append(artist_dict)
    response["data"] = data
    return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).one()
    # basic info
    data = object_as_dict(artist)
    data["genres"] = artist.genres.replace("{","").replace("}", "").replace(",", " ").split()
    # show part
    def show_info_extract(query):
        show_list = []
        show_count = query.count()
        for show in query.all():
            venue_dict = {}
            start_time = show.start_time
            venue_dict['venue_id'] = show.venue_id
            venue_dict['venue_name'] = show.venue.name
            venue_dict['venue_image_link'] = show.venue.image_link
            venue_dict['start_time'] = str(start_time)
            show_list.append(venue_dict)
        return show_list, show_count

    past_shows_query = db.session.query(Show).join(Venue)\
                       .filter(Show.artist_id==artist_id)\
                       .filter(Show.start_time<=datetime.now())
    past_shows, past_shows_count = show_info_extract(past_shows_query)
    upcoming_shows_query = db.session.query(Show).join(Venue)\
                           .filter(Show.artist_id==artist_id)\
                           .filter(Show.start_time>datetime.now())
    upcoming_shows, upcoming_shows_count = show_info_extract(upcoming_shows_query)

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows
    data["past_shows_count"] = past_shows_count
    data["upcoming_shows_count"] = upcoming_shows_count
    return render_template('pages/show_artist.html', artist=data)

@app.route('/test')
def test():
    artist_id = 3
    artist = Artist.query.filter_by(id=artist_id).one()
    # basic info
    data = object_as_dict(artist)
    data["genres"] = artist.genres.replace("{","").replace("}", "").replace(",", " ").split()
    # show part
    def show_info_extract(query):
        show_list = []
        show_count = query.count()
        for show in query.all():
            venue_dict = {}
            start_time = show.start_time
            venue_dict['venue_id'] = show.venue_id
            venue_dict['venue_name'] = show.venue.name
            venue_dict['venue_image_link'] = show.venue.image_link
            venue_dict['start_time'] = str(start_time)
            show_list.append(venue_dict)
        return show_list, show_count

    past_shows_query = db.session.query(Show).join(Venue)\
                       .filter(Show.artist_id==artist_id)\
                       .filter(Show.start_time<=datetime.now())
    past_shows, past_shows_count = show_info_extract(past_shows_query)
    upcoming_shows_query = db.session.query(Show).join(Venue)\
                           .filter(Show.artist_id==artist_id)\
                           .filter(Show.start_time>datetime.now())
    upcoming_shows, upcoming_shows_count = show_info_extract(upcoming_shows_query)

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows
    data["past_shows_count"] = past_shows_count
    data["upcoming_shows_count"] = upcoming_shows_count
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
    form = ArtistForm(request.form)
    try:
        artist = Artist()
        form.populate_obj(artist)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('Error! Artist ' + request.form['name'] + ' was not listed!')
        print(sys.exc_info())
    finally:
        db.session.close()

    return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    artist_name = Artist.query.filter_by(id=artist_id).one().name
    try:
        artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
        flash('Artist ' + artist_name + ' was successfully deleted!')
    except:
        db.session.rollback()
        flash('Error! Artist ' + artist_name + ' was not deleted!')
    finally:
        db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a artist on a artist Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
 # displays list of shows at /shows
    shows = Show.query.all()
    data = []
    for show in shows:
        show_dict = {}
        show_dict["venue_id"] = show.venue_id
        show_dict["venue_name"] = show.venue.name
        show_dict["artist_id"] = show.artist_id
        show_dict["artist_name"] = show.artist.name
        show_dict["artist_image_link"] = show.artist.image_link
        show_dict["start_time"] = str(show.start_time)
        data.append(show_dict)

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        show = Show(artist_id=artist_id, venue_id=venue_id,
                      start_time=start_time)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('Error! Show was not listed!')
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(400)
def not_found_error(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def not_found_error(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
