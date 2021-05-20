#!python
# change support of a geophisics file
# v1.0 05/2021 paulo.ernesto, tiago.webber
'''
usage: $0 input_data*las,csv,xlsx support=0.1 output_path*las,csv,xlsx

'''
import sys, os.path
import pandas as pd

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')
import lasio
from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe, commalist
from bm_breakdown import pd_breakdown
from db_las_export_table import las_set_data

def db_custom_20210513(input_path, support, output_path):
  las = None
  print(input_path)
  if input_path.lower().endswith('las'):
    # the default 4000 bytes are not enough, -1 = full file
    f,c = lasio.open_file(input_path, autodetect_encoding_chars=-1)
    las = lasio.read(f)
    df = las.df()
    df.reset_index(inplace=True)
  else:
    df = pd_load_dataframe(input_path)

  #print("criando suporte")
  #   10 = 1000
  #    1 = 100
  #  0.1 = 10
  # 0.01 = 1
  df['DEPT_RL'] = df.eval("DEPT * 100 // (%s / 0.01)" % support, engine='python')

  #print("breakdown usando suporte")
  vl = [['DEPT_RL'],['DEPT=DEPT','max']]
  vpre = {'DEPT_RL','DEPT'}
  for v in ['furo','holeid','hid','nomrev']:
    for c in [str.lower, str.upper,str.capitalize]:
      if c(v) in df:
        vl.insert(0, [c(v) + '=' + c(v)])
        vpre.add(c(v))
        break
  for v in df.columns:
    if v not in vpre:
      vl.append([v + '=' + v, 'mean'])
  #print(vl)
  df = pd_breakdown(df, vl)
  #print(df)
  #python bm_breakdown.py %work_xlsx% "" "filename;DEPT_RL;DEPT=DEPT,max;CADE=CADE,mean;BIT GRC1=BIT GRC1,mean;DD3L=DD3L,mean;DD3B=DD3B,mean;DENL=DENL,mean;DENB=DENB,mean;GRDE=GRDE,mean;CCO1=CCO1,mean;CO1C=CO1C,mean;DD3G=DD3G,mean;GC1G=GC1G,mean;DD3C=DD3C,mean;GTMP=GTMP,mean;GRDO=GRDO,mean;DNBO=DNBO,mean;DNLO=DNLO,mean;CCLF=CCLF,mean;VAL_EXP CADMED=VAL_EXP CADMED,mean;CODREV=CODREV,mean;DIAM=DIAM,mean;WLEV=WLEV,mean" 0 %work_xlsx%

  #print("removendo colunas temporarias")
  df.reset_index(inplace=True)
  df.drop('DEPT_RL', 1, inplace=True)

  if las is None or not output_path.lower().endswith('las'):
    pd_save_dataframe(df, output_path)
  else:
    las_set_data(las, df)
    las.write(output_path)


main = db_custom_20210513

if __name__=="__main__":
  usage_gui(__doc__)

