import numpy as np
from scipy import misc
from labfuns import *
import random

def mlParams(X, labels, W=None):
    assert(X.shape[0]==labels.shape[0])
    Npts,Ndims = np.shape(X)
    classes = np.unique(labels)
    Nclasses = np.size(classes)

    if W is None:
        W = np.ones((Npts,1))/float(Npts)

    mu = np.zeros((Nclasses,Ndims))
    sigma = np.zeros((Nclasses,Ndims,Ndims))

    for i, k in enumerate(classes):
        # current c, find the indices within labels to obtain x_i where x_i is labled as c 
        idx = np.where(labels == k)[0]
        # Obtain N_k x d matrix
        X_k = X[idx] 
        N_k = len(idx) 
        mu_k = np.average(X_k)
        sigma_k = np.average((X_k-mu_k)**2)
        mu[i, :] = mu_k
        sigma[i, :, :] = sigma_k
    return mu, sigma

X, labels = genBlobs(centers=5)
mu, sigma = mlParams(X,labels)
plotGaussian(X,labels,mu,sigma)


# NOTE: you do not need to handle the W argument for this part!
# in: labels - N vector of class labels
# out: prior - C x 1 vector of class priors
def computePrior(labels, W=None):
    Npts = labels.shape[0]
    if W is None:
        W = np.ones((Npts,1))/Npts
    else:
        assert(W.shape[0] == Npts)
    classes = np.unique(labels)
    Nclasses = np.size(classes)

    prior = np.zeros((Nclasses,1))


    for i, k in enumerate(classes):
        idx = np.where(labels == k)
        prior[i] = len(idx) / float(len(labels))

    return prior

# in:      X - N x d matrix of M data points
#      prior - C x 1 matrix of class priors
#         mu - C x d matrix of class means (mu[i] - class i mean)
#      sigma - C x d x d matrix of class covariances (sigma[i] - class i sigma)
# out:     h - N vector of class predictions for test points
def classifyBayes(X, prior, mu, sigma):

    Npts = X.shape[0]
    Nclasses,Ndims = np.shape(mu)
    logProb = np.zeros((Nclasses, Npts))

    # TODO: fill in the code to compute the log posterior logProb!
    # ==========================
    
    # ==========================
    
    # one possible way of finding max a-posteriori once
    # you have computed the log posterior
    for i in range(Nclasses):
        mu_k = mu[i, :]
        sigma_k = np.diag(sigma[j, :, :])

        term1 = -0.5 * np.sum(np.log(sigma_k))

        diff = X - mu_k

        term2 = -0.25 * np.sum((diff**2)/sigma_k, axis=1)
        term3 = np.log(prior[i])
        logProb[i,:] = term1 + term2 + term3

    h = np.argmax(logProb,axis=0)
    return h

