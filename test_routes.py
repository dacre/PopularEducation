import unittest
import routes


class TestStringMethods(unittest.TestCase):

    def test_routes(self):
        print(routes.hello_world())
    #self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
