"""
WARNING: These tests make real API calls and may be slow.
If you experience timeouts, check your network connection or try again later.

Note: To see the test session notice, run pytest with the `-s` flag:
    poetry run pytest -s
"""

import pytest

from hubeau_py.client import HubeauClient


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print(
        "\n[INFO] These tests make real API calls and may be slow. "
        "If you experience timeouts, check your network connection or try again later."
    )


def test_get_stations() -> None:
    client = HubeauClient()
    stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=1)
    assert isinstance(stations, list)
    if stations:
        assert hasattr(stations[0], "code_station")
        assert hasattr(stations[0], "libelle_station")


def test_get_analyses() -> None:
    client = HubeauClient()
    stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=1)
    if not stations:
        pytest.skip("No stations available for testing")
    analyses = client.qualite_rivieres.get_analyses(
        code_station=stations[0].code_station, size=1, max_records=1
    )
    assert isinstance(analyses, list)
    if analyses:
        assert hasattr(analyses[0], "code_station")
        assert hasattr(analyses[0], "libelle_station")
        assert hasattr(analyses[0], "libelle_parametre")
