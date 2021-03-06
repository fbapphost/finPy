'''
Created on Sep 23, 2014

@author: SSethuraman
'''
'''

Piecewise cubic Hermite interpolation (monotonic...) in Python

References:

    Wikipedia:  Monotone cubic interpolation
                Cubic Hermite spline

A cubic Hermite spline is a third degree spline with each polynomial of the spline
in Hermite form.  The Hermite form consists of two control points and two control
tangents for each polynomial.  Each interpolation is performed on one sub-interval
at a time (piece-wise).  A monotone cubic interpolation is a variant of cubic
interpolation that preserves monotonicity of the data to be interpolated (in other
words, it controls overshoot).  Monotonicity is preserved by linear interpolation
but not by cubic interpolation.

Use:

There are two separate calls, the first call, pchip_slopes(),  computes the slopes that
the interpolator needs.  If there are a large number of points to compute,
it is more efficient to compute the slopes once, rather than for  every point
being evaluated.  The second call, pchip_eval(), takes the slopes computed by
pchip_slopes() along with X, Y, and a vector of desired "xnew"s and computes a vector
of "ynew"s.  If only a handful of points is needed, pchip() is a  third function
which combines a call to pchip_slopes() followed by pchip_eval().

'''
import warnings
import numpy as np
#from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from matplotlib.mlab import slopes, stineman_interp
import irvc

class cubic_spline:
    def __init__(self,x,y, order, extrapol):
        np_x = np.asarray(x,dtype=np.float64) 
        np_y = np.asarray(y, dtype=np.float64)
        self.x = np_x
        self.y = np_y
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        self.interp = InterpolatedUnivariateSpline(self.x, self.y, k=3)
    
    def interp(self, xnew):
        return self.interp(xnew)
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'
    
class exponential_fit:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        def f(x, a, b,c, d):
            return (a + b*x)*np.exp(-c*x)+d
        params, covar = curve_fit(f, self.x, self.y)
        self.params = params
        self.expf = lambda x: (self.params[0] + self.params[1]*x)*np.exp(-self.params[2]*x) + self.params[3]
            
    def interp(self, xnew):
        return self.expf(xnew)
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'
    
class corr5P_tenor1:
    def __init__(self, x, y, tenor1, factor):
        self.x = x
        self.y = y 
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        self.tenor1 = tenor1
        self.factor = factor
        
        def f(t1, f):
            def g(x):
                return str(x) + 'Y'
            return lambda x, p1, p2, p3, p4, p5: [irvc.Swaption_Corr_5P(p1, p2, p3, p4, p5, f, t1, g(i)) for i in x]
        corr_interp = f(tenor1, factor)
        params, covar = curve_fit(corr_interp, self.x, self.y)
        self.params = params
        print(self.params)
        self.corrf = lambda x: corr_interp(x, params[0], params[1], params[2], params[3], params[4])
        
    def interp(self, xnew):
        print(self.params)
        return self.corrf(xnew)[0]
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'

class corr5P_tenor2:
    def __init__(self, x, y, tenor2, factor):
        self.x = x
        self.y = y 
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        self.tenor2 = tenor2
        self.factor = factor
        
        def f(t2, f):
            def g(x):
                return str(x) + 'Y'
            return lambda x, p1, p2, p3, p4, p5: [irvc.Swaption_Corr_5P(p1, p2, p3, p4, p5, f, g(i), t2) for i in x]
        corr_interp = f(tenor2, factor)
        params, covar = curve_fit(corr_interp, self.x, self.y)
        self.params = params
        print(self.params)
        self.corrf = lambda x: corr_interp(x, params[0], params[1], params[2], params[3], params[4])
        
    def interp(self, xnew):
        print(self.params)
        return self.corrf(xnew)[0]
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'


class corr3P_tenor1:
    def __init__(self, x, y, tenor1):
        self.x = x
        self.y = y 
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        self.tenor1 = tenor1
        
        def f(t1):
            def g(x):
                return str(x) + 'Y'
            return lambda x, p1, p2, p3, p4, p5: [irvc.Swaption_Corr_SC3(p1, p2, p3, t1, g(i)) for i in x]
        corr_interp = f(tenor1)
        params, covar = curve_fit(corr_interp, self.x, self.y)
        self.params = params
        print(self.params)
        self.corrf = lambda x: corr_interp(x, params[0], params[1], params[2])
        
    def interp(self, xnew):
        print(self.params)
        return self.corrf(xnew)[0]
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'
    
class corr3P_tenor2:
    def __init__(self, x, y, tenor2):
        self.x = x
        self.y = y 
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        self.tenor2 = tenor2
        
        def f(t2):
            def g(x):
                return str(x) + 'Y'
            return lambda x, p1, p2, p3, p4, p5: [irvc.Swaption_Corr_SC3(p1, p2, p3, g(i), t2) for i in x]
        corr_interp = f(tenor2)
        params, covar = curve_fit(corr_interp, self.x, self.y)
        self.params = params
        print(self.params)
        self.corrf = lambda x: corr_interp(x, params[0], params[1], params[2])
        
    def interp(self, xnew):
        print(self.params)
        return self.corrf(xnew)[0]
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'
         
class cubic_monotone:
    def __init__(self,x,y):
        np_x = np.asarray(x,dtype=np.float64) 
        np_y = np.asarray(y, dtype=np.float64)
        self.m = pchip_slopes(np_x,np_y)
        self.x = np_x
        self.y = np_y
        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)
        #print(self.x)
        #print(self.y)

    def interp(self, xnew):
        #x_n = np.asarray(xnew, dtype=np.float64)
        x_n =  xnew
        ynew =  pchip_eval(self.x, self.y, self.m, x_n)
        return ynew
    
    def get_xbound(self, param):
        if param == 'min':
            return self.xmin
        elif param == 'max':
            return self.xmax
        else:
            return 'err'
    
    def update(self, ynew):
        self.y = np.asarray(ynew, dtype=np.float64)
        self.m = pchip_slopes(self.x, self.y)


#=========================================================
def pchip(x, y, xnew):

    # Compute the slopes used by the piecewise cubic Hermite  interpolator
    m = pchip_slopes(x, y)
    
    # Use these slopes (along with the Hermite basis function) to  interpolate
    ynew = pchip_eval(x, y, m, xnew)
    
    return ynew

#=========================================================
def x_is_okay(x,xvec):
    # Make sure "x" and "xvec" satisfy the conditions for
    # running the pchip interpolator
    
    n = x.size
    m = xvec.size
    
    # Make sure "x" is in sorted order (brute force, but works...)
    xx = x.copy()
    xx.sort()
    total_matches = (xx == x).sum()
    if total_matches != n:
        warnings.warn( "x values weren't in sorted order --- aborting")
        return False
    
    # Make sure 'x' doesn't have any repeated values
    delta = x[1:] - x[:-1]
    if (delta == 0.0).any():
        warnings.warn( "x values weren't monotonic--- aborting")
        return False
    
    # Check for in-range xvec values (beyond upper edge)
    check = xvec > x[-1]
    if check.any():
        #print("*" * 50)
        #print "x_is_okay()"
        #print "Certain 'xvec' values are beyond the upper end of 'x'"
        #print "x_max = ", x[-1]
        indices = np.compress(check, range(m))
        #print "out-of-range xvec's = ", xvec[indices]
        #print "out-of-range xvec indices = ", indices
        #return False - changes the value to True to make it extrapolating
        return True
    
    # Second - check for in-range xvec values (beyond lower edge)
    check = xvec< x[0]
    if check.any():
        #print "*" * 50
        #print "x_is_okay()"
        #print "Certain 'xvec' values are beyond the lower end of 'x'"
        #print "x_min = ", x[0]
        indices = np.compress(check, range(m))
        #print "out-of-range xvec's = ", xvec[indices]
        #print "out-of-range xvec indices = ", indices
        #return False - changed the value to True to make it extrapolating
        return True
    
    return True

#=========================================================
def pchip_eval(x, y, m, xvec):
    '''
     Evaluate the piecewise cubic Hermite interpolant with  monoticity preserved
    
        x = array containing the x-data
        y = array containing the y-data
        m = slopes at each (x,y) point [computed to preserve  monotonicity]
        xnew = new "x" value where the interpolation is desired
    
        x must be sorted low to high... (no repeats)
        y can have repeated values
    
     This works with either a scalar or vector of "xvec"
    '''

    if type(x) == 'numpy.float64':
        n = max(x.shape)
    else:
        n = len(x)
    
    if hasattr(xvec, '__len__'):
        mm = len(xvec)
    else:
        #print(len(xvec))
        mm = 1
    
    ############################
    # Make sure there aren't problems with the input data
    ############################
    if not x_is_okay(x, xvec):
        #print "pchip_eval2() - ill formed 'x' vector!!!!!!!!!!!!!"
    
        # Cause a hard crash...
        return #STOP_pchip_eval2
    
    # Find the indices "k" such that x[k] < xvec < x[k+1]
    
    # Create "copies" of "x" as rows in a mxn 2-dimensional vector
    xx = np.resize(x,(mm,n)).transpose()
    xxx = xx >= xvec
    
    # Compute column by column differences
    z = xxx[:-1,:] - xxx[1:,:]
    
    # Collapse over rows...
    k = z.argmax(axis=0)
    
    # Create the Hermite coefficients
    h = x[k+1] - x[k]
    t = (xvec - x[k]) / h
    
    # Hermite basis functions
    h00 = (2 * t**3) - (3 * t**2) + 1
    h10 =      t**3  - (2 * t**2) + t
    h01 = (-2* t**3) + (3 * t**2)
    h11 =      t**3  -      t**2
    
    # Compute the interpolated value of "y"
    ynew = h00*y[k] + h10*h*m[k] + h01*y[k+1] + h11*h*m[k+1]
    
    return ynew

#=========================================================
def pchip_slopes(x,y, kind='secant', tension=0, monotone=True):
    '''
    Return estimated slopes y'(x) 
    
    Parameters
    ----------
    x, y : array-like
        array containing the x- and y-data, respectively.
        x must be sorted low to high... (no repeats) while
        y can have repeated values.
    kind : string
        defining method of estimation for yp. Valid options are:
        'secant' average secants 
            yp = 0.5*((y[k+1]-y[k])/(x[k+1]-x[k]) + (y[k]-y[k-1])/(x[k]-x[k-1]))
        'Catmull-Rom'  yp = (y[k+1]-y[k-1])/(x[k+1]-x[k-1])
        'Cardinal'     yp = (1-tension) * (y[k+1]-y[k-1])/(x[k+1]-x[k-1])
    tension : real scalar between 0 and 1.
        tension parameter used in Cardinal method
    monotone : bool
        If True modifies yp to preserve monoticity
    
    x input conditioning is assumed but not checked
    '''
    n = len(x)
    
    # Compute the slopes of the secant lines between successive points
    delta = (y[1:] - y[:-1]) / (x[1:] - x[:-1])
    
    # Initialize the tangents at every points as the average of the  secants
    m = np.zeros(n, dtype='d')
    
    # At the endpoints - use one-sided differences
    m[0] = delta[0]
    m[n-1] = delta[-1]
    method = kind.lower()
    if method.startswith('secant'):
        # In the middle - use the average of the secants
        m[1:-1] = (delta[:-1] + delta[1:]) / 2.0
    else: # Cardinal or Catmull-Rom method
        m[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
        if method.startswith('cardinal'):
            m = (1-tension) * m
       
    if monotone:
        # Special case: intervals where y[k] == y[k+1]     
        # Setting these slopes to zero guarantees the spline connecting
        # these points will be flat which preserves monotonicity
        indices_to_fix = np.compress((delta == 0.0), range(n))
        for ii in indices_to_fix:
            m[ii]   = 0.0
            m[ii+1] = 0.0
        
        alpha = m[:-1]/delta
        beta  = m[1:]/delta
        dist  = alpha**2 + beta**2
        tau   = 3.0 / np.sqrt(dist)
        
        # To prevent overshoot or undershoot, restrict the position vector
        # (alpha, beta) to a circle of radius 3.  If (alpha**2 +  beta**2)>9,
        # then set m[k] = tau[k]alpha[k]delta[k] and m[k+1] =  tau[k]beta[b]delta[k]
        # where tau = 3/sqrt(alpha**2 + beta**2).
        
        # Find the indices that need adjustment
        over = (dist > 9.0)
        indices_to_fix = np.compress(over, range(n)) 
        for ii in indices_to_fix:
            m[ii]   = tau[ii] * alpha[ii] * delta[ii]
            m[ii+1] = tau[ii] * beta[ii]  * delta[ii]
    
    return m

#========================================================================
def CubicHermiteSpline(x, y, xnew):
    '''
    Piecewise Cubic Hermite Interpolation using Catmull-Rom
    method for computing the slopes.
    '''
    # Non-montonic cubic Hermite spline interpolator using
    # Catmul-Rom method for computing slopes...
    m = pchip_slopes(x, y, kind='catmull', monotone=False)
    
    # Use these slopes (along with the Hermite basis function) to  interpolate
    ynew = pchip_eval(x, y, m, xnew)
    
    return ynew

  

#==============================================================
def main():
    ############################################################
    # Sine wave test
    ############################################################
    
    # Create a example vector containing a sine wave.
    x = np.arange(30.0)/10.
    y = np.sin(x)
    
    # Interpolate the data above to the grid defined by "xvec"
    xvec = np.arange(250.)/100.
    
    # Initialize the interpolator slopes
    m = pchip_slopes(x,y)
    m1 = slopes(x, y)
    m2  = pchip_slopes(x,y,kind='catmul',monotone=False)
    # Call the monotonic piece-wise Hermite cubic interpolator
    yvec2 = pchip_eval(x, y, m, xvec)
    
    plt.figure(1)
    plt.plot(x,y, 'ro')
    plt.title("pchip() Sin test code")
    
    # Plot the interpolated points
    plt.plot(xvec, yvec2, 'b')
    
     
    
    # Step function test...
    plt.figure(2)
    plt.title("pchip() step function test")
    
    # Create a step function (will demonstrate monotonicity)
    x = np.arange(7.0) - 3.0
    y = np.array([-1.0, -1,-1,0,1,1,1])
    
    # Interpolate using monotonic piecewise Hermite cubic spline
    xvec = np.arange(599.)/100. - 3.0
    
    # Create the pchip slopes
    m  = pchip_slopes(x,y)
    m1 = slopes(x, y)
    m2  = pchip_slopes(x,y,kind='catmul',monotone=False)
    # Interpolate...
    yvec = pchip_eval(x, y, m, xvec)
    
    # Call the Scipy cubic spline interpolator
    from scipy.interpolate import interpolate
    function = interpolate.interp1d(x, y, kind='cubic')
    yvec2 = function(xvec)
    
    # Non-montonic cubic Hermite spline interpolator using
    # Catmul-Rom method for computing slopes...
    yvec3 = CubicHermiteSpline(x,y, xvec)
    
    
    yvec4 = stineman_interp(xvec, x, y, m)
    
    # Plot the results
    plt.plot(x,    y,     'ro')
    plt.plot(xvec, yvec,  'b')
    plt.plot(xvec, yvec2, 'k')
    plt.plot(xvec, yvec3, 'g')
    plt.plot(xvec, yvec4, 'm')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Comparing pypchip() vs. Scipy interp1d() vs. non-monotonic CHS")
    legends = ["Data", "pypchip()", "interp1d","CHS", 'SI']
    plt.legend(legends, loc="upper left")
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    ###################################################################
    main()
