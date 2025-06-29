import sys
import os

msfs_max_py_2024_path = os.path.dirname(__file__)

#### DEBUG
import ptvsd
sys.path.append(msfs_max_py_2024_path)
ptvsd.enable_attach()