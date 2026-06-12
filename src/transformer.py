# Module de transformation (Nettoyage et formatage)
import pandas as pd

cities={
    "Tokyo" : {"long" : 139.691706,"lat":35.689487},
    "Paris" : {"long" : 2.3522219,"lat":48.856614},
    "Londres" : {"long" : -0.1277583,"lat":51.5073509}
}
mapping = {
    'Tokyo': 0,
    'Londres': 1,
    'Paris': 2
}



def transform_air_index_data(data):
    """
        cette fonction permet de transformer le json de l'api de recuperation des index de la 
        qualite de l'air en dataframe correctement formatter
    """
    df =pd.DataFrame(data)
    print(df)
    #on creer le champs city_name en cherchant le nom de la ville a partir des coordonnees
    df["city_name"]=df.apply(lambda item: get_city_by_long_lat(item["longitude"],item["latitude"]),axis=1)
    # #on supprime les colonnes inutiles
    df=df.drop(["generationtime_ms","timezone","elevation","timezone_abbreviation","location_id","utc_offset_seconds"], axis=1)
    #on creer un dictionnaire pour faire le traitement ville par ville
    dfs=dict()
    for city in df['city_name'].unique():
        dfs[city] = df[df['city_name'] == city]

    # print(dfs)
    for city, df in dfs.items():
        df_exploded = df["hourly"].apply(pd.Series).explode(["time","european_aqi"])
        dfs[city] = df_exploded
    
    return dfs
    # """
    #     on utilise la fonction apply avec ce param pour eclater le dict "hourly" en colonne ,
    #     ses clef deviennent les colonnes  dans le df et ses valeurs constite les ligne de la colonne.
    #     Ici chaque element est une list
    # """
    # df_exploded = df["hourly"].apply(pd.Series)
    # """
    #     on utilise la fonction explode pour eclater les listes des colonnes times et european_aqi en ligne
    #     ainsi chaque des listes devient une lignes
    # """
    # final_air_index= df_exploded.explode(["time","european_aqi"])
    # final_air_index=final_air_index.reset_index()
    # return final_air_index
    
def transform_meteo_data(data):
    """
        cette fonction permet de transformer le json de l'api de recuperation des
        historiques meteo  en dataframe correctement formatter
    """
    df =pd.DataFrame(data)
    #on creer le champs city_name en cherchant le nom de la ville a partir des coordonnees
    df["city_name"]=df.apply(lambda item: get_city_by_long_lat(item["longitude"],item["latitude"]),axis=1)
    #on modifie l'index de notre dataframe pour mettre les jours
    #df=df.set_index('city_name')
    #on supprime les colonnes inutiles
    df=df.drop(["generationtime_ms","timezone","elevation","timezone_abbreviation","location_id","utc_offset_seconds"], axis=1)
    dfs=dict()
    for city in df['city_name'].unique():
        dfs[city] = df[df['city_name'] == city]

    # print(dfs)
    for city, df in dfs.items():
        df_exploded = df["hourly"].apply(pd.Series).explode(["time","temperature_2m","precipitation"])
        dfs[city] = df_exploded

    return dfs
    # """
    #     on utilise la fonction apply avec ce param pour eclater le dict "hourly" en colonne ,
    #     ses clef deviennent les colonnes  dans le df et ses valeurs constite les ligne de la colonne.
    #     Ici chaque element est une list
    # """
    # df_exploded = df["hourly"].apply(pd.Series)
    # """
    #     on utilise la fonction explode pour eclater les listes des colonnes times et european_aqi en ligne
    #     ainsi chaque des listes devient une lignes
    # """
    # final_meteo= df_exploded.explode(["time","temperature_2m","precipitation"])
    # # print(final_air_index.index)
    # final_meteo=final_meteo.reset_index()
    # return final_meteo
def merge_data(meteo_dict,air_index_dict):
    """ """
    #on creer un nouveau dict
    merged_dict = {}
    #on effectue un merge des dictionnaires ville par ville
    for city in meteo_dict:
        merged_dict[city] = pd.merge(meteo_dict[city],air_index_dict[city], on='time')
        merged_dict[city]["city"] = city
    
    #maintenant on fusionnes les dfs les uns a la suite des autres
    return pd.concat(merged_dict.values(), ignore_index=True)

def get_city_by_long_lat(long,lat):
    """ permet de recuperer le nom d'une ville via les coordonnees gps"""
    for name,coord in cities.items():
        if(int(coord["long"]) == int(long) and int(coord["lat"]) == int(lat)):
            return name;

def extract_air_index(col):
    """extraire les donnees de european api dans la colonne hourly"""
    for data in col:
        return (data["time"],data["european_aqi"])

    