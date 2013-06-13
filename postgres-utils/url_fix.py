CREATE OR REPLACE FUNCTION url_fix(url text)
    RETURNS text
AS $$
import urllib
import urlparse

def url_fix(s, charset='utf-8'):

    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    reserved_characters = "!*();:@&=+$,?#[]'%"
    qs = urllib.quote_plus(qs, reserved_characters)
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

return url_fix(url)
$$ LANGUAGE plpythonu;

# SQL commands
ALTER TABLE rdfdoc ADD COLUMN uri_fixed;
UPDATE rdfdoc SET uri_fixed=url_fix(uri);
ALTER TABLE rdfdoc DROP COLUMN uri;
ALTER TABLE rdfdoc RENAME COLUMN uri_fixed TO uri;
