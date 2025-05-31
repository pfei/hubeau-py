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
    """Test that get_stations returns a list of models with required fields."""
    client = HubeauClient()
    stations = client.get_stations(size=10)
    assert isinstance(stations, list)
    # If there are stations, check the first one has required fields
    if stations:
        assert hasattr(stations[0], "code_station")
        assert hasattr(stations[0], "libelle_station")


def test_get_analyses() -> None:
    """Test that get_analyses returns a list of models with required fields."""
    client = HubeauClient()
    # First, get a station to use as example
    stations = client.get_stations(size=1)
    if not stations:
        pytest.skip("No stations available for testing")
    # Get analyses for the first station
    analyses = client.get_analyses(code_station=stations[0].code_station, size=10)
    assert isinstance(analyses, list)
    # If there are analyses, check the first one has required fields
    if analyses:
        assert hasattr(analyses[0], "code_station")
        assert hasattr(analyses[0], "libelle_station")
        assert hasattr(analyses[0], "libelle_parametre")
