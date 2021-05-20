#!python
# join hole intervals
# check manual for usage and important details
# v1.0 12/2020 paulo.ernesto
'''
usage: $0 left_db*csv,xlsx left_hid:left_db left_from:left_db left_to:left_db right_db*csv,xlsx right_hid:right_db right_from:right_db right_to:right_db output*csv
'''

import sys, os.path
import numpy as np
import pandas as pd

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe
from db_create_from_to import pd_create_from_to
import portion
import time

def interval_consolidate(dl):
  ''' remove redundant intervals '''
  cl = dl.copy()
  for d0 in dl:
    for d1 in dl:
      if d0 != d1 and d1 in cl and d0.contains(d1):
        cl.remove(d1)
  return cl

def pd_join_interval(dfs, v_lut):
  hl = dict()
  vl = []
  for i in range(2):
    if not v_lut[i]['from']:
      pd_create_from_to(dfs[i], v_lut[i]['hid'], v_lut[i]['to'], True)
      v_lut[i]['from'] = 'from'

    dfs[i].set_index(v_lut[i]['hid'], False, False, True)
    dfs[i].set_index(pd.RangeIndex(0, len(dfs[i])), False, True, True)

    # first step: construct a comprehensive list of intervals
    # where any of the inputs touches
    for row, df in dfs[i].iterrows():
      hid = df[v_lut[i]['hid']]
      if hid not in hl:
        hl[hid] = set()
      d = portion.closedopen(df[v_lut[i]['from']], df[v_lut[i]['to']])
      if not d.empty:
        hl[hid].add(d)

    # add variables one by one since we have to preserve order anyway
    for c in dfs[i].columns:
      if c not in vl:
        vl.append(c)
  t = time.time()
  odf = pd.DataFrame(columns=vl)
  for hid, dl in hl.items():
    print("#", hid)
    c0 = min(dl).lower
    c1 = None
    while True:
      r = pd.Series(None, vl, 'object', (hid,c0))
      cs = portion.singleton(c0)
      for i in range(len(dfs)):
        if hid in dfs[i].index:
          for row_i, row_d in dfs[i].loc[hid].iterrows():
            d = portion.closedopen(row_d[v_lut[i]['from']], row_d[v_lut[i]['to']])
            if d.overlaps(cs):
              r.update(row_d)
              if c1 is None or c1 > d.upper:
                c1 = d.upper
      if c1 is None:
        break
      r['from'] = c0
      r['to'] = c1
      c0 = c1
      c1 = None
      odf = odf.append(r)
  print("pd_join_interval profile time", time.time() - t)
  return odf

def db_join_interval(left_db, left_hid, left_from, left_to, right_db, right_hid, right_from, right_to, output):
  v_lut = [{},{}]
  v_lut[0]['hid'] = left_hid or 'DHID'
  v_lut[1]['hid'] = right_hid or 'DHID'
  v_lut[0]['from'] = left_from
  v_lut[1]['from'] = right_from
  v_lut[0]['to']   = left_to
  v_lut[1]['to']   = right_to

  dfs = [pd_load_dataframe(left_db), pd_load_dataframe(right_db)]

  odf = pd_join_interval(dfs, v_lut)

  if output:
    odf.reset_index(drop=True, inplace=True)
    pd_save_dataframe(odf, output)
  else:
    print(odf.to_string())

main = db_join_interval

if __name__=="__main__":
  usage_gui(__doc__)
