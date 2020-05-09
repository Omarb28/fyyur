#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os, sys, json
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from pprint import PrettyPrinter
import bleach

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
pprint = PrettyPrinter()

# DONE: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#  Association Tables
#  ----------------------------------------------------------------

venue_genres = db.Table('VenueGenre',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre', db.String(120), db.ForeignKey('Genre.genre'), primary_key=True)
)

artist_genres = db.Table('ArtistGenre',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre', db.String(120), db.ForeignKey('Genre.genre'), primary_key=True)
)

#  Models
#  ----------------------------------------------------------------

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(240))

    # backref foreign keys
    shows = db.relationship('Show', backref=db.backref('venue'), lazy=True, cascade='all, delete-orphan')
    genres = db.relationship('Genre', secondary=venue_genres, backref=db.backref('venues'), lazy=True)

    # bonus challenge (list by most recent)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(240))

    # backref foreign keys
    shows = db.relationship('Show', backref=db.backref('artist'), lazy=True, cascade='all, delete-orphan')
    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('artists'), lazy=True)

    # bonus challenge (list by most recent)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# one-to-many relationship between (Parent->Show) and (Artist->Show)
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # foreign keys
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    

# many-to-many relationship between (Parent-Genre) and (Artist-Genre) with Association Tables included above
class Genre(db.Model):
    __tablename__ = 'Genre'

    genre = db.Column(db.String(120), primary_key=True)

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

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():

  # get 10 most recent
  venues = Venue.query.order_by(db.desc('created_at')).limit(10).all()
  artists = Artist.query.order_by(db.desc('created_at')).limit(10).all()

  now = datetime.utcnow()

  data = {
    "venues": venues,
    "artists": artists
  }

  return render_template('pages/home.html', data=data, now=now)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  '''
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  '''
  venues = Venue.query.all()
  
  # dictionary of unique cities
  # keys are city names and values are the index of the city in the data
  cities = {}
  data = []

  for v in venues:
    if v.city not in cities.keys():
      cities[v.city] = len(data) # assign index of city
      city_data = {
        "city": v.city,
        "state": v.state,
        "venues": []
      }
      data.append(city_data)

    venue_data = {
      "id": v.id,
      "name": v.name,
    }
    data_index = cities[v.city]
    data[data_index]['venues'].append(venue_data)
  
  return render_template('pages/venues.html', areas=data);

#  Get Venue by ID
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  '''
  data1={
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
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  '''
  venue = Venue.query.get(venue_id)
  if venue is None:
    abort(404)
  
  past_shows = []
  upcoming_shows = []

  for show in venue.shows:
    artist = show.artist

    show_data = {
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.isoformat(sep='T')[:-3] + 'Z' 
    }

    if show.start_time >= datetime.utcnow():
      upcoming_shows.append(show_data)
    else:
      past_shows.append(show_data)

  genres = []
  for g in venue.genres:
    genres.append(g.genre)

  venue_data = {
    "id": venue.id,
    "name": venue.name,
    "genres": genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  button_links = {
    "edit": url_for('edit_venue', venue_id=venue_id),
    "delete": url_for('delete_venue', venue_id=venue_id)
  }

  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=venue_data, button_links=button_links)

#  Search Venue
#  ----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  '''
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  '''
  response = {}

  search_term = bleach.clean(request.form.get('search_term', ''))
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()

  data = []
  for venue in venues:
    num_upcoming_shows = 0
    for show in venue.shows:
      if show.start_time >= datetime.utcnow():
        num_upcoming_shows += 1

    venue_data = {
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_upcoming_shows
    }
    data.append(venue_data)
  
  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  error = False
  venue_id = 0
  try:
    req = request.form
    form = VenueForm(req)

    if not form.validate_on_submit():
      flash('An error occurred. Venue "' + req.get('name') + '" could not be listed.', 'error')
      return render_template('forms/new_venue.html', form=form)

    genres_str = req.getlist('genres')
    genres = []

    for g in genres_str:
      genre = Genre.query.filter(Genre.genre == g).first()
      genres.append(genre)
    
    seeking_talent = False
    if req.get('seeking_talent') == 'True':
      seeking_talent = True

    venue = Venue(
      name = req.get('name'),
      genres = genres,
      address = req.get('address'),
      city = req.get('city'),
      state = req.get('state'),
      phone = req.get('phone'),
      website = req.get("website"),
      facebook_link = req.get('facebook_link'),
      image_link = req.get('image_link'),
      seeking_talent = seeking_talent,
      seeking_description = req.get('seeking_descriptio')
    )

    db.session.add(venue)
    db.session.commit()

    # find id of venue after creation to redirect url to it
    venue_id = venue.id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  if error:
    flash('An error occurred. Venue "' + request.form.get('name') + '" could not be listed.', 'error')
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)
  else:
    flash('Venue "' + request.form.get('name') + '" was successfully listed!')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Update Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # DONE: populate form with values from venue with ID <venue_id>
  form = VenueForm()

  venue = Venue.query.get(venue_id)
  if venue is None:
    abort(404)

  genres = [g.genre for g in venue.genres]

  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue, genres=genres)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.get(venue_id)
    req = request.form
    form = VenueForm(req)

    genres_str = req.getlist('genres')
    genres = []

    for g in genres_str:
      genre = Genre.query.filter(Genre.genre == g).first()
      genres.append(genre)

    seeking_talent = False
    if req.get('seeking_talent') == 'True':
      seeking_talent = True
    
    venue.name = req.get('name')
    venue.genres = genres
    venue.address = req.get('address')
    venue.city = req.get('city')
    venue.state = req.get('state')
    venue.phone = req.get('phone')
    venue.website = req.get('website')
    venue.facebook_link = req.get('facebook_link')
    venue.image_link = req.get('image_link')
    venue.seeking_talent = seeking_talent
    venue.seeking_description= req.get('seeking_description')

    if not form.validate_on_submit():
      flash('An error occurred. Venue "' + req.get('name') + '" could not be updated.', 'error')
      return render_template('forms/edit_venue.html', form=form, venue=venue, genres=genres)

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Venue "' + request.form.get('name') + '" could not be updated.', 'error')
    form = VenueForm()
    return redirect(url_for('edit_venue', venue_id=venue_id))
  else:
    flash('Venue "' + request.form.get('name') + '" was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Delete Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # called upon submitting the new venue listing form
  
  # BONUS CHALLENGE (DONE): Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  venue_name = '(not found)'
  try:
    venue = Venue.query.get(venue_id)
    venue_name = venue.name
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Venue "' + venue_name + '" could not be deleted.', 'error')
  else:
    flash('Venue "' + venue_name + '" was successfully deleted.')
  
  return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  '''
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  '''
  artists = Artist.query.all()
  data = []
  for a in artists:
    artist_data = {
      "id": a.id,
      "name": a.name,
      "image_link": a.image_link,
      "shows": len(a.shows)
    }
    data.append(artist_data)

  return render_template('pages/artists.html', artists=data)

#  Get Artist by ID
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  '''
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  '''
  artist = Artist.query.get(artist_id)
  if artist is None:
    abort(404)

  past_shows = []
  upcoming_shows = []

  shows = Show.query.filter(Show.artist_id == artist.id).all()

  for show in shows:
    venue = show.venue

    show_data = {
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time.isoformat(sep='T')[:-3] + 'Z' 
    }

    if show.start_time >= datetime.utcnow():
      upcoming_shows.append(show_data)
    else:
      past_shows.append(show_data)

  genres = []
  for g in artist.genres:
    genres.append(g.genre)

  artist_data = {
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  button_links = {
    "edit": url_for('edit_artist', artist_id=artist_id),
    "delete": url_for('delete_artist', artist_id=artist_id)
  }
  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=artist_data, button_links=button_links)

#  Search Artist
#  ----------------------------------------------------------------

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  '''
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  '''
  response = {}

  search_term = bleach.clean(request.form.get('search_term', ''))
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()

  data = []
  for artist in artists:
    num_upcoming_shows = 0
    for show in artist.shows:
      if show.start_time >= datetime.utcnow():
        num_upcoming_shows += 1

    artist_data = {
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_shows
    }
    data.append(artist_data)
  
  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  artist_id = 0
  try:
    req = request.form
    form = ArtistForm(req)

    if not form.validate_on_submit():
      flash('An error occurred. Artist "' + req.get('name') + '" could not be listed.', 'error')
      return render_template('forms/new_artist.html', form=form)

    genres_str = req.getlist('genres')
    genres = []

    for g in genres_str:
      genre = Genre.query.filter(Genre.genre == g).first()
      genres.append(genre)
    
    seeking_venue = False
    if req.get('seeking_venue') == 'True':
      seeking_venue = True
    
    artist = Artist(
      name = req['name'],
      genres = genres,
      city = req.get('city'),
      state = req.get('state'),
      phone = req.get('phone'),
      website = req.get('website'),
      facebook_link = req.get('facebook_link'),
      image_link = req.get('facebook_link'),
      seeking_venue = seeking_venue,
      seeking_description = req.get('seeking_description'),
    )

    db.session.add(artist)
    db.session.commit()

    # find id of artist after creation to redirect url to it
    artist_id = artist.id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  if error:
    flash('An error occurred. Artist "' + request.form.get('name') + '" could not be listed.', 'error')
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)
  else:
    flash('Artist "' + request.form.get('name') + '" was succ"essfully listed!')
    return redirect(url_for('show_artist', artist_id=artist_id))



#  Update Artist
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # DONE: populate form with fields from artist with ID <artist_id>
  form = ArtistForm()

  artist = Artist.query.get(artist_id)
  if artist is None:
    abort(404)

  genres = [g.genre for g in artist.genres]

  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist, genres=genres)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artist = Artist.query.get(artist_id)
    req = request.form
    form = ArtistForm(req)

    genres_str = req.getlist('genres')
    genres = []

    for g in genres_str:
      genre = Genre.query.filter(Genre.genre == g).first()
      genres.append(genre)
    
    seeking_venue = False
    if req.get('seeking_venue') == 'True':
      seeking_venue = True

    seeking_description = req.get('seeking_description')
    if seeking_description is None:
      seeking_description = artist.seeking_description

    artist.name = req.get('name')
    artist.genres = genres
    artist.city = req.get('city')
    artist.state = req.get('state')
    artist.phone = req.get('phone')
    artist.website = req.get('website')
    artist.facebook_link = req.get('facebook_link')
    artist.image_link = req.get('image_link')
    artist.seeking_venue = seeking_venue
    artist.seeking_description= seeking_description

    if not form.validate_on_submit():
      flash('An error occurred. Artist "' + req.get('name') + '" could not be updated.', 'error')
      return render_template('forms/edit_artist.html', form=form, artist=artist, genres=genres)

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Artist "' + request.form.get('name') + '" could not be updated.', 'error')
    form = ArtistForm()
    return render_template('forms/edit_artist.html', form=form)
  else:
    flash('Artist "' + request.form.get('name') + '" was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

#  Delete Artist
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  error = False
  artist_name = '(not found)'
  try:
    artist = Artist.query.get(artist_id)
    artist_name = artist.name
    db.session.delete(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Artist "' + artist_name + '" could not be deleted.', 'error')
  else:
    flash('Artist "' + artist_name + '" was successfully deleted.')
  
  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  '''
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }]
  '''
  shows = Show.query.all()
  data = []
  
  for show in shows:
    venue = show.venue;
    artist = show.artist;
    show_data = {
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.isoformat(sep='T')[:-3] + 'Z' 
    }
    data.append(show_data)
  
  return render_template('pages/shows.html', shows=data)

#  Search Show
#  ----------------------------------------------------------------

@app.route('/shows/search', methods=['POST'])
def search_shows():
  response = {}
  
  search_term = bleach.clean(request.form.get('search_term', ''))
  #shows = db.session.query(Show, Artist).join(Artist).filter(Artist.name.ilike('%' + search_term + '%')).all()
  shows = db.session.query(Show, Artist, Venue).join(Artist).join(Venue).filter(db.or_(Venue.name.ilike('%' + search_term + '%'),
                                                                                        Artist.name.ilike('%' + search_term + '%'))).all()

  data = []
  for show, artist, venue in shows:
    show_data = {
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.isoformat(sep='T')[:-3] + 'Z'
    }
    data.append(show_data)
  
  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/show.html', results=response, search_term=search_term)

#  Create Show
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
  # renders form.
  form = ShowForm()

  artists = Artist.query.order_by('id').all()
  artist_choices = []
  for a in artists:
    artist_name = str(a.id) + ' - ' + a.name
    choice = (a.id, artist_name)
    artist_choices.append(choice)

  venues = Venue.query.order_by('id').all()
  venue_choices = []
  for v in venues:
    venue_name = str(v.id) + ' - ' + v.name
    choice = (v.id, venue_name)
    venue_choices.append(choice)

  form.artist_id.choices = artist_choices
  form.venue_id.choices = venue_choices

  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  error = False
  try:
    req = request.form

    artist = Artist.query.get(req.get('artist_id'))
    if artist is None:
      raise Exception('Artist with id %s not found.' % req.get('artist_id'))
    
    venue = Venue.query.get(req.get('venue_id'))
    if venue is None:
      raise Exception('Venue with id %s not found.' % req.get('venue_id'))

    show = Show(
      artist_id = req.get('artist_id'),
      venue_id = req.get('venue_id'),
      start_time = req.get('start_time')
    )
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  if error:
    flash('An error occurred. Show could not be listed.', 'error')
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)
  else:
    flash('Show was succwas successfully listed!')
    return redirect(url_for('shows'))


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
'''
if __name__ == '__main__':
    app.run()
'''

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

