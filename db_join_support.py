#!python
# join hole intervals using the support of one
# check manual for usage and important details
# v1.0 05/2021 paulo.ernesto
'''
usage: $0 target_db*csv,xlsx target_hid:target_db target_from:target_db target_to:target_db source_db*csv,xlsx source_hid:source_db source_from:source_db source_to:source_db variables#variable:source_db#ponderation=mean,major,sum,list output*csv,xlsx
'''

import sys, os.path
import numpy as np
import pandas as pd

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, commalist, pd_load_dataframe, pd_save_dataframe
from db_join_interval import pd_join_interval
from bm_breakdown import pd_breakdown

def db_join_support(target_db, target_hid, target_from, target_to, source_db, source_hid, source_from, source_to, variables, output):
  v_lut = [{},{}]
  v_lut[0]['hid'] = target_hid or 'hid'
  v_lut[1]['hid'] = source_hid or 'hid'
  v_lut[0]['from'] = target_from or 'from'
  v_lut[1]['from'] = source_from or 'from'
  v_lut[0]['to']   = target_to or 'to'
  v_lut[1]['to']   = source_to or 'to'

  dfs = [pd_load_dataframe(target_db), pd_load_dataframe(source_db)]

  dfs[0]['tmp_target_from'] = dfs[0][v_lut[0]['from']]
  odf = pd_join_interval(dfs, v_lut)
  odf.reset_index(drop=1, inplace=True)
  # pd_join_interval modifies the input array which is bad behavior
  # but datasets may be huge so its best to just cleanup after
  dfs[0].reset_index(drop=1, inplace=True)

  variables = commalist().parse(variables)

  ttf = 'tmp_target_from'
  vl_a = [[ttf], [v_lut[0]['hid']]] + [[_[0] + '=' + _[0], _[1]] for _ in variables]

  odf = pd_breakdown(odf, vl_a)
  odf = pd.merge(dfs[0], odf, 'outer', [v_lut[0]['hid'], ttf])
  odf.drop(ttf, 1, inplace=True)

  if output:
    #odf.reset_index(drop=True, inplace=True)
    pd_save_dataframe(odf, output)
  else:
    print(odf.to_string())

main = db_join_support

if __name__=="__main__":
  usage_gui(__doc__)
