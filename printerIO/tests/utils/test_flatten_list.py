from django.test import TestCase
from printerIO.utils import flatten_list


class FlattenListTests(TestCase):

    def setUp(self) -> None:
        self.util = flatten_list

    def test_flattening_of_double_list(self):
        self.assertEqual(self.util([[1, 2, 3]]), [1, 2, 3])

    def test_flattening_of_two_lists_in_one_double(self):
        self.assertEqual(self.util([[1, 2, 3], [4, 5, 6]]), [1, 2, 3, 4, 5, 6])

    def test_flattening_of_double_list_with_additional_value_raises_type_error(self):

        with self.assertRaises(TypeError):
            self.util([[1, 2], 3])
