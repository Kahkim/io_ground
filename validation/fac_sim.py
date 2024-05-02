
import pandas as pd

class Factory_Simulator:        

    def __init__(self, f):
        self.sche_tbl = pd.read_csv(f, header=0, sep=' *, *', engine='python')
        self.max_make_span = self.sche_tbl['E'].max()
        print(self.sche_tbl['M'].unique())

    def production(self, due_date):
        for t in range(0, self.max_make_span+1):
            print(t)        

        # 단순히 due_date 기준의 초과 여부만 판단
    

class Machine:
    def __init__(self, id):
        self.id = id
        self.cur_setup = None

    def change_setup(self, from_setup, to_setup):
        # TODO: jobtype별 setup time table 참고하여 validation 필요
        self.cur_setup = to_setup


fs = Factory_Simulator('sche_0001.csv')
# print(fs.sche_tbl)
# print(fs.sche_tbl.columns)
# print(f'***{fs.sche_tbl['E']}***')
# print(fs.sche_tbl['E'].max())

fs.production()

# fs.sche_tbl.info()
