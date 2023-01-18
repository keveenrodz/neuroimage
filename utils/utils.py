from nipype.interfaces.fsl import maths

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
