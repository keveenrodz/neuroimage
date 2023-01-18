import glob
import subprocess
from os import path


directory = '/home/gruneco3/Documents/IMAGENES_API/'
all_fmri_path = '/home/gruneco3/Documents/IMAGENES_API/all_fmri/'
all_T1_path = '/home/gruneco3/Documents/IMAGENES_API/all_T1/'


for filename in glob.iglob(f'{directory}/*/'):
    #print(filename)
    for filename2 in glob.iglob(f'{filename}/*/'):
        print(filename2)
        #if str(filename2).find('ADAD-MR-batch2') != -1:
        user_id = str(filename2).split('/')[-2]
        print(user_id)
        for filename3 in glob.iglob(f'{filename2}/Screening/FMRI/raw_fmri_exams/*/'):
            print(filename3)
            im = filename3 + 'FMRI_frame_*.nii'
            user_id = filename3 + user_id + '.nii'
            print(im)
            print(user_id)
            user_id_gz = user_id + '.gz'
            subprocess.run(f'fsl5.0-fslmerge -t {user_id} {im}', shell=True, check=True, universal_newlines=False, stdout=subprocess.PIPE)
            if path.isfile(user_id_gz):
                subprocess.run(f'cp -fr {user_id_gz} {all_fmri_path}', shell=True, check=True, universal_newlines=False, stdout=subprocess.PIPE)
                print('Trasfered')
            print('______________')
print('End fMRI transform and transfer')

for filename in glob.iglob(f'{directory}/*/'):
    #print(filename)
    for filename2 in glob.iglob(f'{filename}/*/'):
        print(filename2)
        user_id = str(filename2).split('/')[-2] + '.nii'
        print(user_id)
        for filename3 in glob.iglob(f'{filename2}/Screening/3DT1/*/'):
            print(filename3)
            im = filename3 + '3DT1_0001.nii'
            if path.isfile(im):
                all_T1_path_full = all_T1_path + user_id
                print(im)
                print(all_T1_path_full)
                subprocess.run(f'cp -fr {im} {all_T1_path_full}', shell=True, check=True, universal_newlines=False, stdout=subprocess.PIPE)
                print('Trasfered')
            print('______________')
print('End T1 transfer')
                    
                
                
                
            
            
            


