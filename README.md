# Learner pathway modeling information for MIT xPRO Additive Manufacturing and Leaders at All Levels courses

To clone the repository:

```
git clone https://github.com/mginda/edx-learnerpathway-modeling.git

```
## Model Overview

Long Short Term Memory (LSTM) neural network and K-medoid clustering is used to identify and predict navigational sequences i.e. trajectories derived from clickstream data.  The model seeks to learn how students progress through course design, and how the interplay between trajectory choices impacts the students success in the course. For this project, success and non-success is defined by the student receiving a certificate for the course, or not.  Clickstream data generated by students is used to learn about the degree to which learner transition activity aligns with the instructor/course design, as well as the models empirically observed emergent learner behavior patterns (LBP).

Visited URLs are the discrete set of choices made by learners.  To model this data, it is necessary to transform this into a continuous vector space through an embedding.  For this model we choose to learn the embedding as part of the broader model optimization rather than attempt to predefine it with a skip-gram or heuristic.

LSTM models are one of the most popular variants of Recurrent Neural Networks (RNN) providing an architecture that is able to adequately represent longer sequences without issues of the vanishing gradient problem.   This work uses the standard definitions of LSTM.  

## Data
| Module type    |    AM    | LaaL     |
| -------------- | -------- | -------- |
| Course         |     1    |     1    |
| Chapter        |     21   |     7    |
| Sequential     |     88   |     46    |
| Vertical       |     246   |     147    |
| Html           |     451   |     219    |
| Problem        |     173   |     162    |
| Video          |     107   |     56    |
| Open assessment|     10   |     5    | 
| Discussion     |     8    |     0    | 
| Drag and Drop  |     0    |     17    | 
| External Tool  |     0    |     7    | 
| Poll           |     0    |     6    | 
| Survey         |     0    |     3    | 
| **Total Modules**     |     1105   |     676    | 

## Components used in analysis
### Clustering
For the purpose of clustering only, vectorization of the counts of transitions between URLs for each trajectory.  This is equivalent to bi-grams in natural language processing (NLP).  The counts are not normalized, as their raw magnitudes capture information on how different students go back and forth through course materials.

The k-medoid algorithm is used to cluster these vectors for various values of k.  The elbow method is used on inter-cluster variance to determine k = 4 is the most natural clustering.

View analysis [here](https://github.com/mginda/edx-learnerpathway-modeling/blob/main/clustering_analysis/trajectory_clustering.ipynb)

### Baseline Model
For the baseline model observation of sequences of URLs within a given trajectory.  At its simplest level predictions are made on the most likely next URL based only on the current URL only.  This is a Markov model with no hidden state.
This results in 0.49 accuracy.  A longer history of URLs was explored to predict the next URL.  Without a smoothing parameter the highest accuracy was achieved with 3 element histories i.e. URL sequence of length 3, which moved accuracy to 0.54.

### Trajectory LSTM Model
The model converts a trajectory to an embedded vector representation which is then processed through an LSTM model.  The output of the LSTM goes through a Dense layer with Softmax to assign the probabilities of each next possible URL.  

### Conditional Trajectory LSTM Model
To expand upon the intial model, and attempt was made to understand if the choices of successful and non-successful learners differ. The embedding and LSTM are processed as before.  In the conditional model a second embedding is also learned that provides a vector of weights to multiply against the LSTM output.  This acts as a mask like operation, effectively upweighting and down weighting different parts of information from the possible next URL choice.  The output of this multiplication is then past through a Dense layer with softmax as before.


### Run with the following
### file imports
```
from data_parsing import DataParser
from models import LSTM_model
from preprocessing import DataGenerator

```
### parsing
```
data = DataParser('file_1', 'file_2')

```
### run the generators
```
generator = DataGenerator(data.trajectories, data.status)

```
### run the models
```
model = LSTM_model(generator.num_URLs)
model.train(generator)

```
