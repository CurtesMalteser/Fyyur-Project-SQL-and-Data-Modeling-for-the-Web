from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    shows = db.relationship('Show', back_populates='venues', lazy='joined')

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
    shows = db.relationship('Show', back_populates='artists', lazy='joined')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
   artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
   artists = db.relationship('Artist', back_populates='shows', lazy=True)
   venues = db.relationship('Venue', back_populates='shows', lazy=True)
   start_time = db.Column(db.DateTime, nullable=False)

class ShowUI:

    id : int
    venue_id : str
    artist_id : str
    artists : str
    artist_image_link: str
    venues: str
    venue_name : str
    venue_image_link: str
    start_time : str

    def __init__(self, show: Show):

        self.id = show.id
        self.venue_id = show.venue_id
        self.artist_id = show.artist_id
        self.artists = show.artists
        self.artist_name = show.artists.name
        self.artist_image_link = show.artists.image_link
        self.venues = show.venues
        self.venue_name = show.venues.name
        self.venue_image_link = show.venues.image_link
        self.start_time = show.start_time


class MapperShowUI:
    _shows : list[Show]

    def __init__(self, shows):
        self._shows = shows

    def past_upcoming_shows(self) -> (list[ShowUI], list[ShowUI]) :

        past_shows, upcoming_shows = [], []

        for show in self._shows:
            (past_shows if show.start_time < datetime.now() else upcoming_shows).append(show)

        past_shows = map(lambda show: ShowUI(show), past_shows)   
        upcoming_shows = map(lambda show: ShowUI(show), upcoming_shows)
        return (past_shows, upcoming_shows)

    def shows(self) -> list[ShowUI]:
        return map(lambda show: ShowUI(show), self._shows)


class ArtistUI:
    id: int
    name : str
    city : str
    state : str
    phone : str
    image_link : str
    facebook_link : str
    website : str
    seeking_venue : str
    seeking_description : str
    genres: list[str]
    past_shows : list[ShowUI]
    upcoming_shows : list[ShowUI]
    past_shows_count: int
    upcoming_shows_count: int

    def __init__(self, artist_data: Artist):

        (past_shows, upcoming_shows) = MapperShowUI(shows=artist_data.shows).past_upcoming_shows()

        past_shows = list(map(ShowUI, past_shows))
        upcoming_shows = list(map(ShowUI, upcoming_shows))

        self.id = artist_data.id
        self.name = artist_data.name
        self.city = artist_data.city
        self.state = artist_data.state
        self.phone = artist_data.phone
        self.genres = artist_data.genres
        self.image_link = artist_data.image_link
        self.facebook_link = artist_data.facebook_link
        self.website = artist_data.website_link
        self.seeking_venue = artist_data.seeking_venue
        self.seeking_description = artist_data.seeking_description
        self.past_shows = past_shows
        self.past_shows_count = len(past_shows)
        self.upcoming_shows = upcoming_shows
        self.upcoming_shows_count = len(upcoming_shows)


class VenueUI():

    id : int
    name : str
    city : str
    state : str
    address : str
    phone : str
    image_link : str
    facebook_link : str
    website : str
    genres : list[str]
    seeking_talent : bool
    seeking_description : str
    past_shows : list [ShowUI]
    upcoming_shows : list [ShowUI]
    past_shows_count: int
    upcoming_shows_count: int

    def __init__(self, venue_data: Venue):

        (past_shows, upcoming_shows) = MapperShowUI(shows=venue_data.shows).past_upcoming_shows()

        past_shows = list(map(ShowUI, past_shows))
        upcoming_shows = list(map(ShowUI, upcoming_shows))

        self.id = venue_data.id
        self.name = venue_data.name
        self.city = venue_data.city
        self.state = venue_data.state
        self.address = venue_data.address
        self.phone = venue_data.phone
        self.genres = venue_data.genres
        self.image_link = venue_data.image_link
        self.facebook_link = venue_data.facebook_link
        self.website = venue_data.website_link
        self.seeking_talent = venue_data.seeking_talent
        self.seeking_description = venue_data.seeking_description
        self.past_shows = past_shows
        self.past_shows_count = len(past_shows)
        self.upcoming_shows = upcoming_shows
        self.upcoming_shows_count = len(upcoming_shows)


class AreaUI():

    city: str
    state: str
    venues : list[VenueUI]

    def __init__(self, city: str, state: str, venues: list[Venue]):
        self.city = city
        self.state = state
        self.venues = map(lambda data: VenueUI(venue_data=data), venues)


class SearchData():
    id: int
    name: str
    num_upcoming_shows: int

    def __init__(self, id, name, num_upcoming_shows):
        self.id = id
        self.name = name
        self.num_upcoming_shows = num_upcoming_shows


class SearchUI():
    count: int
    data: list[VenueUI]

    def __init__(self, count, data):
        self.count = count
        self.data = data