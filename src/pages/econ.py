import os
import pickle
import numpy as np
import pandas as pd
import sklearn
import time
import copy
import random

from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from scipy.stats import mode

random.seed(123)
np.random.seed(123)

NPI_MAX_VALUES = {
    'C1_School closing': 3,
    'C2_Workplace closing': 3,
    'C3_Cancel public events': 2,
    'C4_Restrictions on gatherings': 4,
    'C5_Close public transport': 2,
    'C6_Stay at home requirements': 3,
    'C7_Restrictions on internal movement': 2,
    'C8_International travel controls': 4,
    'H1_Public information campaigns': 2,
    'H2_Testing policy': 3,
    'H3_Contact tracing': 2,
    'H6_Facial Coverings': 4
}

NPI_COLUMNS = list(NPI_MAX_VALUES.keys())
E1_decoder = {0. : "0/0",
              1. : "1/0",  
              2. : "2/0", 
              11.: "1/1", 
              12.: "2/1"}

E1_meanings = {
    "0/0" : 'No income support',
    "1/0" : 'Government is replacing less than 50 percent of lost salary, formal sector workers only',
    "2/0" : 'Government is replacing 50 percent or more of lost salary, formal sector workers only',
    "1/1" : 'Government is replacing less than 50 percent of lost salary, all workers',
    "2/1" : 'Government is replacing 50 percent or more of lost salary, all workers',
}
E2_meanings = {
    0.0: 'No debt/contract relief',
    1.0: 'Narrow relief, specific to one kind of contract',
    2.0: 'Broad debt/contract relief',
}

def add_geo_id(df):

    df['RegionName'] = df['RegionName'].replace('', np.nan)
    df['GeoID'] = np.where(df['RegionName'].isnull(),
                           df['CountryName'],
                           df['CountryName'] + ' / ' + df['RegionName'])
    return df


def output_econ_predictions_geo(econ_filepath,
                                prescriptions_geo,
                                target_vars = ['E1_cat', 'E2_cat']):
    """
    Main function that returns prescription outputs. 
    Inputs:
        - econ_filepath: filepath to the pickle containing the trained models
                         and the encoders for the predicted variables
        
        - prescriptions_geo: Oxford tracker-style dataframe for a single GeoID
                             Must contain: NPI columns, date columns, and 
                                           Country/Region or GeoID columns
    
    Outputs for the well predicted geos:
        A dataframe with the following columns: 
        - Date
        - GeoID
        - E1_cat: categorical variable for qualitative description of income support
            - format is "x/x"
                - the left number represents the value of E1
                - the right number represents the value of a flag associated to E1
        - E2_cat: categorical variable for qualitative description of Household
                  debt/contract relief
    Outputs for the poorly predicted geos:
        - np.nan
    """
    
    if 'GeoID' not in prescriptions_geo.columns:
        prescriptions_geo = add_geo_id(prescriptions_geo)
    assert len(prescriptions_geo.GeoID.unique()) == 1, 'only 1 geo in df'
    geo = prescriptions_geo.GeoID.unique()[0]
    
    # load econ models - these are geo specific
    with open(econ_filepath, 'rb') as f:
        models_and_encoders = pickle.load(f)

    good_models = models_and_encoders[0]
    encoders = models_and_encoders[1]
    
    # get 14 rolling window mode of NPIs
    df = prescriptions_geo[NPI_COLUMNS + ['Date', 'GeoID']]
    df.loc[:, NPI_COLUMNS] = df[NPI_COLUMNS].fillna(0).rolling(14, center=True).apply(lambda x: mode(x)[0])
    df = df.dropna(subset = NPI_COLUMNS)
    
    # if geo has good predictions about E1 and E2
    if geo in good_models['E1_cat'].keys():

        for target in target_vars[0:2]:
            df[target] = good_models[target][geo].predict(df[NPI_COLUMNS])
            df[target] = encoders[geo][target].inverse_transform(df[target])

        df['E1_cat'] = df['E1_cat'].replace(E1_decoder)
        return df[['Date', 'GeoID', 'E1_cat', 'E2_cat']]    

    # if geo has no good info
    else:
        return np.nan