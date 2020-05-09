from printerIO.utils import flatten_list
import pytest

pytestmark = pytest.mark.django_db


class TesttFlattenList:
    def test_flatten_double_list(self):
        assert flatten_list([[1, 2, 3]]) == [1, 2, 3]

    def test_flatten_n_list(self):
        assert flatten_list([[1, 2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]

    def test_fail_flatten_list(self):
        """Should fail due to additional item not being a list"""

        with pytest.raises(TypeError):
            flatten_list([[1, 2], 3])
