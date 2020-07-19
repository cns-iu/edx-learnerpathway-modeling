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

def load_trajectories(folder_path):
	trajectories = []

	for fname in glob(folder_path + '/*.csv'):
	    df = pd.read_csv(fname)
	    trajectories.append(df)
	    
	trajectories = pd.concat(trajectories)
	return trajectories.groupby('user_id').apply(get_trajectory)