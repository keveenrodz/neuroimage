from __future__ import print_function
import numpy as np
import pandas as pd
from nipype.algorithms.metrics import Overlap


def mri_overlap(vol1: str, vol2: str, output: str):
    """
    Calculates the overlap between 2 images (Dice and Jaccard Index)
    :param vol1: path of volume 1
    :param vol2: path of volume 2
    :param output: output path
    :return: overlap object with all the results
    """
    import os
    
    assert os.path.isfile(vol1), 'Volume 1 is not a correct file'
    assert os.path.isfile(vol2), 'Volume 2 is not a correct file'
    assert os.path.isfile(output), 'Output file name is not a correct file [NII]'

    overlap = Overlap()
    overlap.inputs.volume1 = vol1
    overlap.inputs.volume2 = vol2
    overlap.inputs.out_file = output
    res = overlap.run()
    return res


def dice_jaccard(vol1: str, vol2: str, nets: list, out: str):
    """
    Generate the overlap (Dice Index) and similarity (Jaccard Index) between 2 images
    :param vol1: path of volume 1
    :param vol2: path of volume 2
    :param output: output path
    :return: results: list with the raw results, networks: dataframe object with all the results
    """
    
    import os
    nets = nets
    dice = []
    jaccard = []
    volume_difference = []
    results = []
    
    assert os.path.isdir(out), 'Output is not a directory'
        

    for i in range(len(vol1)):        
        vol1_mean = vol1[i] + '.nii'
        vol2_mean = vol2[i] + '.nii'
        output = out + f'diff_{i:04}' + '.nii'
        res = mri_overlap(vol1_mean, vol2_mean, output)
        
        results.append(res.outputs)
        dice.append(res.outputs.dice)
        jaccard.append(res.outputs.jaccard)
        volume_difference.append(res.outputs.volume_difference)
        
    networks = pd.DataFrame({'rs_network': nets,
                                'Dice': dice,
                                'Jaccard': jaccard,
                                'volume_difference': volume_difference})
    networks.to_csv(out + 'results.csv')
    
    return results, networks