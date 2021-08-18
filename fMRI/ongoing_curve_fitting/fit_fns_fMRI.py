# RUN THIS CELL

from lmfit.models import StepModel, LinearModel, SineModel
from lmfit import Model

def hello():
    print('Hello 3!')

def fit_goodness_test_fn(y,best_fit):
    # function returns R-squared value  (defined as 1 - ratio  of residual to 
    # total variance's sums of squares) 
    # for a given timecourse "y" and fit result "result"
   
    import numpy as np
    
    res = y- best_fit
    ss_res = np.sum((res - np.mean(res))** 2)# or ss_res = res.var()
    ss_tot = np.sum((y   - np.mean(y))  ** 2)# or ss_tot = y.var()
    
    r2 = 1 - (ss_res / ss_tot)
    #print('r2: ', r2)
    
    return r2


def logfit_fn(y,plot_fig=0):
    # computes the best fit using a logistic function for a timecourse y
    # Returns best fit parameters that are above the rsquared threshold r2_thr,
    # keys (i.e., param names), rsq and aic.
    #plot_fig =0 (don't plot) or 1 (plot)
    
    from lmfit.models import StepModel
    import numpy as np
    import matplotlib.pyplot as plt
    
    #model = Model(logistic_function)#,nan_policy = 'omit') # set model here
    #model.set_param_hint('A', min=-1, max = 1) # set a parameter's range here
    #model.set_param_hint('c', min=2, max = 25)
    #model.set_param_hint('s', min=.1, max = 500)
    #params = model.make_params(c=np.argmax(np.diff(y)), 
    #                               A = max(y)-min(y), s = 1)  # set initial parameter value here
    
    model = StepModel(form='logistic') # set model here
    model.set_param_hint('amplitude', min=-1.5*(max(y)-min(y)), max = 1.5*(max(y)-min(y)))
    model.set_param_hint('center', min=4, max = 24)
    model.set_param_hint('sigma', min=.1, max = 10)
   
    params = model.make_params(amplitude=max(y)-min(y),
                               center=np.argmax(np.diff(y)),
                                   sigma = 1 )  # set initial parameter value here
    
    result = model.fit(y, params, x=np.arange(0,28))
    
        
    param_keys = list(result.best_values.keys()) # A,c,s for logisticfn
    param_keys.remove('form')
    params_best = np.zeros((len(param_keys),))
    r2 = fit_goodness_test_fn(y, result.best_fit)
    
    if plot_fig:
        result.plot()
        plt.suptitle('Logistic,Rsq='+str(np.round(r2,2)),fontweight = 'bold')
    
    for pind,pname in enumerate(param_keys):
        params_best[pind] = result.best_values[pname] 
        
    return params_best,param_keys,r2,result.aic, result


def sinefit_fn(y,plot_fig=0):
    # computes the best fit using a sinusoidal function for a timecourse y
    # Returns best fit parameters that are above the rsquared threshold r2_thr,
    # keys (i.e., param names), rsq and aic.
    #plot_fig =0 (don't plot) or 1 (plot)
    
    from lmfit.models import SineModel
    import numpy as np

    import matplotlib.pyplot as plt
    
    from scipy.signal import find_peaks
    
    model = SineModel() # set function here
    
    model.set_param_hint('amplitude', min = 1e-3,max = 1) # set param range here
    model.set_param_hint('frequency', min = .5, max = 3)
    
    peak,_ = find_peaks(np.abs(y),height= max(np.abs(y))/2)
    #print(peak)
    if len(peak) > 0:
        if y[peak[0]] > 0:
            ph = 0
        else:
            ph = np.pi
        init_amp = abs(y[peak[0]])
        init_freq =  len(peak)/2
    else:
        ph = 0
        init_amp = .5
        init_freq =  1
    
    params = model.make_params(amplitude = init_amp, frequency = init_freq,
                               shift = ph ) # set initial param values here
    #y = y[5:]
    #print('y=',y,'\namp init=',max(y, key=abs))
    result = model.fit(y, params, x=np.linspace(0,2*np.pi,len(y)))
    param_keys = list(result.best_values.keys()) # E.g. A,freq,ph
    params_best = np.zeros((len(param_keys),))
    r2 = fit_goodness_test_fn(y, result.best_fit)
    if plot_fig:
        result.plot()
        plt.suptitle('Sinusoidal, Rsq='+str(np.round(r2,2)),fontweight = 'bold')
    #print(result.best_values)
    for pind,pname in enumerate(param_keys):
        params_best[pind] = result.best_values[pname]
        
    return params_best,param_keys, r2, result.aic, result



def gaussianfit_fn(y,plot_fig=0):
    # computes the best fit using a gaussian function (for early peak-timecourses) for a timecourse y
    # Returns best fit parameters that are above the rsquared threshold r2_thr,
    # keys (i.e., param names), rsq and aic.
    #plot_fig =0 (don't plot) or 1 (plot)
    
    from lmfit.models import GaussianModel
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    model = GaussianModel()  # set model here
    
    if y[np.argmax(np.abs(y))] < 0:
        minval = -2*np.pi*5*(max(y)-min(y))
        maxval = -1e-10
        #maxval = -2*np.pi*5*(max(y)-min(y))/10
        init_amp = -2*np.pi*max(np.abs(y))
    else:
        #minval = 2*np.pi*5*(max(y)-min(y))/10
        minval = 1e-10
        maxval = 2*np.pi*5*(max(y)-min(y))
        init_amp = 2*np.pi*max(np.abs(y))
    
    model.set_param_hint('amplitude', min=minval, max = maxval) # set parameter ranges here
    model.set_param_hint('center', min = 3, max = 25)
    model.set_param_hint('sigma', min=.1, max = 10)
    
    params = model.make_params(amplitude = init_amp, center = np.argmax(np.abs(y)),
                               sigma = 1) # set initial param values here
    
    result = model.fit(y, params, x=np.arange(0,28))
    param_keys = list(result.best_values.keys()) # E.g. A,freq,ph
    params_best = np.zeros((len(param_keys),))
    r2 = fit_goodness_test_fn(y, result.best_fit)
    if plot_fig:
        result.plot()
        plt.suptitle('Gaussian, Rsq='+ str(np.round(r2,2)),fontweight = 'bold')    
    #print(result.best_values)
    
    for pind,pname in enumerate(param_keys):
        params_best[pind] = result.best_values[pname]
        
    return params_best,param_keys, r2, result.aic, result

def delayed_sin(x, step_onset, amp, freq, phase):
#def delayed_sin(x, step_size = .01, step_onset = 5, amp=.5, freq=1, phase=3.14):
    import numpy as np
    y = np.zeros((len(x),))
    nonzero_ind = np.arange(int(step_onset),len(x))
    for i in nonzero_ind: # e.g. 5 to 28
        if np.round(phase*100)-np.round(np.pi*100)<1:
            y[i] = amp * np.sin(freq*(x[i]-x[nonzero_ind[0]])+phase)
        # print(y[i])
    return y
    
def stepsine_fn(y, plot_fig=0):

    from lmfit.models import Model
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks
    
    model = Model(delayed_sin)
    #model.set_param_hint('step_size', min=  -.2, max = .2)
    
    factor = 5 # arbitrary yoffset threshold. If i<maxdelay and y(i) < max(y)/factor, they're considered
    maxdelay = 6 # the delay is usually < 6 TRs based on manual examination
    
    peak,_ = find_peaks(np.abs(y),height= max(np.abs(y))/4) # return peak locations
    #print(peak)
    if len(peak) > 0:
        if y[peak[0]] > 0:
            ph = 0
        else:
            ph = np.pi
        init_amp = max(abs(y))
        
    else:
        ph = 0
        init_amp = .5
      
    init_freq = 1
   
    i = np.where(y<(np.nanmean(abs(y))/factor))[0]
    i = i[i<maxdelay]
    i = max(i)
    # to set the initial step_onset value. Thresholds are a bit arbitrary based on eyeballing the mean curves.
    # can change if there's a more objective way of doing this.
    
    model.set_param_hint('step_onset', min=2, max = maxdelay)
    model.set_param_hint('amp', min=1e-3, max = max(y)-min(y))
    model.set_param_hint('freq', min=.5, max = 2.5)
    model.set_param_hint('phase', min=0, max = np.pi)
    #sum_is = [sum(y[0:i]) for i in len(y)]
    # to determine if the first big peak is positive or negative
    #print('init:',i,init_amp,init_freq,ph)
    
    params = model.make_params(step_onset=i, amp = init_amp, freq = init_freq, phase = ph)

    result = model.fit(y, params, x=np.linspace(0,2*np.pi,28))
    param_keys = list(result.best_values.keys()) # E.g. A,freq,ph
    params_best = np.zeros((len(param_keys),))
    r2 = fit_goodness_test_fn(y, result.best_fit)
    if plot_fig:
        result.plot()
        plt.suptitle('Step sine, Rsq='+ str(np.round(r2,2)),fontweight = 'bold')    
    #print(result.best_values)
    
    for pind,pname in enumerate(param_keys):
        params_best[pind] = result.best_values[pname]
        
    return params_best,param_keys, r2, result.aic, result

