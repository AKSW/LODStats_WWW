from rdfstats.tests import *

class TestSearchController(TestController):

    def test_index(self):
        response = self.app.get(url('property_search'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_property_search', format='xml'))

    def test_create(self):
        response = self.app.post(url('property_search'))

    def test_new(self):
        response = self.app.get(url('property_new_searchone'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_property_new_searchone', format='xml'))

    def test_update(self):
        response = self.app.put(url('property_searchone', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('property_searchone', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('property_searchone', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('property_searchone', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('property_searchone', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_property_searchone', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('property_edit_searchone', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_property_edit_searchone', id=1, format='xml'))
