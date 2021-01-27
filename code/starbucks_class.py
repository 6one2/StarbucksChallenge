import pandas as pd
import numpy as np
from .data_wrangling import load_data

PORTFOLIO, PROFILE, TRANSCRIPT = load_data('./data/')

class Person():
    
    def __init__(self, _id):
        self._id = _id
        self.data = TRANSCRIPT.query('person == @_id')
        self.offers = self.data.query('event == "offer received"').index.tolist()
        self.total_spending = self.data['amount'].sum()
    
    
    def get_transaction(self, start, end):
        if not any(self.data['event'] == 'transaction') or np.isnan(start):
            return []
            
        return self.data.query('(event == "transaction") & (@start <= time <= @end)')[['time', 'amount']]
    
    def get_reward(self, start, end):
        if not any(self.data['event'] == 'offer completed') or np.isnan(start):
            return []
        
        return self.data.query('(event == "offer completed") & (@start <= time <= @end)')[['time', 'reward']]
    

class Event():

    def __init__(self, _id:int, df):
        '''
        INPUTS
        _id - indice of offer according to TRANSCRIPT
        df - dataframe with series of events - usually subset of transcript for 1 user
        '''
        self._id = _id
        self.offer_id = df.loc[self._id,'offer_id']
#         self.details = PORTFOLIO.query('id == @self.offer_id')
        self.details = PORTFOLIO.loc[self.offer_id,:]
        self.offer_type = self.details['offer_type']
        duration_hours = self.details['duration'] * 24
        self.start = df.loc[self._id,'time']
        self.end = self.start + duration_hours
        
        self.events = df.query('@self.start <= time <= @self.end')
        
        test_viewed = self.events.query('(event == "offer viewed") & (offer_id == @self.offer_id)')['time']
        test_completed = self.events.query('(event == "offer completed") & (offer_id == @self.offer_id)')['time']
        
        self.viewed = np.nan if test_viewed.empty else test_viewed.values[0]
        self.completed = np.nan if test_completed.empty else test_completed.values[0]