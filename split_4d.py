import os
import re

from nipype.interfaces.fsl import Split


def extract_gICA_files(base_path: str) -> list:
    included_extensions = ['nii', 'gz']
    include = ['component_ica_s']
    file_names = [fn for fn in os.listdir(base_path)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    r = re.compile(".*component_ica_s")
    file_names = list(filter(r.match, file_names))

    return file_names


def split_fsl(in_file: str, out_base_name: str, dimension='t', output_type='NIFTI') -> None:
    """
    Split 4D fMRI into 3D
    :param in_file: input 4D nifti file
    :param out_base_name: output 3D nifti(gz) file, the output will have 000x sufix
    :param dimension: this can be in time:t or in some axes: x,y,z
    :param output_type: 'NIFTI'
    """
    split = Split()
    split.inputs.dimension = dimension
    split.inputs.in_file = in_file
    split.inputs.out_base_name = out_base_name
    split.inputs.output_type = output_type
    print(split.cmdline)
    res = split.run()


# relevant_path_ad_adni3_v2 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_AD_ADNI3_V2/'
# relevant_path_ad_adni3_v1 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_AD_ADNI3_V1/'
# relevant_path_mci_adni3_v2 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_MCI_ADNI3_V2/'
# relevant_path_mci_adni3_v1 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_MCI_ADNI3_V1/'
# relevant_path_cn_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_CN_ADNI3/'
# relevant_path_cn_oasis3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_CN_OASIS3/'
# relevant_path_ad_oasis3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_AD_OASIS3/'
#
# relevant_path_ad_v2_adni3_v1 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_AD_ADNI3_V1/'
# relevant_path_ad_v2_adni3_v2 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_AD_ADNI3_V2/'
# relevant_path_mci_v2_adni3_v1 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_MCI_ADNI3_V1/'
# relevant_path_mci_v2_adni3_v2 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_MCI_ADNI3_V2/'
# relevant_path_cn_v2_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_CN_ADNI3/'
# relevant_path_cn_v2_oasis3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_CN_OASIS3/'
# relevant_path_ad_v2_oasis3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_AD_OASIS3/'


# relevant_path = [relevant_path_ad_adni3_v2, relevant_path_ad_adni3_v1, relevant_path_mci_adni3_v2,
#                  relevant_path_mci_adni3_v1, relevant_path_cn_adni3, relevant_path_ad_oasis3,
#                  relevant_path_cn_oasis3, relevant_path_ad_v2_adni3_v1, relevant_path_ad_v2_adni3_v2,
#                  relevant_path_mci_v2_adni3_v1, relevant_path_mci_v2_adni3_v2, relevant_path_cn_v2_adni3,
#                  relevant_path_cn_v2_oasis3, relevant_path_ad_v2_oasis3]


# relevant_path_cn_ad_v2_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_CN_AD_ADNI3_V2/'
# relevant_path_cn_ad_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_CN_AD_ADNI3_V2/'
# relevant_path_cn_mci_v2_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_CN_MCI_ADNI3_V2/'
# relevant_path_cn_mci_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_CN_MCI_ADNI3_V2/'
# relevant_path = [relevant_path_cn_ad_adni3, relevant_path_cn_ad_v2_adni3, relevant_path_cn_mci_adni3,
#                  relevant_path_cn_mci_v2_adni3]

relevant_path_ad_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_AD_ADNI/'
relevant_path_cn_ad_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_CN_AD_ADNI3/'
relevant_path_mci_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_MCI_ADNI/'
relevant_path_cn_mci_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_CN_MCI_ADNI/'

relevant_path = [relevant_path_ad_adni3, relevant_path_cn_ad_adni3, relevant_path_mci_adni3,
                 relevant_path_cn_mci_adni3]

for gica in relevant_path:
    files_gica = extract_gICA_files(gica)
    print(files_gica)
    for gica_name in files_gica:
        output_gica_name = gica_name[: gica_name.index('.nii')]
        split_fsl(gica + gica_name, gica + output_gica_name)
        print(f'File: {output_gica_name} DONE')
    print('_______________-')
