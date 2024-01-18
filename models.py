from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
    website_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(24)))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', back_populates='venues', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', back_populates='artists', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
   artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
   artists = db.relationship('Artist', back_populates='shows', lazy=True)
   venues = db.relationship('Venue', back_populates='shows', lazy=True)
   start_time = db.Column(db.DateTime, nullable=False)


class ArtistUI(Artist):
    past_shows : list[Show]
    upcoming_shows : list[Show]
    past_shows_count: int
    upcoming_shows_count: int

    def __init__(self, artist_data):
        self.name = artist_data.name
        self.city = artist_data.city
        self.state = artist_data.state
        self.phone = artist_data.phone
        self.genres = artist_data.genres
        self.image_link = artist_data.image_link
        self.facebook_link = artist_data.facebook_link
        self.website_link = artist_data.website_link
        self.seeking_venue = artist_data.seeking_venue
        self.seeking_description = artist_data.seeking_description
        self.shows = artist_data.shows
        self.past_shows = []
        self.upcoming_shows = []
        self.past_shows_count = 0
        self.upcoming_shows_count = 0