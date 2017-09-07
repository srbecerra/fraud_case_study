# Project Scope

## How we will determine feature importance
1. Possibilities
  - PCA
  - UVD (?)
  - Random Forest

## Data preprocessing
0. Reorg data so each row is unique and each column is as meaningful as could be
  - Could split data so each row is ticket instead of event
1. Cleaning
2. Class balancing
  - If significant # of fraud cases (>5000), then make classes equal in number
  - If # of fraud cases is not enough data points, try ...
3. Scaling features
  - Depends on model used (Random Forest not required)

1. Find which features are important (PCA, UVD, or Random Forest)
  - Drop any rows that contain Nan or None or blank
  - I imagine that the html features will be useful for an NLP model, where as money/client info features will be useful for a classification model

## How we will choose models
1. Classification vs regression
  - Classification model is natural fit, but regression could help stratify the different amounts ($) of fraud
  - EDA may tell if there is levels of fraud that we could predict
2. Combining normal (?) with NLP
  - HTML features contain text that could signal when fraud.
  - Need to separate an NLP model from a normal (?) model since an NLP model already has a huge amount of features


## How we will evaluate models
1. Choosing a metric
  - Will use EDA to determine different types of fraud and the different levels ($)
  - Will assume practical costs (real fraud = greater cost vs spam fraud)
  - Use metric that represents parts of cost matrix we want to reduce
2. Evaluate with metric
  - Use cost (ROC) curve
