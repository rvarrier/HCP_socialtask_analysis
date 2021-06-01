def get_roi_info(labels, nodes_list, pnum):

    import pandas as pd
    import numpy as np
    
    flname = r"/Users/f0053cz/Dropbox (Dartmouth College)/postdoc_Dartmouth/shen_roi_info_files/xilin_268parc_labels.csv"
    
    list_temp = ['gui_Lobes','gui_BrodLabels','gui_Networks']
    roi_breakdown = {}
    for n in list_temp:
        roi_breakdown[n] = []
        
    roi_breakdown['gui_Lobes'] = {
        1: 'R-Prefrontal',
        2: 'R-MotorStrip',  3: 'R-Insula',
        4: 'R-Parietal',    5: 'R-Temporal',
        6: 'R-Occipital',   7: 'R-Limbic',
        8: 'R-Cerebellum',  9: 'R-Subcortical',
        10: 'R-Brainstem', 11: 'L-Prefrontal',
        12: 'L-MotorStrip',13: 'L-Insula',
        14: 'L-Parietal',  15: 'L-Temporal',
        16: 'L-Occipital', 17: 'L-Limbic',
        18: 'L-Cerebellum',19: 'L-Subcortical',
        20: 'L-Brainstem' };

    roi_breakdown['gui_BrodLabels'] = {1 : 'PrimSensory (1)',   4 : 'PrimMotor (4)',
        5 : 'SensoryAssoc (5)',  6 : 'BA6',
        7 : 'BA7',              8 : 'BA8',
        9 : 'BA9',              10 : 'BA10',
        11 : 'BA11',            13 : 'Insula (13)',
        14 : 'BA14',            17 : 'PrimVisual (17)',
        18 : 'VisualAssoc (18)', 19 : 'BA19',
        20 : 'BA20',            21 : 'BA21',
        22 : 'BA22',            23 : 'BA23',
        24 : 'BA24',            25 : 'BA25',
        30 : 'BA30',            31 : 'BA31',
        32 : 'BA32',            34 : 'BA34',
        36 : 'Parahip (36)',     37 : 'Fusiform (37)',
        38 : 'BA38',            39 : 'BA39',
        40 : 'BA40',            41 : 'PrimAuditory (41)',
        44 : 'BA44',            45 : 'BA45',
        46 : 'BA46',            47 : 'BA47',
        48 : 'Caudate (48)',     49 : 'Putamen (49)',
        50 : 'Thalamus (50)',    51 : 'GlobPal (51)',
        52 : 'NucAccumb (52)',   53 : 'Amygdala (53)',
        54 : 'Hippocampus (54)', 55 : 'Hypothalamus (55)',
        58 : 'BrainStem',        57 : 'Cerebellum',
            };

    roi_breakdown['gui_Networks'] ={
        1:  'Somato-Motor',
        3:  'Cingular-opercular',
        4:  'Auditory',
        5:  'Default Mode',
        7:  'Visual',
        8:  'Frontal-Parietal',
        9:  'Salience',
        10: 'Subcortical',
        11: 'Ventral-Attention',
        12: 'Dorsal-Attention'}
        
        
        
    lobe_list = []
    network_list = []
    cols = ['ROI', 'Estimate','Lobe', 'Network', 'BrodLabel', 'Name']
    lst = []

    #pnum = 0
    for i,n in enumerate(nodes_list[pnum][0]):
        n += 1 # same as roi
        val = nodes_list[pnum][1][i]
        row = np.where(labels['Node_No']==int(n))[0][0]

        Lobe = labels.iloc[row][4]
        Network = labels.iloc[row][6]
        BrodLabel = labels.iloc[row][7]

        try:
            a = roi_breakdown['gui_Lobes'][Lobe]
        except:
            a = Lobe
        try:
            b = roi_breakdown['gui_BrodLabels'][BrodLabel]
        except: 
            b = BrodLabel
        try:
            c = roi_breakdown['gui_Networks'][Network]
        except:
            c = Network
        res = eval(shen268[str(n)][0])

        lobe_list.append(a)
        network_list.append(c)

        lst.append([n, val,a, c, b, res['name']])
        
    df1 = pd.DataFrame(lst, columns=cols)
    df1 = df1.style.set_properties(**{
        'background-color': 'white',
        'font-size': '12pt',
    })
    
    return df1
      


