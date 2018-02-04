import unittest

import routes


class TestStringMethods(unittest.TestCase):

    def test_routes(self):
        events = routes.get_events()
        for event in events:
            print(event)
    #self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
