import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import LSTM, Dense, Input, Embedding, Reshape, Multiply
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model

class Base_model ():
  def __init__(self):
    pass

  def save(self, fname):
    pass

  def generate_traj(self, proposed_traj):
    proposed_traj = [0]
    visit_count = defaultdict(int)
    max_allowed_visits = 25

    while len(proposed_traj) < 1000 and (len(proposed_traj) == 1 or proposed_traj[-1] != 0):
        x = np.array(proposed_traj).reshape(1,-1)
        for url in reversed(np.argsort(self.predict(x)[0,-1])):
            if visit_count[url] < max_allowed_visits:
                proposed_traj.append(url)
                visit_count[url] += 1
                break
        
    traj_to_edge_csv(proposed_traj, 'traj_fname.csv')

class LSTM_model (Base_model):
  def __init__(self, number_of_URL, optimizer=Adam(learning_rate=0.001), num_hidden=10, embedding_size=10, simple=True):
    super(self.__class__, self).__init__
    self.num_hidden = num_hidden
    self.embedding_size = embedding_size
    self.simple = simple
    self.optimizer = optimizer
    self.number_of_URL = number_of_URL

    self.model = self._build_model()

  def _build_model(self):
    input_ = Input(shape=(None,), name='history')
    embed = Embedding(self.number_of_URL, self.embedding_size, name='URL_embedding')(input_)
    rnn = LSTM(self.num_hidden, return_sequences=True, name='LSTM')(embed)
    predicted_URL = Dense(self.number_of_URL, activation = 'softmax', name='Predicted_URL')(rnn)

    self.model = Model(inputs=input_, outputs=predicted_URL, name='Simple_model')
    self.model.compile(loss='sparse_categorical_crossentropy', optimizer=self.optimizer, metrics=['acc'])
    return self.model

  def train(self, data, filepath=None):
    train_generator, valid_generator = data.build_generators(False)
    if filepath is not None:
      checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
      callbacks_list = [checkpoint]
    else:
      callbacks_list = None
    model.fit_generator(train_generator(), 
                        validation_data=valid_generator(),
                        callbacks=callbacks_list,
                        steps_per_epoch = data.n_train, #batch size is inherently 1 via generator
                        validation_steps= data.n_valid,
                        epochs=150,
                        verbose=1,)

  def save(self, fname):
    self.model.save_weights(os.path.join('weights', fname))

  def load(self, fname):
    path = os.path.join('weights', fname)
    self.model.load_weights(path, by_name=True)

  def predict(self, input_traj):
    #give the probs for the next URLs based on current trajectory
    probabilities = np.array(self.model(input_traj)).reshape(-1, self.number_of_URL)[-1]
    return probabilities 

class Random_model (Base_model):
  def __init__(self):
    super(self.__class__, self).__init__
    pass

  def predict(self, pred_traj):
    pred_traj = np.random.choice(self.number_of_URL)
    enc = np.eye(self.number_of_URL)[pred_traj]
    return enc