
UPDATE artists set artist_letter = replace(rtrim(url, replace(url, '/', '')), '/', '');

