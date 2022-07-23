import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 20)
pd.set_option('display.precision', 4)
pd.set_option('display.width', 250)

np.set_printoptions(linewidth=250, formatter=dict(float=lambda x: "%.3g" % x))
