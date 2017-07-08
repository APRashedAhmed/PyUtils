# ML and Data centric helper functions
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sklearn
import numpy as np

from sklearn.utils import assert_all_finite, as_float_array, check_X_y
from sklearn.preprocessing import LabelBinarizer

################################################################################
#                            Scikit-Learn Functions                            #
################################################################################


def shuffle_data(X, y, random_state=0, n_samples=None):
    """Performs a shape tets on the data then shuffles correctly.
    
    Args:
        X (indexable): X array containing the data.
        y (indexable): y array containing labels.
        random_state (int): Control the shuffling for reproducible behavior.
        n_samples (int, None): Number of samples to generate. If left to None 
            this is automatically set to the first dimension of the arrays.

    Returns:
        X (indexable). A shuffled version of the inputted X.
        y (indexable). A shuffled version of the inputted y.
    """
    sklearn.utils.check_X_y(X, y)
    return sklearn.utils.shuffle(
        X, y, random_state=random_state, n_samples=n_samples)

def split_data(X, y, test_size=None, train_size=None, random_state=0, 
               stratify=None):
    """Performs a shape test then splits the data according to the inputted 
    percentages.
    
    Args:
        X (indexable): X array containing the data.
        y (indexable): y array containing labels.
        test_size (float, int, None): If float, should be between 0.0 and 1.0 
            and represent the proportion of the dataset to include in the test 
            split. If int, represents the absolute number of test samples. If 
            None, the value is automatically set to the complement of the train 
            size. If train size is also None, test size is set to 0.25.
        train_size (float, int, None): If float, should be between 0.0 and 1.0 
            and represent the proportion of the dataset to include in the train 
            split. If int, represents the absolute number of train samples. If 
            None, the value is automatically set to the complement of the test 
            size
        random_state (int): Control the shuffling for reproducible behavior.
        stratify (array-like or None): If not None, data is split in a 
            stratified fashion, using this as the class labels.

    Returns:
        X_train (indexable): X array containing the training data.
        X_test (indexable): X array containing the testing data.
        y_train (indexable): y array containing training labels.
        y_test (indexable): y array containing testing labels.
    """
    sklearn.utils.check_X_y(X, y)
    return sklearn.model_selection.train_test_split(
        X, y, test_size=test_size, train_size=train_size, 
        random_state=random_state, stratify=stratify)

def binarize(y, pos_label=1, neg_label=0, classes=None):
    """Binarizes a vector in a one-vs-all fashion.

    Args:
        y (np.ndarray): Vector to be binarized.
        pos_label (int): Value with which positive labels must be encoded.
        neg_label (int): Value with which negative labels must be encoded.

    Returns:
        Binary Array (np.ndarray): Resulting binary array denoting the classes.
    """
    lb = MyLabelBinarizer()
    # There are issues here that need to be investigated with the classes. There 
    # doesnt seem to be any way to correctly assign the labels to a y. 
    try:
        lb.fit(classes)
    except ValueError:
        lb.fit(y)
    return lb.transform(y)

def inverse_binarize(y_binary, classes=None):
    """Inverse binarizes a vector in a one-vs-all fashion. Will return an 
    enumeration if no classes are provided.

    Args:
        y (np.ndarray): Vector to be binarized.
        classes (iterable): Iterable of y vector classes.
    Returns:
        Class Vector (np.ndarray): Vector containing the classes
    """
    lb = MyLabelBinarizer()
    try:
        lb.fit(classes)
    except ValueError:
        lb.fit(range(y_binary.shape[1]))
    return lb.inverse_transform(y_binary)

def confusion_mat(y_true, y_pred, labels=None, sample_weights=None):
    """Compute confusion matrix to evaluate the accuracy of a classification.

    Args:
        y_true (np.ndarray): Ground truth array.
        y_pred (np.ndarray): Predicted values array.
        labels (list): List of classification labels.
        sample_weight (np.ndarray): Sample weights.

    Returns:
        confusion_mat (np.ndarray): Matrix of size n_labels x n_labels showing
            confusion.
    """
    sklearn.utils.check_X_y(y_true, y_pred)
    sklearn.utils.assert_all_finite(y_true)
    sklearn.utils.assert_all_finite(y_pred)
    return sklearn.metrics.confusion_matrix(y_true, y_pred, labels=labels,
                                            sample_weights=sample_weights)
    

def nan_to_num(*args):
    """Replace nan with zero and inf with finite numbers.
    
    Args:
        *args (np.ndarrays): Sequence of np arrays to convert.

    Returns:
        tuple. The inputted arrays but with nans and infs converted.

    Returns an array or scalar replacing Not a Number (NaN) with zero, 
    (positive) infinity with a very large number and negative infinity with a 
    very small (or negative) number.
    """
    return tuple(np.nan_to_num(arg) for arg in args)
        
def check_data(X, y):
    """Runs some basic checks on the data for input validation and then converts
    the array to floats.

    Args:
        X (indexable): X array containing the data.
        y (indexable): y array containing labels.

    Returns:
        X (indexable): X array containing the data converted to floats.
        y (indexable): y array containing labels converted to floats.
    """
    assert_all_finite(X)
    assert_all_finite(y)
    check_X_y(X, y)
    return as_float_array(X), as_float_array(y)


################################################################################
#                             Scikit-Learn Classes                             #
################################################################################

class MyLabelBinarizer(LabelBinarizer):
    def transform(self, y):
        y_binary = super(MyLabelBinarizer, self).transform(y)
        if self.y_type_ == 'binary':
            return np.hstack((y_binary, 1-y_binary))
        else:
            return y_binary

    def inverse_transform(self, y_binary, threshold=None):
        if self.y_type_ == 'binary':
            return super(MyLabelBinarizer, self).inverse_transform(
                y_binary[:, 0], threshold)
        else:
            return super(MyLabelBinarizer, self).inverse_transform(
                y_binary, threshold)
