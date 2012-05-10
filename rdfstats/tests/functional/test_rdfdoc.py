from rdfstats.tests import *

class TestRdfdocController(TestController):

    def test_index(self):
        response = self.app.get(url('rdfdoc'))
        # Test response...
