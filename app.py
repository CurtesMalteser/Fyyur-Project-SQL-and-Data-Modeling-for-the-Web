#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
import logging
from flask import (
  Flask,
  render_template,
  request,
  flash,
  redirect,
  url_for,
  abort
  )
from flask_moment import Moment
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date : datetime
  
  if isinstance(value, str):
     date = dateutil.parser.parse(value)
  else:
     date = value

  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data: list[AreaUI] = []

  def get_venues_by_city(city):
    return Venue.query.filter_by(city=city).order_by('id').all()

  try:
    areas = Venue.query.with_entities(Venue.city, Venue.state).distinct(Venue.city).all()

    data = map(lambda area: AreaUI(city= area.city, state= area.state, venues = get_venues_by_city(area.city)), areas)

  except:
    flash('Some error ocurred while fetching veues.', 'error')

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search = request.form.get('search_term')

  response = SearchUI(count=0, data=[])

  try:
    response = Venue.query.filter(Venue.name.ilike('%{}%'.format(search)))
    response = data_to_search_ui(response)
  except Exception as e:
    flash('Some error ocurred while searching results for {}.'.format(e), 'error')

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  try:
    data = Venue.query.get(venue_id)
    data = VenueUI(venue_data=data)
    return render_template('pages/show_venue.html', venue=data)
  except:
    flash('Some error ocurred while fetching venue with id {}.'.format(venue_id))
    return render_template('pages/home.html')

 
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
    venue = Venue(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website_link = request.form['website_link'],
      seeking_talent = bool(request.form.get("seeking_talent", False)),
      seeking_description = request.form['seeking_description']
      )

    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue was successfully listed!'.format(request.form['name']))
  except:
     # TODO: on unsuccessful db insert, flash an error instead.
     # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
     db.session.rollback()
     flash('An error occurred. Venue {} could not be listed.'.format(request.form['name']), 'error')
  finally:
     db.session.close() 

   # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venue : Venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    
  except Exception as e:
    db.session.rollback()
    error = True

  finally:
    db.session.close()

  if error:
        abort(500)
  else:
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists', methods=['GET'])
def artists():
  # TODO: replace with real data returned from querying the database
  try:
     artists = Artist.query.with_entities(Artist.id, Artist.name).all()
     return render_template('pages/artists.html', artists=artists)
  except:
     flash('Some error ocurred while fetching artists.')
     return render_template('pages/artists.html', artists=[])

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search = request.form.get('search_term')

  response = SearchUI(count=0, data=[])

  try:
    response = Artist.query.filter(Artist.name.ilike('%{}%'.format(search)))
  
    response = data_to_search_ui(response)
  except:
    flash('Some error ocurred while searching results for {}.'.format(search), 'error')

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  try:
    artist = Artist.query.get(artist_id)
    artist_ui = ArtistUI(artist_data=artist)
    return render_template('pages/show_artist.html', artist=artist_ui)
  except:
     flash('Some error ocurred while fetching artist with id {}.'.format(artist_id))
     return render_template('pages/home.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  try:
    artist = Artist.query.get(artist_id)
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

    return render_template('forms/edit_artist.html', form=form, artist=artist)
  except:
     flash('Some error ocurred while fetching artist with id {}.'.format(artist_id), 'error')
     return render_template('forms/edit_artist.html', form=form)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website_link = request.form['website_link']
    artist.seeking_venue = bool(request.form.get("seeking_venue", False))
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
     db.session.rollback()
     flash('An error occurred. Artist {} could not be updated.'.format(request.form['name']), 'error')
  finally:
     db.session.close() 

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  try:
    venue = Venue.query.get(venue_id)
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link
    return render_template('forms/edit_venue.html', form=form, venue=venue)
  except:
    flash('Some error ocurred while fetching veue with id {}.'.format(venue_id), 'error')
    return render_template('forms/edit_venue.html', form=form)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website_link = request.form['website_link']
    venue.seeking_talent = bool(request.form.get("seeking_talent", False))
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()
  except Exception as e:
     db.session.rollback()
     flash('An error occurred. Venue {} could not be update.'.format(request.form['name']), 'error')
  finally:
     db.session.close()

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
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    artist = Artist(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website_link = request.form['website_link'],
      seeking_venue = bool(request.form.get("seeking_venue", False)),
      seeking_description = request.form['seeking_description']
      )

    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist {} was successfully listed!'.format(request.form['name']))
  except:
     # TODO: on unsuccessful db insert, flash an error instead.
     # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
     db.session.rollback()
     flash('An error occurred. Artist {} could not be listed.'.format(request.form['name']), 'error')
  finally:
     db.session.close() 

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]
  try:
    shows = Show.query.all()
    data = MapperShowUI(shows=shows).shows()
  except:
    flash('Some error ocurred while fetching artists.')

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
     show = Show(
        venue_id = request.form['venue_id'],
        artist_id = request.form['artist_id'],
        start_time = request.form['start_time']
        )
     db.session.add(show)
     db.session.commit()
    # on successful db insert, flash success
     flash('Show was successfully listed!')
        
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    db.session.rollback()
    flash('An error occurred while saving the show.', 'error')
  finally:
    db.session.close()

  return render_template('pages/home.html')

#  Utils
#  ----------------------------------------------------------------

# takes Arstist and Venue data as input,
# returns SearchUI,
# since the html files expect same data
def data_to_search_ui(data):
    data = map(lambda venue: SearchData(
      id= venue.id,
      name= venue.name,
      num_upcoming_shows= len(list(filter(lambda show: show.start_time > datetime.now(),venue.shows)))
    ) , data)

    data = list(data)

    return SearchUI(
      count = len(data),
      data= data
    )

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
