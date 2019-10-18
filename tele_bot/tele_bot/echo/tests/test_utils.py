from unittest import TestCase

from echo.utils import get_filename


class UtilsTestCase(TestCase):

    def test_filename_prefix(self):
        r = get_filename()
        self.assertTrue(r.startswith("result_"))

    def test_filename_postfix(self):
        r = get_filename()
        self.assertTrue(r.endswith(".png"))

    def test_filename_structure(self):
        r = get_filename()
        self.assertEqual(len(r.split("_")), 3)
