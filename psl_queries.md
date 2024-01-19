## SELECT 'all' ##
* SELECT * FROM "Artist";
* SELECT * FROM "Venue";
* SELECT * FROM shows;

## INSERT Venue ##
INSERT INTO "Venue"(name, city, state, address, phone, image_link, facebook_link, genres, seeking_talent, seeking_description, website_link)
VALUES('The Musical Hop',
    'San Francisco',
    'CA',
    '1015 Folsom Street',
    '123-123-1234',
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    'https://www.facebook.com/TheMusicalHop',
    '{"Jazz", "Reggae", "Swing", "Classical", "Folk"}',
    1,
    'We are on the lookout for a local artist to play every two weeks. Please call us.',
    'https://www.themusicalhop.com'
);

## DELETE ##
DELETE FROM "Venue" WHERE id=4;