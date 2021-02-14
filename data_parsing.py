import pandas as pd
import numpy as np
from glob import glob
import os

class DataParser ():
  def __init__(self, folder_path, status_file):
    self.folder_path = folder_path
    self.status_file = status_file
    self._load_trajectories()

  def _get_trajectory(self, df):
    order = [0]
    for url in df['order']:
      if url != order[-1]:
          order.append(url)
    order.append(0)
    return order

  def _load_trajectories(self):
    self.trajectories = []

    for fname in glob(self.folder_path + '/*.csv'):
      df = pd.read_csv(fname)
      self.trajectories.append(df)
        
    self.trajectories = pd.concat(self.trajectories)
    self.trajectories = pd.DataFrame(self.trajectories.groupby('user_id').apply(self._get_trajectory)).reset_index()

    id_and_performance = pd.read_csv(self.status_file)
    dummy = pd.merge(self.trajectories, id_and_performance, left_on='user_id', right_on='id', how='inner')

    #add data for certificate status
    self.status = np.where(dummy['certGrp'].str.contains('Certified'), 1, 0)
    self.trajectories = self.trajectories.set_index('user_id')
    self.trajectories.columns = ['some string']
    self.trajectories = self.trajectories['some string']