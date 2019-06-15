import unittest
import base64


class TestAuth(unittest.TestCase):
    def setUp(self):
        pass

    def test_login(self):
        image_file = open('test.jpg', mode='rb')
        a = {'picture': base64.b64encode(image_file.read())}
        print(a)
        self.assertEqual(1, 1)  # TODO change

    def test_register(self):
        self.assertEqual(1, 1)  # TODO change
