"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.resource('rdf_class', 'rdf_classes')
    map.resource('property', 'properties')
    map.resource('vocabulary', 'vocabularies')
    map.resource('datatype', 'datatypes')
    map.resource('link', 'links')
    map.resource('language', 'languages')
    map.resource('stat_result', 'stat_result')
    map.resource('dataset', 'datasets')
    map.resource('searchone', 'search', controller='property/search',
                 path_prefix='/property', name_prefix='property_')
    map.connect('/datasets/*id', controller='datasets', action='show')
    map.connect('/vocab/search/*id', controller='vocab/search', action='show')
    map.connect('/property/search/*query', controller='property/search', action='show')
    map.connect('/', controller='homepage', action='home')
    map.connect('/stats', controller='homepage', action='stats')
    map.connect('/rdfdocs/void', controller='rdfdocs', action='void')
    map.resource('rdfdoc', 'rdfdocs')
    map.connect('/rdfdocs/', controller='rdfdocs', action='index')
    # enable routes for bookmarks for older LODStats versions
    map.connect('/rdfdoc/', controller='rdfdocs', action='index')
    map.connect('/rdfdoc', controller='rdfdocs', action='index')
    map.connect('/rdfdoc/view/{id}', controller='rdfdocs', action='show')
    map.connect('/rdfdoc/valid_and_available', controller='rdfdocs', action='valid_and_available')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
