#!python
# outer join tables by primary key
# primary_key: one or more columns (comma separated) to be used as join
# lookup_mode: alternative method in case regular method crashes
# v1.0 10/2018 paulo.ernesto
'''
usage: $0 input#file*bmf,csv,xlsx,isis,dm,00t condition primary_key:input output*csv,xlsx,shp lookup_mode@
'''
import sys, os.path
import pandas as pd
import numpy as np

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe

def db_join(input_path, condition, primary_key, output_path, lookup_mode):
  if len(primary_key) == 0:
    primary_key = None
  elif "," in primary_key:
    primary_key = primary_key.split(',')
 
  header = dict()
  tables = []
  for i_path in input_path.split(';'):
    idf = pd_load_dataframe(i_path, condition)
    for v in idf.columns:
      if v not in header:
        header[v] = len(header)
    tables.append(idf)

  odf = tables[0]

  if (int(lookup_mode)):
    for i in range(1, len(tables)):
      for j in odf.index:
        if np.isnan(odf.loc[j, primary_key]):
          continue
        flag = None
        for k in tables[i].index:
          flag = k
          if odf.loc[j, primary_key] < tables[i].loc[k, primary_key]:
            break
        if flag is not None:
          for cn in tables[i].columns:
            if cn != primary_key:
              odf.loc[j, cn] = tables[i].loc[flag, cn]
  else:
    for i in range(1, len(tables)):
      # {left, right, outer, inner, cross}, default inner
      odf = pd.merge(odf, tables[i], 'outer', primary_key)

  pd_save_dataframe(odf, output_path)

main = db_join

if __name__=="__main__":
  usage_gui(__doc__)
