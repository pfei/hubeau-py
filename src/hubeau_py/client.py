from hubeau_py.api.hydrometrie import HydrometrieAPI
from hubeau_py.api.qualite_rivieres import QualiteRivieresAPI


class HubeauClient:
    """Unified client for the Hubeau APIs.
    Access sub-APIs as .qualite_rivieres and .hydrometrie attributes.
    """

    def __init__(self) -> None:
        self.qualite_rivieres = QualiteRivieresAPI()
        self.hydrometrie = HydrometrieAPI()
