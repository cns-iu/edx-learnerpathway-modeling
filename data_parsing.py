import pandas as pd
import numpy as np
from glob import glob
import os

# for each student this is list of numerical id's for the URLs - removing duplicates
def get_trajectory(df):
    order = [0]
    for url in df['order']:
        if url != order[-1]:
            order.append(url)
    order.append(0)
    return order

def load_trajectories(folder_path, status_file):
	trajectories = []

	for fname in glob(folder_path + '/*.csv'):
	    df = pd.read_csv(fname)
	    trajectories.append(df)
	    
	trajectories = pd.concat(trajectories)
	trajectories = pd.DataFrame(trajectories.groupby('user_id').apply(get_trajectory)).reset_index()

	id_and_performance = pd.read_csv(status_file)
	dummy = pd.merge(trajectories, id_and_performance, left_on='user_id', right_on='id', how='inner')

	#add data for pass/fail to status
	status = np.where(dummy['certGrp'].str.contains('Certified'), 1, 0)
	trajectories = trajectories.set_index('user_id')
	trajectories.columns = ['some string']
	return trajectories['some string'], status

#def load_status(folder_path):
