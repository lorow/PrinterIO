from printers.utils import validate_build_volume
import pytest

pytestmark = pytest.mark.django_db


class TestValidateBuildVolume:
    def test_fail_provided_with_no_volume(self):
        """ should raise ValueError due to no volume being provided """

        with pytest.raises(ValueError):
            validate_build_volume(None)

    def test_validate_build_volume_for_unknow_type(self):
        """ Should fail due being provied an unsupported printer type  """
        with pytest.raises(ValueError):
            validate_build_volume("127x127x127x", "SLS")

    def test_validate_build_volume_fail_with_NaN_dim(self):
        """ Should return False due to 'lol' being the second dimension """
        assert not validate_build_volume("200xlolx300", "CR")

    @pytest.mark.parametrize(
        "printer_type,build_volume",
        [("CR", "200x200"), ("DL", "200x200x200"), ("RS", "200x200"),],
    )
    def test_validate_with_unmatched_dimensions(self, printer_type, build_volume):
        """ should return False for every combination """
        assert not validate_build_volume(build_volume, printer_type)

    @pytest.mark.parametrize(
        "printer_type,build_volume",
        [("CR", "20fx200"), ("DL", "200x20ax200"), ("RS", "200x2y0"),],
    )
    def test_validate_volume_with_type(self, printer_type, build_volume):
        """ Should return False due to typo """
        assert not validate_build_volume(build_volume, printer_type)

    @pytest.mark.parametrize(
        "printer_type,build_volume",
        [("CR", "200x200x200"), ("DL", "200x200"), ("RS", "200x200x200"),],
    )
    def test_validate_volume_proper(self, printer_type, build_volume):
        """ Should return True """
        assert validate_build_volume(build_volume, printer_type)
