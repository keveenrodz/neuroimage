from utils.utils import extract_gICA_files
from utils.utils import ztop_threshold
from utils.utils import threshold
from utils.utils import bin_img
from utils.utils import sub_img


def p_val_threshold(absolute_gica_path: str, file_gica_name: str, output_gica_name: str, th: int=5):
    """
    Extract the activation values from gica prob map, using (uncorrected) P<0.05.
    This help to reduce the individual noise.
    :param absolute_gica_path: Directory path
    :param file_gica_name: file gica name
    :param output_gica_name: output file gica name
    """
    ztop_threshold(absolute_gica_path + file_gica_name, absolute_gica_path + 'pval_' + output_gica_name)
    threshold(absolute_gica_path + 'pval_' + output_gica_name + '.nii',
              absolute_gica_path + 'thr5_pval_' + output_gica_name, th)
    bin_img(absolute_gica_path + 'thr5_pval_' + output_gica_name + '.nii',
            absolute_gica_path + 'bin_thr5_pval_' + output_gica_name)
    sub_img(absolute_gica_path + file_gica_name, absolute_gica_path + f'bin_thr{th}_pval_' + output_gica_name,
            absolute_gica_path + f'res_bin_thr{th}_pval_' + output_gica_name)


#rs_networks_V2_CN_AD_ADNI3_V2 = '/home/kevrodz/Documents/test_fwe_threshold/rs-networks_CN_AD_ADNI3_V2/'
#rs_networks_V2_CN_AD_ADNI3_V2 = '/home/kevrodz/Documents/test_fwe_threshold/rs-networks_AD_ADNI3_V2/'
#rs_networks_V2_CN_AD_ADNI3_V2 = '/home/kevrodz/Documents/test_fwe_threshold/'
#relevant_path = [rs_networks_V2_CN_AD_ADNI3_V2]
#
# relevant_path_cn_ad_v2_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_CN_AD_ADNI3_V2/'
# relevant_path_cn_ad_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_CN_AD_ADNI3_V2/'
# relevant_path_cn_mci_v2_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_V2_CN_MCI_ADNI3_V2/'
# relevant_path_cn_mci_adni3 = '/run/media/kevrodz/Salvador/ADNI3_KEV_CLAUDIA/rs-networks_CN_MCI_ADNI3_V2/'
#
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
#
#
# relevant_path = [relevant_path_cn_v2_adni3, relevant_path_cn_v2_oasis3, relevant_path_ad_v2_oasis3, relevant_path_cn_ad_adni3,
#                  relevant_path_cn_ad_v2_adni3, relevant_path_cn_mci_adni3, relevant_path_cn_mci_v2_adni3,
#                  relevant_path_ad_adni3_v2, relevant_path_ad_adni3_v1, relevant_path_mci_adni3_v2,
#                  relevant_path_mci_adni3_v1, relevant_path_cn_adni3, relevant_path_ad_oasis3,
#                  relevant_path_cn_oasis3, relevant_path_ad_v2_adni3_v1, relevant_path_ad_v2_adni3_v2,
#                  relevant_path_mci_v2_adni3_v1, relevant_path_mci_v2_adni3_v2]

# relevant_path_ad_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_AD_ADNI/'
# relevant_path_cn_ad_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_CN_AD_ADNI3/'
# relevant_path_mci_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_MCI_ADNI/'
# relevant_path_cn_mci_adni3 = '/run/media/kevrodz/KEVS/rs_networks/rs_networks_CN_MCI_ADNI/'

# relevant_path = [relevant_path_ad_adni3, relevant_path_cn_ad_adni3, relevant_path_mci_adni3,
#                  relevant_path_cn_mci_adni3]

relevant_path_biomarcadores_GK = '/media/gruneco-server/DB_GRUNECO/BIOMARCADORES_GICA_300ROI/GK-GICA/'
relevant_path_biomarcadores_GW = '/media/gruneco-server/DB_GRUNECO/BIOMARCADORES_GICA_300ROI/GW-GICA/'

relevant_path = [relevant_path_biomarcadores_GK, relevant_path_biomarcadores_GW]

for gica in relevant_path:
    files_gica = extract_gICA_files(gica)
    print(*files_gica, sep='\n')
    for gica_name in files_gica:
        print('gica name: ', gica_name)
        output_gica_name = gica_name[: gica_name.index('.nii')]
        p_val_threshold(gica, gica_name, output_gica_name)
        print(f'File: {output_gica_name} DONE')


