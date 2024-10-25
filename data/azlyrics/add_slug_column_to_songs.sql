ALTER TABLE songs ADD COLUMN slug STRING;

UPDATE songs SET slug = replace(replace(url, rtrim(url, replace(url, '/', '')), ''), '.html', '');

CREATE TABLE songs_copy(
	title,
	slug,
	artist,
	url,
	status,
	primary key (slug, artist),
	foreign key (artist) references artists(slug));

INSERT INTO songs_copy (title, slug, artist, url, status)
SELECT title, slug, artist, url, status FROM songs;
DROP TABLE songs;
ALTER TABLE songs_copy RENAME To songs;
