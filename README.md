# Learner pathway modeling information for MITxPRO Additive Manufacturing and LaaL courses

To clone the repository:

```
git clone https://github.com/mginda/edx-learnerpathway-modeling.git

```

## Model Overviews

Long Short Term Memory (LSTM) neural network and K-medoid clustering is used to identify and predict navigational sequences i.e. trajectories derived from clickstream data.  The model seeks to learn how students progress through course design, and how the interplay between trajectory choices and whether students are successful or not. For this project, success and non-success is defined by the student receiving a certificate for the course, or not.  Clickstream data generated by students is used to learn about the degree to which learner transition activity aligns with the instructor/course design, as well as the models empirically observe emergent learner behavior patterns.

Visited URLs are the discrete set of choices made by learners.  to model this data, it is necessary to transform this into a continuous vector space through an embedding.  For this model we choose to learn the embedding as part of the broader model optimization rather than attempt to predefine it with a skip-gram or heuristic.

LSTM models are one of the most popular variants of Recurrent Neural Networks (RNN) providing an architecture that is able to adequately represent longer sequences without issues of the vanishing the gradient problem.   This work uses the standard definitions of LSTM.  

## Data

## Analysis and Discussion 

### Clustering
For the purposed of clustering only, we vectorize the counts of transitions between URLs for each trajectory.  This is equivalent to bi-grams in NLP.  
We do not normalize the counts, as their raw magnitudes capture information how different students go back and forth.  We then use a k-medoid scheme to cluster these vectors for various values of k.  We use the elbow method on inter-cluster variance to determine k = 4 is the most natural clustering.  The exemplar trajectoris from each cluster are visualized below.

CountVectorizer
Kmedoids
loop over ks
plt

### Baseline Model
For the baseline model we look at sequences of URLs within a given trajectory.  At its simplest level we can make predictions on the mostly likely next URL based only on the current URL only.  This results in 0.49 accuracy.  This is a Markov model with no hidden state.  We also explored using a longer history of URLs to predict the next URL.  Without a smoothing parameter the highest accuracy was achieved 3 element histories which moved accuracy to 0.54.

test, train = data
frequencies = markov_model(train)
accuracy = markov_model.predict(test)

### Trajectory Modeling - LSTM
Our model converts a trajectory to an embedded vector represetnation which is then processed thorugh an LSTM model.  The output of the LSTM goes through a Dense layer with softmax to assign the probabilities of each next possible URL.  


keras model
keras.fit

### Conditional Trajectory Modeling - LSTM
To expand upon our intial model, we want to understand how the choices and successful and unsuccessful students differ.  We process the embedding and LSTM as before.  In te conditional model a second embedding is also learned that provides a vector of weights to multiply against the LSTM output.  This acts as a mask like operation, effectively upweighting and down weighting different parts of information from teh possible next URL choice.  The output of this multiplication is then past through a Dense layer with softmax as before.  picture

keras model
keras.fit

## File details

[LSTM model](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/learning_pathways.ipynb)
[Baseline model](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/baseline_model.ipynb)
[Additive K-medoid model](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/clustering_trajectories.ipynb)
  * [K-medoid cluster, K=10](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/kmedoids%2010%20clusters.csv)
  * [K-medoid cluster, K=4](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/kmedoids%204%20clusters.csv)
  * [K-medoid cluster, K=2](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/kmedoids%202%20clusters.csv)
[LaaL K-medoid model](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/clustering_trajectories_LaaL.ipynb)
  * [K-medoid cluster, K=2](https://github.com/mginda/edx-learnerpathway-modeling/blob/python/LaaL%20kmedoids%202%20clusters.csv)

