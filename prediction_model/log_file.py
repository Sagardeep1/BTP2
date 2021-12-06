Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import numpy as np
>>> import pandas as pd
>>> import seaborn as sns
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    import seaborn as sns
ModuleNotFoundError: No module named 'seaborn'
>>> import matplotlib as plt
>>> df=pd.read_csv('C:/Users/hp/Downloads/bm/bm16_excel.csv')
>>> df
              AbsTime  ...  {mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM)}Delta
0                 NaN  ...                                                NaN     
1    03/10/2021 17:46  ...                                                0.0     
2    03/10/2021 17:46  ...                                                0.0     
3    03/10/2021 17:46  ...                                                0.0     
4    03/10/2021 17:46  ...                                                0.0     
..                ...  ...                                                ...     
860  03/10/2021 19:26  ...                                                0.0     
861  03/10/2021 19:26  ...                                                0.0     
862  03/10/2021 19:27  ...                                                0.0     
863  03/10/2021 19:27  ...                                                0.0     
864  03/10/2021 19:27  ...                                                0.0     

[865 rows x 22 columns]
>>> df.plot()
<matplotlib.axes._subplots.AxesSubplot object at 0x000001E3683FAA00>
>>> from matplotlib import pyplot as plt
>>> from matplotlib import interactive
>>> interactive(True)
>>> df.plot()
<matplotlib.axes._subplots.AxesSubplot object at 0x000001E36A8E65E0>
>>> import seaborn as sns
>>> sns.heatmap(df)
Traceback (most recent call last):
  File "<pyshell#12>", line 1, in <module>
    sns.heatmap(df)
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\_decorators.py", line 46, in inner_f
    return f(**kwargs)
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\matrix.py", line 535, in heatmap
    plotter = _HeatMapper(data, vmin, vmax, cmap, center, robust, annot, fmt,
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\matrix.py", line 155, in __init__
    self._determine_cmap_params(plot_data, vmin, vmax,
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\matrix.py", line 189, in _determine_cmap_params
    calc_data = plot_data.astype(float).filled(np.nan)
ValueError: could not convert string to float: '03/10/2021 17:46'
>>> sns.heatmap(df, cmap ='RdYlGn', linewidths = 0.30, annot = True)
Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    sns.heatmap(df, cmap ='RdYlGn', linewidths = 0.30, annot = True)
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\_decorators.py", line 46, in inner_f
    return f(**kwargs)
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\matrix.py", line 535, in heatmap
    plotter = _HeatMapper(data, vmin, vmax, cmap, center, robust, annot, fmt,
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\matrix.py", line 155, in __init__
    self._determine_cmap_params(plot_data, vmin, vmax,
  File "C:\Users\hp\AppData\Local\Programs\Python\Python38\lib\site-packages\seaborn\matrix.py", line 189, in _determine_cmap_params
    calc_data = plot_data.astype(float).filled(np.nan)
ValueError: could not convert string to float: '03/10/2021 17:46'
>>> df.drop(['AbsTime'],axis=1)
     RelTime  ...  {mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM)}Delta
0        NaN  ...                                                NaN     
1     6997.0  ...                                                0.0     
2     7000.0  ...                                                0.0     
3     6999.0  ...                                                0.0     
4     7001.0  ...                                                0.0     
..       ...  ...                                                ...     
860   7000.0  ...                                                0.0     
861   7000.0  ...                                                0.0     
862   7000.0  ...                                                0.0     
863   7000.0  ...                                                0.0     
864   7000.0  ...                                                0.0     

[865 rows x 21 columns]
>>> df.drop(['RelTime'],axis=1)
              AbsTime  ...  {mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM)}Delta
0                 NaN  ...                                                NaN     
1    03/10/2021 17:46  ...                                                0.0     
2    03/10/2021 17:46  ...                                                0.0     
3    03/10/2021 17:46  ...                                                0.0     
4    03/10/2021 17:46  ...                                                0.0     
..                ...  ...                                                ...     
860  03/10/2021 19:26  ...                                                0.0     
861  03/10/2021 19:26  ...                                                0.0     
862  03/10/2021 19:27  ...                                                0.0     
863  03/10/2021 19:27  ...                                                0.0     
864  03/10/2021 19:27  ...                                                0.0     

[865 rows x 21 columns]
>>> df=df.drop(['AbsTime','RelTime'],axis=1)
>>> df
     {mem_tot_alloc_bm16384-MEM_LOGGING}Val  ...  {mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM)}Delta
0                                       NaN  ...                                                NaN     
1                                    1056.0  ...                                                0.0     
2                                    1056.0  ...                                                0.0     
3                                    1056.0  ...                                                0.0     
4                                    1056.0  ...                                                0.0     
..                                      ...  ...                                                ...     
860                                  1056.0  ...                                                0.0     
861                                  1056.0  ...                                                0.0     
862                                  1056.0  ...                                                0.0     
863                                  1056.0  ...                                                0.0     
864                                  1056.0  ...                                                0.0     

[865 rows x 20 columns]
>>> sns.heatmap(df, cmap ='RdYlGn')
<matplotlib.axes._subplots.AxesSubplot object at 0x000001E3683FAA00>
>>> plt.show()
>>> sns.heatmap(df.corr(), cmap ='RdYlGn')
<matplotlib.axes._subplots.AxesSubplot object at 0x000001E3683FAA00>
>>> plt.show()
>>> df.corr()
                                                    {mem_tot_alloc_bm16384-MEM_LOGGING}Val  ...  {mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM)}Delta
{mem_tot_alloc_bm16384-MEM_LOGGING}Val                                                 NaN  ...                                                NaN     
{mem_tot_alloc_bm16384-MEM_LOGGING}Delta                                               NaN  ...                                                NaN     
{mem_tot_alloc_bm16384-mempool_LOGGING(LOGGING)...                                     NaN  ...                                                NaN     
{mem_tot_alloc_bm16384-mempool_LOGGING(LOGGING)...                                     NaN  ...                                                NaN     
{mem_tot_alloc_bm16-MEM_LB_SERVICE}Val                                                 NaN  ...                                                NaN     
{mem_tot_alloc_bm16-MEM_LB_SERVICE}Delta                                               NaN  ...                                                NaN     
{mem_tot_alloc_bm16-MEM_SSL}Val                                                        NaN  ...                                          -0.014616     
{mem_tot_alloc_bm16-MEM_SSL}Delta                                                      NaN  ...                                           0.120903     
{mem_tot_alloc_bm16-MEM_DHT}Val                                                        NaN  ...                                           0.014056     
{mem_tot_alloc_bm16-MEM_DHT}Delta                                                      NaN  ...                                          -0.012843     
{mem_tot_alloc_bm16-MEM_LOGSTREAM_TRANS}Val                                            NaN  ...                                           0.070816     
{mem_tot_alloc_bm16-MEM_LOGSTREAM_TRANS}Delta                                          NaN  ...                                           1.000000     
{mem_tot_alloc_bm16-mempool_LB(LB)}Val                                                 NaN  ...                                                NaN     
{mem_tot_alloc_bm16-mempool_LB(LB)}Delta                                               NaN  ...                                                NaN     
{mem_tot_alloc_bm16-mempool_SSL(SSL)}Val                                               NaN  ...                                          -0.014616     
{mem_tot_alloc_bm16-mempool_SSL(SSL)}Delta                                             NaN  ...                                           0.120903     
{mem_tot_alloc_bm16-mempool_DHT(DHT)}Val                                               NaN  ...                                           0.014056     
{mem_tot_alloc_bm16-mempool_DHT(DHT)}Delta                                             NaN  ...                                          -0.012843     
{mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM...                                     NaN  ...                                           0.070816     
{mem_tot_alloc_bm16-mempool_LOGSTREAM(LOGSTREAM...                                     NaN  ...                                           1.000000     

[20 rows x 20 columns]
>>> import os
>>> from os import listdir
>>> import numpy as np
import pandas as pd
import os
import glob
import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
from sklearn.linear_model import LinearRegression
SyntaxError: multiple statements found while compiling a single statement
>>> from sklearn import preprocessing
>>> from scipy import stats
>>> from sklearn.linear_model import LinearRegression
>>> import glob
>>> 