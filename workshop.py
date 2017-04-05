from qgis.core import *
import processing
import numpy as np

def findUpstreamNpy(com, npy_file):
    '''
    __author__ =  "Rick Debbout <debbout.rick@epa.gov>"
    Finds upstream array of COMIDs for any given catchment COMID
    Arguments
    ---------
    zone                  : string of an NHDPlusV2 VPU zone, i.e. 10L, 16, 17
    com                   : COMID of NHD Catchment, integer
    numpy_dir             : directory where .npz file is stored
    '''
    npzfile = np.load(npy_file)
    comids = npzfile['comids']
    lengths= npzfile['lengths']
    upStream = npzfile['upStream']
    itemindex = int(np.where(comids == com)[0])
    n = lengths[:itemindex].sum()
    arrlen = lengths[itemindex]
    return upStream[n:n+arrlen]
    
f = '/home/rick/Dropbox/QGIS_workshop/upstream_arrays.npz'
com = 23763517 # COMID where the Calapooia meets the Willamette
wsIds = findUpstreamNpy(com, f)
len(wsIds)
print wsIds

layer = processing.getObject('Catchments')
layer.featureCount()
query = "\"FEATUREID\" in %s" % str(tuple(wsIds))
selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
layer.setSelectedFeatures([k.id() for k in selection])
