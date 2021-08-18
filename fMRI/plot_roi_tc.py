

def plot_roi_tc(tc1,tc2,node_ind,data_file_loc,cols = ['r','b'],labels = ['S','NS']):
    #tc1 = timecourse: dims = nsubs group1,32
    #tc2 = timecourse: dims = nsubs group2,32
    #node_ind = 0-267
    #cols: colors
    
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy import stats
    from nltools.data import Brain_Data
    from nltools.mask import expand_mask, roi_to_brain

    plt.errorbar(np.arange(0,tc1.shape[1]), np.nanmedian(tc1,axis=0), stats.sem(tc1,axis=0,nan_policy='omit'), color = cols[0], label = labels[0])
    plt.errorbar(np.arange(0,tc2.shape[1]), np.nanmedian(tc2,axis=0), stats.sem(tc2,axis=0,nan_policy='omit'), color = cols[1], label = labels[1])
    plt.hlines(0,tc1.shape[1], color = 'grey')
    ymin,ymax = plt.ylim()
    plt.vlines(3,ymin,ymax, color = 'grey')
    plt.legend()
    
    shen268 = pd.read_csv(os.path.join(data_file_loc,"shen_dictionary.csv"))
    node_lbl = eval(shen268[str(node_ind+1)][0])
    print('Node label:',node_lbl['name'])

    #plot node location
    mat = np.zeros((268,))
    mat[node_ind] = 1
    mask = Brain_Data('https://neurovault.org/media/images/8423/shen_2mm_268_parcellation.nii.gz')
    mask_x = expand_mask(mask)
    img = roi_to_brain(pd.Series(mat), mask_x) 
    img.plot(colorbar=True, title = 'node'+str(node_ind+1), cmap = 'RdBu_r')