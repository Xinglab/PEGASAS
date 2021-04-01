
# -*- coding: UTF-8 -*-

"""Here are general configurations for the IRIS package, including 
version control, trained model parameter, etc.
"""

from pkg_resources import resource_filename
import os, sys
#import yaml


CURRENT_VERSION = "v1.1.11111111111"


def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def file_len(fin):
    with open(fin) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# For screening and translation
HALLMARKS50 = resource_filename('PEGASAS.data','hallmarks50.gmt.txt')
MAT_REORDER= resource_filename('PEGASAS','prepareGeneMatrixOrdered.py')
MAT_GENERATE= resource_filename('PEGASAS','generateMatrixbySample.py')
MAT_CORR= resource_filename('PEGASAS','cor_matrix_direct_perm.R')

GO_PLOT= resource_filename('PEGASAS','GO_plot.R')
GO_PLOT_LIB= resource_filename('PEGASAS','GO_enrichr_plot.R')

## For qsub
# QSUB_PREDICTION_CONFIG='h_data=15G,h_rt=5:00:00'
# QSUB_ALIGNMENT_CONFIG='h_data=38G,h_rt=4:30:00'
# QSUB_EXPRESSION_CONFIG='h_data=8G,h_rt=14:00:00'
# QSUB_RMATS_PREP_CONFIG='h_data=4G,h_rt=5:00:00'


