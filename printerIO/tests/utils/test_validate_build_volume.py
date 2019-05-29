from django.test import TestCase
from printerIO.utils import validate_build_volume


class ValidateBuildVolumeWithATypoTest(TestCase):

    def setUp(self) -> None:
        self.util = validate_build_volume
        self.build_volume="300x30fx300"

    def test_if_validation_fails_due_to_a_typo(self):

        self.assertEquals(self.util(self.build_volume), False)


class ValideBuildVolumeWithNothingWrong(TestCase):
    def setUp(self) -> None:
        self.util = validate_build_volume
        self.build_volume = "300x300x300"

    def test_if_validation_passes(self):
        self.assertEquals(self.util(self.build_volume), True)


class ValidateBuildVolumeWithFourAxis(TestCase):

    def setUp(self) -> None:
        self.util = validate_build_volume
        self.build_volume = "30x300x300x300"

    def test_if_validation_fails_due_to_abnormal_amount_of_axis(self):
        self.assertEquals(self.util(self.build_volume), False)

class ValidateBuildVolumeWithTwoAxis(TestCase):

    def setUp(self) -> None:
        self.util = validate_build_volume
        self.build_volume = "300x300"

    def test_if_validation_fails_due_to_too_little_axises(self):
        self.assertEquals(self.util(self.build_volume), False)