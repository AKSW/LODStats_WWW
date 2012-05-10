from rdfstats.tests import *

class TestVocabulariesController(TestController):

    def test_index(self):
        response = self.app.get(url('vocabularies'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_vocabularies', format='xml'))

    def test_create(self):
        response = self.app.post(url('vocabularies'))

    def test_new(self):
        response = self.app.get(url('new_vocabulary'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_new_vocabulary', format='xml'))

    def test_update(self):
        response = self.app.put(url('vocabulary', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('vocabulary', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('vocabulary', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('vocabulary', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('vocabulary', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_vocabulary', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('edit_vocabulary', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_vocabulary', id=1, format='xml'))
