# Module d'extraction (Appels API et gestion d'erreurs)
import requests

meteo_enpdoint = "https://archive-api.open-meteo.com/v1/archive"
air_quality_endpoint ="https://air-quality-api.open-meteo.com/v1/air-quality"

def retrieve_meteo_by_city(long, lat):
    """ Permet de recuperer les donnees meteo des 7 dernier jours
        d'une ville via ses coordonnees GPS
    """
    params = {
        'latitude': lat,
        'longitude': long,
        'hourly' :['temperature_2m','precipitation'],
        'start_date':'2026-06-02',
        'end_date':'2026-06-09'
    }
    response = requests.get(url=meteo_enpdoint,params=params)
    return response.json()

def retrieve_air_quality_by_city(long, lat):
    """ Permet de recuperer les donnees sur la qualite de l'air 
        des 7 dernier jours d'une ville via ses coordonnees GPS
    """
    params = {
        'latitude': lat,
        'longitude': long,
        'hourly' :'european_aqi',
        'start_date':'2026-06-02',
        'end_date':'2026-06-09'
    }
    response = requests.get(url=air_quality_endpoint,params=params)
    return response.json()
