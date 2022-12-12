import numpy as np

def polyfit_thru_zero(x, y, order, num_pts=500):
    """
    Fit polynomial to data such that p(x) = y which is constrained
    to go through zero, e.g. p(0) = 0. 

    args:
      x        = x-coordinates of sample points, array like shape (M,)   
      y        = y-coordinates of sample points, array like shape (M,)  
      order    = order of the polynomial fit, integer >= 1
      num_pts  = number of points at which to evaluate data.

    Returns:
      coef     = fit coefficients highest order to lowest (polyval order)
      x_fit    = x-coordinates of evaluated fit, array like (num_pts,)
      y_fit    = y-coordinates of evaluated fit, array like (num_pts,)

    """
    x_array = np.array(x)
    y_array = np.array(y)
    A = np.zeros((x_array.shape[0],order))
    for i in range(order):
        A[:,i] = x_array**(i+1)
    result = np.linalg.lstsq(A, y_array, rcond=None)
    coef = result[0]
    x_fit = np.linspace(x_array.min(), x_array.max(), num_pts)
    A_fit = np.zeros((num_pts,order))
    for i in range(order):
        A_fit[:,i] = x_fit**(i+1)
    y_fit = np.dot(A_fit,coef)
    coef_polyval = coef_to_polyval(coef)
    return coef_polyval, x_fit, y_fit

def coef_to_polyval(fit_coef):
    fit_coef_polyval = np.zeros(fit_coef.size+1)
    fit_coef_polyval[:-1] = fit_coef[::-1]
    return fit_coef_polyval
