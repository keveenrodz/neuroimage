from nilearn.input_data import NiftiLabelsMasker, NiftiMapsMasker, NiftiSpheresMasker
from nilearn.datasets import load_mni152_template, load_mni152_brain_mask
from nilearn.image import load_img
import os
import numpy as np
from joblib import Memory
import logging

brainmask = load_mni152_brain_mask()
mem = Memory('nilearn_cache')


def read_coords(roi_file: str) -> list:
    """
    Parse and validate coordinates from file
    :param roi_file: roi file path
    :return: list of roi's values
    """
    if not roi_file.endswith('.tsv'):
        raise ValueError('Coordinate file must be a tab-separated .tsv file')

    coords = pd.read_table(roi_file)

    # validate columns
    columns = [x for x in coords.columns if x in ['x', 'y', 'z']]
    if (len(columns) != 3) or (len(np.unique(columns)) != 3):
        raise ValueError('Provided coordinates do not have 3 columns with '
                         'names `x`, `y`, and `z`')

    # convert to list of lists for nilearn input
    return coords.values.tolist()


def signal_extract(data: list, atlas: str, t_r: float = None,
                   masker_type: str = 'Maps', config: dict = {}, saveas: str = 'file') -> list:
    """
    Extracts BOLD time-series from regions of interest.
    These regions can be from coordinates (Spheres), probabilistic maps, binary maps (Maps) or by labeled maps (Labels)
    Please see https://nilearn.github.io/stable/modules/generated/nilearn.maskers
    :param data: Filenames of subjects.
    :param atlas: Regions or coordinates to extract signals from. Can be your own atlas or from nilearn atlas
    :param t_r: TR if need it.
    :param masker_type: Type of masker used to extract BOLD signals. types are : 'Spheres','Maps','Labels'
    :param config: dictionary with the configurations by masker_type. Following the nilearn parameters.
    :param saveas: Destination to save and load output (.npz)
    :return: subject_ts : array-like , 2-D (n_subjects,n_regions)
    Array of BOLD time-series.
    roi_img: ROI image or seeds path
    labels: labels (columns names) fro time series extracted.
    masker_type: name of masker type applied.
    """
    subjects_ts = []
    radius = config.get('radius', 4)
    detrend = bool(config.get('detrend', False))
    standardize = bool(config.get('standardize', True))
    low_pass = config.get('low_pass', None)
    high_pass = config.get('high_pass', None)
    memory_level = int(config.get('memory_level', 0))
    smoothing_fwhm = config.get('smoothing_fwhm', None)
    resampling_target = config.get('resampling_target', 'data')
    confounds = config.get('confounds', None)
    verbose = int(config.get('verbose', 5))
    reports = bool(config.get('reports', True))
    time_series = list()
    labels = list()
    dim_data = len(data)

    if (isinstance(atlas, str) and atlas.endswith('.tsv')):
        roi = read_coords(atlas)
        n_rois = len(roi)
        is_coords = True
        print('  {} region(s) detected from coordinates'.format(n_rois))
    elif isinstance(atlas, list) or isinstance(atlas, np.recarray):
        is_coords = True
        pass
    else:
        roi = load_img(atlas)
        n_rois = len(np.unique(roi.get_data())) - 1

        is_coords = False
        print('  {} region(s) detected from {}'.format(n_rois,
                                                       roi.get_filename()))

    if os.path.exists(saveas):

        subjects_ts = np.load(saveas)['arr_0']
        labels = np.load(saveas)['labels_0']
        roi_img = np.load(saveas)['roi_img_0']

    else:

        if masker_type == 'Spheres':
            logging.debug('Spheres Extract')
            if is_coords:
                if radius is None:
                    warnings.warn('No radius specified for coordinates; setting '
                                  'to nilearn.input_data.NiftiSphereMasker default '
                                  'of extracting from a single voxel')
            masker = NiftiSpheresMasker(seeds=atlas, smoothing_fwhm=smoothing_fwhm, radius=radius,
                                            mask_img=brainmask, detrend=detrend, standardize=standardize,
                                            low_pass=low_pass, high_pass=high_pass, t_r=t_r, allow_overlap=True)

        elif masker_type == 'Maps':
            logging.debug('Maps Extract')
            masker = NiftiMapsMasker(maps_img=atlas, mask_img=brainmask, standardize=True,
                                     high_pass=high_pass, low_pass=low_pass, detrend=detrend, t_r=t_r,
                                     memory_level=memory_level, smoothing_fwhm=smoothing_fwhm,
                                     resampling_target=resampling_target, memory=mem, verbose=verbose, reports=reports)
        elif masker_type == 'Labels':
            logging.debug('Labels Extract')
            if n_rois >= 1:
                masker = NiftiLabelsMasker(labels_img=atlas, mask_img=brainmask, standardize=True,
                                           high_pass=high_pass, low_pass=low_pass, detrend=detrend, t_r=t_r,
                                           memory_level=memory_level, smoothing_fwhm=smoothing_fwhm,
                                           resampling_target=resampling_target, memory=mem, verbose=verbose)
            else:
                raise ValueError('No ROI detected; check ROI file')
        else:
            raise ValueError("Please provide masker type (Spheres, Maps, Labels). ")

        for func_file in data:
            try:
                time_series = masker.fit_transform(func_file, confounds=confounds)
                subjects_ts.append(time_series)
                np.savez(saveas, subjects_ts)
            except BaseException:
                logging.exception("An exception was thrown! ", exc_info=True)
            # Determine column names for timeseries
            if isinstance(masker, NiftiMapsMasker):
                labels = ['map {}'.format(int(i))
                          for i in np.arange(time_series.shape[1])]
                roi_img = masker.maps_img_
                masker_type = 'NiftiMapsMasker'

            elif isinstance(masker, NiftiLabelsMasker):
                if labels is None:
                    labels = ['roi {}'.format(int(i)) for i in masker.labels_img_]
                roi_img = masker.mask_img_
                masker_type = 'NiftiLabelsMasker'

            elif isinstance(masker, NiftiSpheresMasker):
                if labels is None:
                    labels = ['roi {}'.format(int(i)) for i in range(len(masker.seeds_))]
                roi_img = masker.seeds_
                masker_type = 'NiftiSpheresMasker'

    return subjects_ts, roi_img, labels, masker_type


def discard_scans(img, n_scans: int = 0, regressors=None):
    """
    crop scans from image
    :param regressors: regressors params
    :param img: mri data
    :param n_scans: # scans to be drop
    """
    arr = img.get_data()
    arr = arr[:, :, :, n_scans:]
    img = nib.Nifti1Image(arr, img.affine)

    if regressors is not None:
        # crop from regressors
        regressors = regressors.iloc[n_scans:, :]
    return img, regressors
