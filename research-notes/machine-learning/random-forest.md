# Random Forest

<https://www.ibm.com/cloud/learn/random-forest>

- A supervised ML algorithm
- Combines the output of multiple decision trees to reach a single result
  - Ideally decision trees are uncorrelated
  - The average or most popular result is the ultimate decision
- Uses a subset of all possible feature splits
- Hyperparameters: Node size, number of trees, number of features sampled
- Random forest makes a “forest” of decision trees each of which uses a different subset of the entire training dataset
  - 1/3 of data is set aside – the out-of-bag sample
- For classification needs, random forest does a “majority vote” for decision tree results
  - Out-of-bag sample is used for cross-validation, finalizing prediction
- Benefits:
  - Reduced risk of overfitting: Training data is not generalized enough, so unseen scenarios fail to be recognized – high variance
  - Flexible: Classification or regression
  - Determines Feature Importance Easily
- Challenges:
  - Time Consuming, more complex, requires resources to store and process data

<https://towardsdatascience.com/understanding-random-forest-58381e0602d2>
