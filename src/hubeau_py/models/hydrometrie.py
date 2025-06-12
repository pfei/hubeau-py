from typing import Any, Dict, Optional

from pydantic import BaseModel


class Site(BaseModel):
    code_site: Optional[str] = None
    libelle_site: Optional[str] = None
    altitude_site: Optional[float] = None
    code_commune_site: Optional[str] = None
    code_cours_eau: Optional[str] = None
    code_departement: Optional[str] = None
    code_entite_hydro_site: Optional[str] = None
    code_projection: Optional[int] = None  # or str, check API docs
    code_region: Optional[str] = None
    code_systeme_alti_site: Optional[str] = None
    code_troncon_hydro_site: Optional[str] = None
    code_zone_hydro_site: Optional[str] = None
    commentaire_influence_generale_site: Optional[str] = None
    commentaire_site: Optional[str] = None
    coordonnee_x_site: Optional[float] = None
    coordonnee_y_site: Optional[float] = None
    date_maj_site: Optional[str] = None  # or datetime, see API
    date_premiere_donnee_dispo_site: Optional[str] = None  # or datetime, see API
    geometry: Optional[Dict[str, Any]] = None  # or use a GeoJSON model if you want
    grandeur_hydro: Optional[str] = None
    influence_generale_site: Optional[str] = None
    latitude_site: Optional[float] = None
    libelle_commune: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    libelle_departement: Optional[str] = None
    libelle_region: Optional[str] = None
    longitude_site: Optional[float] = None
    premier_mois_annee_hydro_site: Optional[int] = None  # or str, see API
    premier_mois_etiage_site: Optional[int] = None  # or str, see API
    statut_site: Optional[str] = None
    surface_bv: Optional[float] = None
    type_contexte_loi_stat_site: Optional[str] = None
    type_loi_site: Optional[str] = None
    type_site: Optional[str] = None
    uri_cours_eau: Optional[str] = None


class Station(BaseModel):
    altitude_ref_alti_station: Optional[float] = None
    code_commune_station: Optional[str] = None
    code_cours_eau: Optional[str] = None
    code_departement: Optional[str] = None
    code_finalite_station: Optional[str] = None
    code_projection: Optional[int] = None  # or str, check API
    code_regime_station: Optional[str] = None
    code_region: Optional[str] = None
    code_sandre_reseau_station: Optional[str] = None
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_systeme_alti_site: Optional[str] = None
    commentaire_influence_locale_station: Optional[str] = None
    commentaire_station: Optional[str] = None
    coordonnee_x_station: Optional[float] = None
    coordonnee_y_station: Optional[float] = None
    date_activation_ref_alti_station: Optional[str] = None  # or datetime
    date_debut_ref_alti_station: Optional[str] = None  # or datetime
    date_fermeture_station: Optional[str] = None  # or datetime
    date_maj_ref_alti_station: Optional[str] = None  # or datetime
    date_maj_station: Optional[str] = None  # or datetime
    date_ouverture_station: Optional[str] = None  # or datetime
    descriptif_station: Optional[str] = None
    en_service: Optional[bool] = None
    geometry: Optional[Dict[str, Any]] = None  # or GeoJSON model
    influence_locale_station: Optional[str] = None
    latitude_station: Optional[float] = None
    libelle_commune: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    libelle_departement: Optional[str] = None
    libelle_region: Optional[str] = None
    libelle_site: Optional[str] = None
    libelle_station: Optional[str] = None
    longitude_station: Optional[float] = None
    qualification_donnees_station: Optional[str] = None
    type_contexte_loi_stat_station: Optional[str] = None
    type_loi_station: Optional[str] = None
    type_station: Optional[str] = None
    uri_cours_eau: Optional[str] = None


class Observation(BaseModel):
    code_continuite: Optional[int] = None  # Check API: sometimes int, sometimes str
    code_methode_obs: Optional[str] = None
    code_qualification_obs: Optional[str] = None
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_statut: Optional[int] = None  # or str, see API
    code_systeme_alti_serie: Optional[str] = None
    date_debut_serie: Optional[str] = None  # or datetime
    date_fin_serie: Optional[str] = None  # or datetime
    date_obs: Optional[str] = None  # or datetime
    grandeur_hydro: Optional[str] = None  # e.g. "H" (hauteur), "Q" (débit)
    latitude: Optional[float] = None
    libelle_continuite: Optional[str] = None
    libelle_methode_obs: Optional[str] = None
    libelle_qualification_obs: Optional[str] = None
    libelle_statut: Optional[str] = None
    longitude: Optional[float] = None
    resultat_obs: Optional[float] = None  # or int, depending on the data


class ObservationElab(BaseModel):
    code_methode: Optional[str] = None
    code_qualification: Optional[str] = None
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_statut: Optional[int] = None  # or str, see API
    date_obs_elab: Optional[str] = None  # or datetime
    date_prod: Optional[str] = None  # or datetime
    grandeur_hydro_elab: Optional[str] = None  # e.g. "QmnJ", "H"
    latitude: Optional[float] = None
    libelle_methode: Optional[str] = None
    libelle_qualification: Optional[str] = None
    libelle_statut: Optional[str] = None
    longitude: Optional[float] = None
    resultat_obs_elab: Optional[float] = None  # or int, depending on the data
