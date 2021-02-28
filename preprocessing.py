import numpy as np
from functools import partial, reduce

class DataGenerator ():
  def __init__(self, trajectories, status):
    self.trajectories = trajectories
    self.status = status
    self.num_URLs = max(self.trajectories.sum()) + 1
    self.index = np.arange(len(self.trajectories))
    np.random.seed(9)
    np.random.shuffle(self.index)
    self.n_valid = int(2*np.sqrt(len(self.trajectories)))
    self.n_train = len(self.trajectories) - self.n_valid
    self.success_rate = self.status[self.index[:self.n_train]].sum() / self.n_train

  def build_generators(self, use_status):
    incoming_traj = []
    outgoing_traj = []

    for traj in self.trajectories.values:
      incoming_traj.append(np.array(traj[:-1]).reshape(1,-1))
      outgoing_traj.append(np.array(traj[1:]).reshape(-1,1))


    def data_generator(start, stop):
      while True:
        for i in range(start, stop):        
            x = incoming_traj[self.index[i]].reshape(1,-1)
            s = np.broadcast_to(self.status[self.index[i]], x.shape) ## do I set self.status?
            y = outgoing_traj[self.index[i]].reshape(1,-1)
            if use_status:
                yield [x,s],y
            else:
                yield x,y

    train_generator = partial(data_generator, 0, self.n_train)
    valid_generator = partial(data_generator, self.n_train, self.n_train+self.n_valid)
    return train_generator, valid_generator
