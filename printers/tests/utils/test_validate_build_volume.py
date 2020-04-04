from django.test import TestCase
from printers.utils import validate_build_volume
import pytest
pytestmark = pytest.mark.django_db


class ValidateBuildVolumeTests(TestCase):

    def setUp(self) -> None:
        self.service = validate_build_volume

    def test_validating_proper_build_volume(self):

        self.assertTrue(self.service("30x30x30"))

    def test_validating_build_volume_with_a_typo(self):

        self.assertFalse(self.service("30x3fx30"))

    def test_validating_empty_build_volume(self):

        with self.assertRaises(ValueError):
            self.service("")

    def test_validating_four_axis_build_volume(self):

        self.assertFalse(self.service("300x300x300x300"))

    def test_validating_two_axis_build_volume(self):

        self.assertFalse(self.service("300x300"))
