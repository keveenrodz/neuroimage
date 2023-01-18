import subprocess
import os
import math



target_n_vols = 164
relevant_path = '/media/gruneco1/GRUNECO/ADNI_AD_tercera_seleccion/siemens/011_S_6303/Axial_rsfMRI__Eyes_Open_/2019-04-30_09_41_30.0/S819900/4D/'
output_path = relevant_path + 'vol_164/'
included_extensions = ['nii','gz']
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]
print(f'file names: {file_names}')


subprocess.run(['mkdir', '-p',output_path], stdout=subprocess.PIPE)
file_names_full = file_names.copy()
unwanted = file_names_full + [i[:i.index('.nii')] + '_v' + str(target_n_vols) + '_' + '.nii.gz' for i in file_names_full]

print('UNWANTED: ', unwanted)

#file_names = ['4D_2.nii']
for im in file_names:
    n_vol = int(subprocess.run(['fsl5.0-fslnvols', relevant_path + im], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    print(f'Image: {im} -> # Vols: {n_vol}')
    n_vol_to_delete = int((n_vol - target_n_vols) / 2) if (n_vol - target_n_vols) % 2 == 0 else int(math.floor((n_vol - target_n_vols) / 2) + 1)
    left = n_vol_to_delete if (n_vol - target_n_vols) % 2 == 0 else n_vol_to_delete - 1
    right = n_vol - n_vol_to_delete
    print(f'left: {left} - right: {right}')
    print(f'Total final vol: {right - left}')
    subprocess.run(['cp', relevant_path + im, output_path], stdout=subprocess.PIPE)
    idx = im.index('.nii')
    new_im_name = im[:idx] + '_v' + str(target_n_vols) + '_'
    subprocess.run(['fsl5.0-fslsplit', output_path + im, output_path + new_im_name], stdout=subprocess.PIPE)
    sub_path = output_path + new_im_name
    names_3d = [fn for fn in os.listdir(output_path)
              if any(fn.endswith(ext) for ext in included_extensions)]
    names_3d = [ele for ele in names_3d if ele not in unwanted]
    names_3d.sort()
    for i in names_3d[:left+1]:
        os.remove(output_path + i)
    for i in names_3d[right+1:]:
        os.remove(output_path + i)
    p = output_path + im[:idx] + '_v' + str(target_n_vols) + '*'
    subprocess.run(f'fsl5.0-fslmerge -t {output_path + new_im_name} {p}', shell=True, check=True, universal_newlines=False, stdout=subprocess.PIPE)
    for i in names_3d[left+1:right+1]:
        os.remove(output_path + i)
    os.remove(output_path + im)
    print('______________')




