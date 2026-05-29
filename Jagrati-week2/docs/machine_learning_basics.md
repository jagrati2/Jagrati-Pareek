# Machine Learning Basics

## What is Machine Learning?
Machine learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves.

## Types of Machine Learning

### Supervised Learning
In supervised learning, the algorithm is trained on labeled data. The model learns to map input features to output labels. Examples include:
- Linear Regression for predicting continuous values
- Logistic Regression for binary classification
- Decision Trees and Random Forests
- Support Vector Machines (SVM)
- Neural Networks

### Unsupervised Learning
Unsupervised learning works with unlabeled data. The model finds hidden patterns or intrinsic structures. Examples include:
- K-Means Clustering
- Hierarchical Clustering
- Principal Component Analysis (PCA)
- Autoencoders

### Reinforcement Learning
In reinforcement learning, an agent learns to make decisions by interacting with an environment. The agent receives rewards or penalties based on its actions and learns to maximize cumulative reward. Examples include game-playing AI like AlphaGo.

## Key Concepts

### Training and Test Sets
Data is typically split into training set (used to train the model) and test set (used to evaluate performance). A validation set is often used during training to tune hyperparameters.

### Overfitting and Underfitting
- Overfitting: Model learns training data too well, performs poorly on new data
- Underfitting: Model is too simple to capture patterns in the data
- Regularization techniques (L1, L2) help prevent overfitting

### Gradient Descent
Gradient descent is an optimization algorithm used to minimize the loss function. It iteratively adjusts model parameters in the direction that reduces the error. Variants include Stochastic Gradient Descent (SGD), Mini-batch Gradient Descent, and Adam optimizer.

### Cross-Validation
Cross-validation is a technique to evaluate model performance on different subsets of data. K-fold cross-validation splits data into K equal parts and trains/tests the model K times.

## Common Metrics
- Accuracy: Proportion of correct predictions
- Precision: True positives / (True positives + False positives)
- Recall: True positives / (True positives + False negatives)
- F1 Score: Harmonic mean of precision and recall
- Mean Squared Error (MSE) for regression tasks
- ROC-AUC for classification problems