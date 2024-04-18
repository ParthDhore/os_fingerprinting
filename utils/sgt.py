from sgt import SGT
import pandas as pd
import pickle

with open('models\sgt_model.pkl', 'rb') as f:
    sgt = pickle.load(f)

def get_enc(olayout):
      data={'id':1, 'sequence': olayout}
      temp=pd.DataFrame([data])
      val=sgt.transform(temp)
      val.drop(['id'], axis=1, inplace=True)
      return val.to_numpy()
