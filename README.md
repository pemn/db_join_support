# db_join_support
multiple hole database join utilities using from/to
## description
Those scripts are used in common operations in the mining industry which works with drillhole datasets containing intervals depth (from > to).  
In those datasets you dont have a primary key but a combination of hole id and intervals. Joining two datasets with different intervais is not trivial and may be done in multiple ways.  
 1 - Breaking intervals every time either dataset has a break. The output intervals wont match either datasets.  
 2 - Using the support of the first dataset and aggregating the values from the second dataset to fit into those intervals.  
 3 - Using a fixed support with regular intervals which wont match either dataset so both will be aggregated to fit.  
 ## scripts  
  - db_join_support.py - (case 2) join hole intervals using the support of one  
  - db_join_interval.py - (case 1) join hole intervals  
  - db_join.py - generic join script using a primary key  
  - db_create_from_to.py - create from and to field based on a single depth field. Its a helper script with funcions used by other scripts.  
  - bm_breakdown.py - generic aggregation script. In this project works only as a helper script.
 ## supported file formats
 - csv  
 - xlsx  
 - las  
 ## requirement
 WinPython 3.7+ installed.
 Alternatively WinPython can be extracted to %appdata% and the .cmd files should autodetect it there.
 
