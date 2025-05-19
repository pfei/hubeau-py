from hubeau_py.client import HubeauClient


def test_get_stations() -> None:
    client = HubeauClient()
    stations = client.get_stations("Agen")
    assert isinstance(stations, list)
    if stations:
        assert hasattr(stations[0], "code_station")
        assert hasattr(stations[0], "libelle_commune")
