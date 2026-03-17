# Machine Learning

OpenCV's Machine Learning module (`cv2.ml`) provides a comprehensive set of statistical machine learning algorithms for classification, regression, and clustering tasks. These tools enable pattern recognition, data analysis, and predictive modeling directly within the OpenCV framework.

The module includes both traditional machine learning algorithms (SVM, KNN, decision trees) and neural networks, all designed to work seamlessly with OpenCV's matrix data structures and image processing capabilities.

## Capabilities

### StatModel Base Class

The `StatModel` class serves as the base class for all statistical models in OpenCV's ML module, providing a unified interface for training, prediction, and model persistence.

```python { .api }
# Core methods available on all StatModel subclasses

# Train the model
StatModel.train(samples, layout, responses) -> retval

# Make predictions
StatModel.predict(samples[, results[, flags]]) -> retval, results

# Save trained model to file
StatModel.save(filename) -> None

# Load model from file (class method)
StatModel.load(filename) -> model

# Calculate prediction error
StatModel.calcError(data, test) -> retval, resp

# Check if model is trained
StatModel.isTrained() -> retval

# Check if model is a classifier
StatModel.isClassifier() -> retval

# Get number of variables
StatModel.getVarCount() -> retval
```

**Training Data Layouts:**
- `cv2.ml.ROW_SAMPLE` - Each row represents a training sample
- `cv2.ml.COL_SAMPLE` - Each column represents a training sample

### Support Vector Machines (SVM)

Support Vector Machines are powerful supervised learning algorithms used for classification and regression. They work by finding the optimal hyperplane that maximally separates different classes in high-dimensional space.

```python { .api }
# Create SVM instance
cv2.ml.SVM_create() -> svm

# Configure SVM
SVM.setType(val) -> None
SVM.getType() -> retval

SVM.setKernel(val) -> None
SVM.getKernel() -> retval

SVM.setDegree(val) -> None
SVM.getDegree() -> retval

SVM.setGamma(val) -> None
SVM.getGamma() -> retval

SVM.setCoef0(val) -> None
SVM.getCoef0() -> retval

SVM.setC(val) -> None
SVM.getC() -> retval

SVM.setNu(val) -> None
SVM.getNu() -> retval

SVM.setP(val) -> None
SVM.getP() -> retval

# Get support vectors
SVM.getSupportVectors() -> retval

# Get decision function
SVM.getDecisionFunction(i) -> retval, alpha, svidx

# Automatic parameter optimization
SVM.trainAuto(samples, layout, responses[, kFold[, ...]])
```

**SVM Types:**
```python { .api }
cv2.ml.SVM_C_SVC          # C-Support Vector Classification
cv2.ml.SVM_NU_SVC         # Nu-Support Vector Classification
cv2.ml.SVM_ONE_CLASS      # One-class SVM (anomaly detection)
cv2.ml.SVM_EPS_SVR        # Epsilon-Support Vector Regression
cv2.ml.SVM_NU_SVR         # Nu-Support Vector Regression
```

**Kernel Types:**
```python { .api }
cv2.ml.SVM_LINEAR         # Linear kernel: u'*v
cv2.ml.SVM_POLY           # Polynomial kernel: (gamma*u'*v + coef0)^degree
cv2.ml.SVM_RBF            # Radial Basis Function: exp(-gamma*|u-v|^2)
cv2.ml.SVM_SIGMOID        # Sigmoid kernel: tanh(gamma*u'*v + coef0)
cv2.ml.SVM_CHI2           # Chi-square kernel
cv2.ml.SVM_INTER          # Histogram intersection kernel
```

### K-Nearest Neighbors (KNearest)

K-Nearest Neighbors is a simple, instance-based learning algorithm that classifies samples based on the majority vote of their k nearest neighbors in the feature space.

```python { .api }
# Create KNN instance
cv2.ml.KNearest_create() -> knearest

# Set number of neighbors
KNearest.setDefaultK(val) -> None
KNearest.getDefaultK() -> retval

# Set algorithm type
KNearest.setAlgorithmType(val) -> None
KNearest.getAlgorithmType() -> retval

# Set E parameter for KDTREE
KNearest.setEmax(val) -> None
KNearest.getEmax() -> retval

# Set if classifier
KNearest.setIsClassifier(val) -> None
KNearest.getIsClassifier() -> retval

# Find nearest neighbors
KNearest.findNearest(samples, k[, results[, ...]]) -> retval, results, neighborResponses, dist
```

**Algorithm Types:**
```python { .api }
cv2.ml.KNearest_BRUTE_FORCE    # Brute force search
cv2.ml.KNearest_KDTREE          # KD-tree for efficient search
```

### Decision Trees (DTrees)

Decision Trees recursively split data based on feature values, creating a tree-like model of decisions. They are interpretable and can handle both numerical and categorical data.

```python { .api }
# Create decision tree instance
cv2.ml.DTrees_create() -> dtree

# Configure tree parameters
DTrees.setMaxDepth(val) -> None
DTrees.getMaxDepth() -> retval

DTrees.setMinSampleCount(val) -> None
DTrees.getMinSampleCount() -> retval

DTrees.setMaxCategories(val) -> None
DTrees.getMaxCategories() -> retval

DTrees.setCVFolds(val) -> None
DTrees.getCVFolds() -> retval

DTrees.setUseSurrogates(val) -> None
DTrees.getUseSurrogates() -> retval

DTrees.setUse1SERule(val) -> None
DTrees.getUse1SERule() -> retval

DTrees.setTruncatePrunedTree(val) -> None
DTrees.getTruncatePrunedTree() -> retval

# Set pruning parameters
DTrees.setPriors(val) -> None
DTrees.getPriors() -> retval

# Get the tree structure
DTrees.getRoots() -> retval
DTrees.getNodes() -> retval
DTrees.getSplits() -> retval
DTrees.getSubsets() -> retval
```

### Random Forest (RTrees)

Random Forest is an ensemble learning method that constructs multiple decision trees during training and outputs the mode of their predictions, providing better accuracy and robustness than single trees.

```python { .api }
# Create random trees instance
cv2.ml.RTrees_create() -> rtrees

# Configure forest parameters
RTrees.setMaxDepth(val) -> None
RTrees.getMaxDepth() -> retval

RTrees.setMinSampleCount(val) -> None
RTrees.getMinSampleCount() -> retval

RTrees.setMaxCategories(val) -> None
RTrees.getMaxCategories() -> retval

# Random forest specific parameters
RTrees.setActiveVarCount(val) -> None
RTrees.getActiveVarCount() -> retval

RTrees.setTermCriteria(val) -> None
RTrees.getTermCriteria() -> retval

RTrees.setCalculateVarImportance(val) -> None
RTrees.getCalculateVarImportance() -> retval

# Get variable importance
RTrees.getVarImportance() -> retval

# Get votes from individual trees
RTrees.getVotes(samples, flags) -> retval
```

### Boosting (Boost)

Boosting algorithms combine multiple weak learners (typically decision trees) into a strong classifier by iteratively training new models to correct errors made by previous ones.

```python { .api }
# Create boosting instance
cv2.ml.Boost_create() -> boost

# Configure boosting parameters
Boost.setBoostType(val) -> None
Boost.getBoostType() -> retval

Boost.setWeakCount(val) -> None
Boost.getWeakCount() -> retval

Boost.setWeightTrimRate(val) -> None
Boost.getWeightTrimRate() -> retval

# Inherits decision tree parameters
Boost.setMaxDepth(val) -> None
Boost.getMaxDepth() -> retval

Boost.setMinSampleCount(val) -> None
Boost.getMinSampleCount() -> retval

Boost.setMaxCategories(val) -> None
Boost.getMaxCategories() -> retval

Boost.setPriors(val) -> None
Boost.getPriors() -> retval
```

**Boosting Types:**
```python { .api }
cv2.ml.Boost_DISCRETE      # Discrete AdaBoost
cv2.ml.Boost_REAL          # Real AdaBoost
cv2.ml.Boost_LOGIT         # LogitBoost
cv2.ml.Boost_GENTLE        # Gentle AdaBoost
```

### Neural Networks (ANN_MLP)

Multi-Layer Perceptron (MLP) is a feedforward artificial neural network with one or more hidden layers. It can learn complex non-linear relationships through backpropagation training.

```python { .api }
# Create neural network instance
cv2.ml.ANN_MLP_create() -> ann

# Configure network architecture
ANN_MLP.setLayerSizes(layerSizes) -> None
ANN_MLP.getLayerSizes() -> retval

# Set activation function
ANN_MLP.setActivationFunction(type[, param1[, param2]]) -> None

# Configure training parameters
ANN_MLP.setTrainMethod(method[, param1[, param2]]) -> None
ANN_MLP.getTrainMethod() -> retval

ANN_MLP.setBackpropWeightScale(val) -> None
ANN_MLP.getBackpropWeightScale() -> retval

ANN_MLP.setBackpropMomentumScale(val) -> None
ANN_MLP.getBackpropMomentumScale() -> retval

ANN_MLP.setRpropDW0(val) -> None
ANN_MLP.getRpropDW0() -> retval

ANN_MLP.setRpropDWPlus(val) -> None
ANN_MLP.getRpropDWPlus() -> retval

ANN_MLP.setRpropDWMinus(val) -> None
ANN_MLP.getRpropDWMinus() -> retval

ANN_MLP.setRpropDWMin(val) -> None
ANN_MLP.getRpropDWMin() -> retval

ANN_MLP.setRpropDWMax(val) -> None
ANN_MLP.getRpropDWMax() -> retval

ANN_MLP.setAnnealInitialT(val) -> None
ANN_MLP.getAnnealInitialT() -> retval

ANN_MLP.setAnnealFinalT(val) -> None
ANN_MLP.getAnnealFinalT() -> retval

ANN_MLP.setAnnealCoolingRatio(val) -> None
ANN_MLP.getAnnealCoolingRatio() -> retval

ANN_MLP.setAnnealItePerStep(val) -> None
ANN_MLP.getAnnealItePerStep() -> retval

# Set termination criteria
ANN_MLP.setTermCriteria(val) -> None
ANN_MLP.getTermCriteria() -> retval

# Get network weights
ANN_MLP.getWeights(layerIdx) -> retval
```

**Activation Functions:**
```python { .api }
cv2.ml.ANN_MLP_IDENTITY        # Identity: f(x) = x
cv2.ml.ANN_MLP_SIGMOID_SYM     # Symmetric sigmoid: f(x) = beta*(1-exp(-alpha*x))/(1+exp(-alpha*x))
cv2.ml.ANN_MLP_GAUSSIAN        # Gaussian: f(x) = beta*exp(-alpha*x*x)
cv2.ml.ANN_MLP_RELU            # ReLU: f(x) = max(0, x)
cv2.ml.ANN_MLP_LEAKYRELU       # Leaky ReLU: f(x) = x if x >= 0 else alpha*x
```

**Training Methods:**
```python { .api }
cv2.ml.ANN_MLP_BACKPROP        # Backpropagation
cv2.ml.ANN_MLP_RPROP           # Resilient backpropagation (RProp)
cv2.ml.ANN_MLP_ANNEAL          # Simulated annealing
```

**Training Flags:**
```python { .api }
cv2.ml.ANN_MLP_UPDATE_WEIGHTS     # Update network weights
cv2.ml.ANN_MLP_NO_INPUT_SCALE     # Do not normalize input
cv2.ml.ANN_MLP_NO_OUTPUT_SCALE    # Do not normalize output
```

### Naive Bayes (NormalBayesClassifier)

Normal Bayes Classifier assumes that features follow a normal (Gaussian) distribution and applies Bayes' theorem for classification. It's simple, fast, and works well when the assumption holds.

```python { .api }
# Create Naive Bayes classifier instance
cv2.ml.NormalBayesClassifier_create() -> bayes

# Train and predict using StatModel interface
# NormalBayesClassifier.train(samples, layout, responses) -> retval
# NormalBayesClassifier.predict(samples) -> retval, results

# Predict with probabilities
NormalBayesClassifier.predictProb(inputs[, outputs[, ...]]) -> retval, outputs, outputProbs
```

### Logistic Regression (LogisticRegression)

Logistic Regression is a linear model for binary and multi-class classification that estimates the probability of class membership using a logistic function.

```python { .api }
# Create logistic regression instance
cv2.ml.LogisticRegression_create() -> lr

# Configure learning parameters
LogisticRegression.setLearningRate(val) -> None
LogisticRegression.getLearningRate() -> retval

LogisticRegression.setIterations(val) -> None
LogisticRegression.getIterations() -> retval

LogisticRegression.setRegularization(val) -> None
LogisticRegression.getRegularization() -> retval

LogisticRegression.setTrainMethod(val) -> None
LogisticRegression.getTrainMethod() -> retval

LogisticRegression.setMiniBatchSize(val) -> None
LogisticRegression.getMiniBatchSize() -> retval

# Get learned coefficients
LogisticRegression.get_learnt_thetas() -> retval
```

**Regularization Types:**
```python { .api }
cv2.ml.LogisticRegression_REG_DISABLE    # No regularization
cv2.ml.LogisticRegression_REG_L1         # L1 regularization (Lasso)
cv2.ml.LogisticRegression_REG_L2         # L2 regularization (Ridge)
```

**Training Methods:**
```python { .api }
cv2.ml.LogisticRegression_BATCH          # Batch gradient descent
cv2.ml.LogisticRegression_MINI_BATCH     # Mini-batch gradient descent
```

### Expectation Maximization (EM)

The EM algorithm is used for finding maximum likelihood estimates of parameters in probabilistic models with latent variables. It's commonly used for Gaussian Mixture Models and clustering.

```python { .api }
# Create EM instance
cv2.ml.EM_create() -> em

# Configure EM parameters
EM.setClustersNumber(val) -> None
EM.getClustersNumber() -> retval

EM.setCovarianceMatrixType(val) -> None
EM.getCovarianceMatrixType() -> retval

EM.setTermCriteria(val) -> None
EM.getTermCriteria() -> retval

# Train the model
EM.trainEM(samples[, logLikelihoods[, labels[, probs]]]) -> retval, logLikelihoods, labels, probs

EM.trainE(samples, means0[, covs0[, weights0[, ...]]]) -> retval, logLikelihoods, labels, probs

EM.trainM(samples, probs0[, logLikelihoods[, labels[, probs]]]) -> retval, logLikelihoods, labels, probs

# Get model parameters
EM.getWeights() -> retval
EM.getMeans() -> retval
EM.getCovs() -> retval

# Predict cluster and probability
EM.predict(samples[, results[, flags]]) -> retval, results
EM.predict2(sample) -> retval, probs
```

**Covariance Matrix Types:**
```python { .api }
cv2.ml.EM_COV_MAT_SPHERICAL    # Spherical covariance matrix (single variance)
cv2.ml.EM_COV_MAT_DIAGONAL     # Diagonal covariance matrix
cv2.ml.EM_COV_MAT_GENERIC      # Full covariance matrix
cv2.ml.EM_COV_MAT_DEFAULT      # Default covariance matrix type
```

**Start Step:**
```python { .api }
cv2.ml.EM_START_E_STEP         # Start with E-step
cv2.ml.EM_START_M_STEP         # Start with M-step
cv2.ml.EM_START_AUTO_STEP      # Automatically choose start step
```

### K-means Clustering

K-means is a clustering algorithm that partitions data into K clusters by iteratively assigning samples to the nearest cluster center and updating centers based on assigned samples.

```python { .api }
# Perform K-means clustering
cv2.kmeans(data, K, bestLabels, criteria, attempts, flags) -> retval, bestLabels, centers

# Parameters:
#   data - Input data (each row is a sample)
#   K - Number of clusters
#   bestLabels - Output labels (cluster assignments)
#   criteria - Termination criteria (type, max_iter, epsilon)
#   attempts - Number of times algorithm is run with different initial labelings
#   flags - Initialization method
```

**K-means Flags:**
```python { .api }
cv2.KMEANS_RANDOM_CENTERS      # Random initialization of cluster centers
cv2.KMEANS_PP_CENTERS          # K-means++ initialization (smart seeding)
cv2.KMEANS_USE_INITIAL_LABELS  # Use provided initial labels
```

**Termination Criteria:**
```python { .api }
# Create termination criteria
cv2.TermCriteria(type, maxCount, epsilon)

# Termination types (can be combined with bitwise OR):
cv2.TermCriteria_COUNT         # Stop after maxCount iterations
cv2.TermCriteria_EPS           # Stop when accuracy (epsilon) is reached
cv2.TermCriteria_MAX_ITER      # Alias for COUNT
```

### Training Data Preparation

```python { .api }
# Create training data container
cv2.ml.TrainData_create(samples, layout, responses[, ...]) -> trainData

# Access training data properties
TrainData.getLayout() -> retval
TrainData.getNTrainSamples() -> retval
TrainData.getNTestSamples() -> retval
TrainData.getNSamples() -> retval
TrainData.getNVars() -> retval
TrainData.getNAllVars() -> retval

# Get data splits
TrainData.getTrainSamples([, layout[, ...]]) -> retval
TrainData.getTestSamples() -> retval
TrainData.getTrainResponses() -> retval
TrainData.getTestResponses() -> retval

# Data sampling and splitting
TrainData.setTrainTestSplit(count[, shuffle]) -> None
TrainData.setTrainTestSplitRatio(ratio[, shuffle]) -> None
TrainData.shuffleTrainTest() -> None

# Variable types and missing data
TrainData.getVarType() -> retval
TrainData.setVarType(var_idx, type) -> None
TrainData.getMissing() -> retval
TrainData.getDefaultSubstValues() -> retval
```

**Variable Types:**
```python { .api }
cv2.ml.VAR_NUMERICAL          # Numerical (continuous) variable
cv2.ml.VAR_ORDERED            # Ordered categorical variable
cv2.ml.VAR_CATEGORICAL        # Unordered categorical variable
```

### Stochastic Gradient Descent SVM

```python { .api }
# Create SGD-based SVM instance
cv2.ml.SVMSGD_create() -> svmsgd

# Configure SGD parameters
SVMSGD.setOptimalParameters([, svmsgdType[, marginType]]) -> None

SVMSGD.setSvmsgdType(svmsgdType) -> None
SVMSGD.getSvmsgdType() -> retval

SVMSGD.setMarginType(marginType) -> None
SVMSGD.getMarginType() -> retval

SVMSGD.setMarginRegularization(marginRegularization) -> None
SVMSGD.getMarginRegularization() -> retval

SVMSGD.setInitialStepSize(InitialStepSize) -> None
SVMSGD.getInitialStepSize() -> retval

SVMSGD.setStepDecreasingPower(stepDecreasingPower) -> None
SVMSGD.getStepDecreasingPower() -> retval

SVMSGD.setTermCriteria(val) -> None
SVMSGD.getTermCriteria() -> retval

# Get decision function weights
SVMSGD.getWeights() -> retval
SVMSGD.getShift() -> retval
```

**SVMSGD Types:**
```python { .api }
cv2.ml.SVMSGD_SGD             # Stochastic Gradient Descent
cv2.ml.SVMSGD_ASGD            # Average Stochastic Gradient Descent
```

**Margin Types:**
```python { .api }
cv2.ml.SVMSGD_SOFT_MARGIN     # Soft margin (allows some misclassification)
cv2.ml.SVMSGD_HARD_MARGIN     # Hard margin (no misclassification allowed)
```

### Model Evaluation

```python { .api }
# Common evaluation patterns for all models

# Calculate prediction error on test set
error = model.calcError(test_data, test_flag)

# Get predictions with additional information
retval, results = model.predict(samples)

# For classifiers, check accuracy
correct_predictions = np.sum(predictions == ground_truth)
accuracy = correct_predictions / len(ground_truth)
```

**Prediction Flags:**
```python { .api }
cv2.ml.StatModel_RAW_OUTPUT        # Return raw output values
cv2.ml.StatModel_COMPRESSED_INPUT  # Input is compressed
cv2.ml.StatModel_PREPROCESSED_INPUT # Input is preprocessed
cv2.ml.StatModel_UPDATE_MODEL       # Update model during prediction
```
