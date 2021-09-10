

def ttest_diffmovies(movieTC_yes, movieTC_no, plot_fig = 0, plot_type = 'diff',single_plot = 0,tr0_ind =3):
    #This function performs an unpaired t-test between yes and no for each timepoint of a
    # single node and movie    
    # old name of fn: responses_ttest(....)
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats

    nt = movieTC_yes.shape[1]
    thr = 0.05 # pvalue threshold
    #print("nr. of timepts:",nt)
    tscore = np.empty((nt,))
    tscore[:] = np.nan
    
    pval = np.empty((nt,))
    pval[:] = np.nan
    
    for imno in np.arange(tr0_ind,tr0_ind+28): #time.
    #for imno in np.arange(3,nt-1): #time
        tscore[imno],pval[imno] = stats.ttest_rel(movieTC_yes[:,imno], \
                                                   movieTC_no[:,imno], nan_policy='omit')
        pval[imno] = np.round(pval[imno],2)
        
    #print(pval)
    #print(np.where(pval < thr))
    #np.nanmean(movieTC_yes[:,imno])
    ts =   [ np.where(pval[tr0_ind:] <= thr)[0], \
          np.sign(tscore[tr0_ind + np.where(pval[tr0_ind:] <= thr)[0]])]
    #print(ts)
    # t=0 is t=0 in ts too
    
    #print('diff:',np.nanmedian(movieTC_yes-movieTC_no,axis=0))
            
    #plot_fig = 1
    if plot_fig:

        if plot_type == 'both':
            plt.errorbar(np.arange(nt),np.nanmedian(movieTC_yes,axis=0),
                         stats.sem(movieTC_yes,axis=0,nan_policy='omit'),color = 'r')
            plt.errorbar(np.arange(nt),np.nanmedian(movieTC_no,axis=0),
                         stats.sem(movieTC_no,axis=0,nan_policy='omit'),color = 'b')
        elif plot_type[:4] == 'diff':
            if single_plot==1: # plot all tcs on one single plot
                alpha = .1
            else: # plot mean with errorbars
                alpha = 1
            plt.plot(np.arange(nt),np.nanmedian(movieTC_yes-movieTC_no,axis=0),color = 'k',alpha = alpha)
            
    if plot_fig:
        ymin,ymax = plt.ylim()
        if plot_type == 'both':
            #plt.plot(ts[0]+tr0_ind,np.repeat(1.1*ymax,len(ts[0])),color = 'magenta',marker = '*',ls = 'none')
            inds = np.where(pval<=.001)[0]
            plt.plot(inds,np.repeat(1.1*ymax,len(inds)),color = 'magenta',marker = '*',ls = 'none',
                    label = 'p<.001')
            inds = np.where((pval<=.05)&(pval>.001))[0]
            plt.plot(inds,np.repeat(1.1*ymax,len(inds)),color = 'k',marker = '*',ls = 'none',
                    label = 'p<.05')

        plt.vlines(tr0_ind,ymin,ymax,color = 'grey')
        plt.hlines(0,0,32,color ='grey')
        plt.xticks(np.arange(0,31,6),[str(i) for i in np.arange(0,31,6)-tr0_ind])
        #if len(ts[0]>0):
        #    plt.vlines(ts[0][0],ymax-.1*(ymax-ymin),ymax,color = 'magenta')
        #plt.legend()
             
    return ts
        
    
    
    
def ttest_samemovies(movieTC_yes, movieTC_no, plot_fig = 0, plot_type = 'diff',single_plot = 0,tr0_ind =3):
    #This function performs an unpaired t-test between yes and no for each timepoint of a
    # single node and movie    
    # old name of fn: responses_ttest(....)
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats

    nt = movieTC_yes.shape[1]
    thr = 0.05 # pvalue threshold
    #print("nr. of timepts:",nt)
    tscore = np.empty((nt,))
    tscore[:] = np.nan
    
    pval = np.empty((nt,))
    pval[:] = np.nan
    
    for imno in np.arange(tr0_ind,tr0_ind+28): #time.
    #for imno in np.arange(3,nt-1): #time
        tscore[imno],pval[imno] = stats.ttest_ind(movieTC_yes[:,imno], \
                                                   movieTC_no[:,imno], equal_var=False,
                                                  nan_policy='omit')
        pval[imno] = np.round(pval[imno],2)
        
    #print(pval)
    #print(np.where(pval < thr))
    #np.nanmean(movieTC_yes[:,imno])
    
    ts = [ np.where(pval[tr0_ind:] <= thr)[0], \
          np.sign(tscore[tr0_ind + np.where(pval[tr0_ind:] <= thr)[0]])]
    #print(ts)
    # t=0 is t=0 in ts too
    
    #print('diff:',np.nanmedian(movieTC_yes-movieTC_no,axis=0))
            
    #plot_fig = 1
    if plot_fig:

        if plot_type == 'both':
            plt.errorbar(np.arange(nt),np.nanmedian(movieTC_yes,axis=0),
                         stats.sem(movieTC_yes,axis=0,nan_policy='omit'),color = 'r')
            plt.errorbar(np.arange(nt),np.nanmedian(movieTC_no,axis=0),
                         stats.sem(movieTC_no,axis=0,nan_policy='omit'),color = 'b')
        elif plot_type[:4] == 'diff':
            if single_plot==1: # plot all tcs on one single plot
                alpha = .1
            else: # plot mean
                alpha = 1
            plt.plot(np.arange(nt),np.nanmedian(movieTC_yes,axis=0)-np.nanmedian(movieTC_no,axis=0),
                    color = 'k',alpha = alpha)
            
    if plot_fig:
        ymin,ymax = plt.ylim()
        if plot_type == 'both':
            #plt.plot(ts[0]+tr0_ind,np.repeat(1.1*ymax,len(ts[0])),color = 'magenta',marker = '*',ls = 'none')
            inds = np.where(pval<=.001)[0]
            plt.plot(inds,np.repeat(1.1*ymax,len(inds)),color = 'magenta',marker = '*',ls = 'none',
                    label = 'p<.001')
            inds = np.where((pval<=.05)&(pval>.001))[0]
            plt.plot(inds,np.repeat(1.1*ymax,len(inds)),color = 'k',marker = '*',ls = 'none',
                    label = 'p<.05')
        
        

        plt.vlines(tr0_ind,ymin,ymax,color = 'grey')
        plt.hlines(0,0,32,color ='grey')
        plt.xticks(np.arange(0,31,6),[str(i) for i in np.arange(0,31,6)-tr0_ind])
        #if len(ts[0]>0):
        #    plt.vlines(ts[0][0],ymax-.1*(ymax-ymin),ymax,color = 'magenta')
        #plt.legend()
             
    return ts
                 