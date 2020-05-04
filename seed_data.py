
#----------------------------------------------------------------------------#
# Seed Data into Database
#----------------------------------------------------------------------------#

from app import db, Venue, Artist, Show, Genre

#  Reset Tables
#  ----------------------------------------------------------------

db.session.execute('DELETE FROM "VenueGenre";')
db.session.execute('DELETE FROM "ArtistGenre";')
Show.query.delete()
Venue.query.delete()
Artist.query.delete()
Genre.query.delete()
db.session.execute('ALTER SEQUENCE "Venue_id_seq" RESTART WITH 1;')
db.session.execute('ALTER SEQUENCE "Artist_id_seq" RESTART WITH 7;')
db.session.execute('ALTER SEQUENCE "Show_id_seq" RESTART WITH 1;')
db.session.commit()

#  Venues
#  ----------------------------------------------------------------

venues = (
  {"name": "The Musical Hop", "address": "1015 Folsom Street", "city": "San Francisco", "state": "CA", "phone": "123-123-1234", "website": "https://www.themusicalhop.com",  "facebook_link": "https://www.facebook.com/TheMusicalHop", "seeking_talent": True, "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.", "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60" },
  {"name": "The Dueling Pianos Bar", "address": "335 Delancey Street", "city": "New York", "state": "NY", "phone": "914-003-1132", "website": "https://www.theduelingpianos.com", "facebook_link": "https://www.facebook.com/theduelingpianos", "seeking_talent": False, "seeking_description": None, "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80" },
  {"name": "Park Square Live Music & Coffee", "address": "34 Whiskey Moore Ave", "city": "San Francisco", "state": "CA", "phone": "415-000-1234", "website": "https://www.parksquarelivemusicandcoffee.com", "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee", "seeking_talent": False, "seeking_description": None, "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80" }
)

for v in venues:
  venue = Venue(**v)
  db.session.add(venue)

#  Artists
#  ----------------------------------------------------------------

artists = (
  { "id": 4, "name": "Guns N Petals", "city": "San Francisco", "state": "CA", "phone": "326-123-5000", "website": "https://www.gunsnpetalsband.com", "facebook_link": "https://www.facebook.com/GunsNPetals", "seeking_venue": True, "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!", "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80" },
  { "id": 5, "name": "Matt Quevedo", "city": "New York", "state": "NY", "phone": "300-400-5000", "website": None, "facebook_link": "https://www.facebook.com/mattquevedo923251523", "seeking_venue": False, "seeking_description": None, "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80" },
  { "id": 6, "name": "The Wild Sax Band", "city": "San Francisco", "state": "CA", "phone": "432-325-5432", "website": None, "facebook_link": None, "seeking_venue": False, "seeking_description": None, "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80" }
)

for a in artists:
  artist = Artist(**a)
  db.session.add(artist)

#  Shows
#  ----------------------------------------------------------------

shows = (
  {"venue_id": 1, "artist_id": 4, "start_time": "2019-05-21T21:30:00.000Z" },
  {"venue_id": 3, "artist_id": 5, "start_time": "2019-06-15T23:00:00.000Z" },
  {"venue_id": 3, "artist_id": 6, "start_time": "2035-04-01T20:00:00.000Z" },
  {"venue_id": 3, "artist_id": 6, "start_time": "2035-04-08T20:00:00.000Z" },
  {"venue_id": 3, "artist_id": 6, "start_time": "2035-04-15T20:00:00.000Z" }
)

for s in shows:
  show = Show(**s)
  db.session.add(show)

#  Genres
#  ----------------------------------------------------------------

genres = (
  { "genre": "Alternative" },
  { "genre": "Blues" },
  { "genre": "Classical" },
  { "genre": "Country" },
  { "genre": "Electronic" },
  { "genre": "Folk" },
  { "genre": "Funk" },
  { "genre": "Hip-Hop" },
  { "genre": "Heavy Metal" },
  { "genre": "Instrumental" },
  { "genre": "Jazz" },
  { "genre": "Musical Theatre" },
  { "genre": "Pop" },
  { "genre": "Punk" },
  { "genre": "R&B" },
  { "genre": "Reggae" },
  { "genre": "Rock n Roll" },
  { "genre": "Soul" },
  { "genre": "Swing" },
  { "genre": "Other" }
)

for g in genres:
  genre = Genre(**g)
  db.session.add(genre)

#  Genre Association Tables
#  ----------------------------------------------------------------

db_genres = Genre.query.all()
genre_dictionary = {}

for g in db_genres:
  genre_dictionary[g.genre] = g

def get_genre_list(genre_str_list):
  genre_list = []
  for genre_str in genre_str_list:
    genre = genre_dictionary[genre_str]
    genre_list.append(genre)
  return genre_list

venues = Venue.query.all()

venues[0].genres = get_genre_list(["Jazz", "Reggae", "Swing", "Classical", "Folk"])
venues[1].genres = get_genre_list(["Classical", "R&B", "Hip-Hop"])
venues[2].genres = get_genre_list(["Rock n Roll", "Jazz", "Classical", "Folk"])

artists = Artist.query.all()

artists[0].genres = get_genre_list(["Rock n Roll"])
artists[1].genres = get_genre_list(["Jazz"])
artists[2].genres = get_genre_list(["Jazz", "Classical"])

db.session.commit()
db.session.close()
