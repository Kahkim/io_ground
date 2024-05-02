
import pandas as pd

class Factory_Flowshop_Validator:

    def __init__(self, f):
        self.sche_tbl = pd.read_csv(f, header=0, sep=' *, *', engine='python')

    