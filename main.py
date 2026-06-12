# Chef d'orchestre du pipeline
import src.extractor as ex
import src.transformer as tr
import pandas as pd
cities={
    "tokyo" : {"long" : 139.691706,"lat":35.689487},
    "paris" : {"long" : 2.3522219,"lat":48.856614},
    "londre" : {"long" : -0.1277583,"lat":51.5073509}
}
meteo_raw_data = ex.retrieve_meteo_by_city([139.691706,2.3522219,-0.1277583],[35.689487,48.856614,51.5073509])
air_quality_raw_data = ex.retrieve_air_quality_by_city([139.691706,2.3522219,-0.1277583],[35.689487,48.856614,51.5073509])

meteo_dict = tr.transform_meteo_data(meteo_raw_data)
air_index_dict = tr.transform_air_index_data(air_quality_raw_data)
meteo_and_air_index_df = tr.merge_data(air_index_dict,meteo_dict)
print(meteo_and_air_index_df)

