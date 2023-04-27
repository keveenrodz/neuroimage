import os
import re
from nipype.interfaces.fsl import maths
from nipype.interfaces.fsl import Split


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

    
def extract_gICA_files(base_path: str) -> list:
    """
    Extract every component file from gICA directory
    :param base_path: gICA directory path
    :return: file names
    """
    import os
    import re
    included_extensions = ['nii', 'gz']
    include = ['component_ica_s']
    file_names = [fn for fn in os.listdir(base_path)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    r = re.compile(".*component_ica_s")
    file_names = list(filter(r.match, file_names))

    return file_names


def ztop_threshold(in_file: str, out_base_name: str, output_type='NIFTI') -> None:
    """
    Convert Z-stat to (uncorrected) P Image, Nonparametric uncorrected P-value,
    assuming timepoints are the permutations; first timepoint is actual (unpermuted)
    stats image
    :param in_file: input path image
    :param out_base_name: output name, please include the prefix
    :param output_type: [NIFTI, NIFTI_GZ]
    """
    math_command = maths.MathsCommand()
    math_command.inputs.in_file = in_file
    math_command.inputs.args = '-ztop'
    math_command.inputs.out_file = out_base_name
    math_command.inputs.output_type = output_type
    print(math_command.cmdline)
    res = math_command.run()

    
def threshold(in_file: str, out_base_name: str, th=5, output_type='NIFTI') -> None:
    """
    Binary image based on a threshold, use following percentage (0-100) of ROBUST
    RANGE of non-zero voxels and threshold below
    :param in_file: input path image
    :param out_base_name: output name, please include the prefix
    :param th: threshold in percentage (0-100), default th=5%
    :param output_type: [NIFTI, NIFTI_GZ]
    """
    math_command = maths.MathsCommand()
    math_command.inputs.in_file = in_file
    math_command.inputs.args = f'-thrP {th}'
    math_command.inputs.out_file = out_base_name
    math_command.inputs.output_type = output_type
    print(math_command.cmdline)
    res = math_command.run()

    
def bin_img(in_file: str, out_base_name: str, output_type='NIFTI') -> None:
    """
    Binarize the image, use (current image>0) to binarise
    :param in_file: input path image
    :param out_base_name: output name, please include the prefix
    :param output_type: [NIFTI, NIFTI_GZ]
    """
    math_command = maths.MathsCommand()
    math_command.inputs.in_file = in_file
    math_command.inputs.args = '-bin'
    math_command.inputs.out_file = out_base_name
    math_command.inputs.output_type = output_type
    print(math_command.cmdline)
    res = math_command.run()

    
def sub_img(in_file: str, in_file_subs: str, out_base_name: str, output_type='NIFTI') -> None:
    """
    Substract image, subtract following input from current image.
    res = in_file - in_file_subs
    :param in_file_subs: input path image to substract
    :param in_file: input path image
    :param out_base_name: output name, please include the prefix
    :param output_type: [NIFTI, NIFTI_GZ]
    """
    math_command = maths.MathsCommand()
    math_command.inputs.in_file = in_file
    math_command.inputs.args = f'-sub {in_file_subs}'
    math_command.inputs.out_file = out_base_name
    math_command.inputs.output_type = output_type
    print(math_command.cmdline)
    res = math_command.run()

    
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