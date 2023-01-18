import os
import pandas as pd
from scipy.io import loadmat 


relevant_path = '/media/gruneco3/GRUNECO/API_preprocesamiento/conn_project_API_2mm/results/qa/QA_2022_06_08_191158109/'

included_extensions = ['mat']
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]

annots = loadmat('/media/gruneco3/GRUNECO/API_preprocesamiento/conn_project_API_2mm/results/qa/QA_2022_06_08_191158109/QA_COV.subject001.mat')
usr = []
appended_data = pd.DataFrame(columns = ['Subj', 'QC_ValidScans', 'QC_InvalidScans', 'QC_MaxMotion', 'QC_MeanMotion', 'QC_MaxGSchange', 'QC_MeanGSchange', 'QC_BOLDstd', 'QC_GCOR_rest'])

for idx, s in enumerate(file_names):
    annots = loadmat(relevant_path + s)
    con_list = [[element for element in upperElement] for upperElement in annots['results_label']]
    temp = []
    for i in range(len(con_list[0][0][0])):
        m = con_list[0][0][0][i][0]
        m = m.replace(" ", "").split('=')
        temp.append(m)
    df = pd.DataFrame(temp, columns =['QA', 'Value'])
    df = df.T
    df.columns = df.iloc[0].reset_index(drop=True)
    df = df[1:]
    subj = list(df.columns)[0]
    df.columns.values[0] = 'Subj'
    df.Subj = subj
    appended_data = pd.concat([appended_data, df], join="inner")

print('__________________')
print(appended_data)
appended_data.to_excel("API_QA.xlsx", sheet_name='QA_values', engine='xlsxwriter')
