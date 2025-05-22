from hubeau_py.api.qualite_rivieres import QualiteRivieresAPI


class HubeauClient:
    def __init__(self) -> None:
        self.qualite_rivieres = QualiteRivieresAPI()
        # In the future, add other APIs as attributes
        # self.hydrometrie = HydrometrieAPI()
        # self.temperature = TemperatureAPI()
