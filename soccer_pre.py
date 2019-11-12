# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: soccer_pre.py
@Time: 2019/11/12 22:02
@Motto：I have a bad feeling about this.
"""
import numpy as np
import pandas as pd
from datetime import datetime
import os

match_1={
    'win1':2.7,
    'draw1':3.5,
    'lose1':2.13
}
match_2={
    'win2': 2.85,
    'draw2': 3.55,
    'lose2': 2.02
}
match_3={
    'win3': 2.69,
    'draw3': 3.4,
    'lose3': 2.2
}

list1 = [match_1['win1'], match_1['draw1'], match_1['lose1']]
list2 = [match_2['win2'], match_2['draw2'], match_2['lose2']]
list3 = [match_3['win3'], match_3['draw3'], match_3['lose3']]

list4 =['win1', 'draw1', 'lose1']
list5 =['win2', 'draw2', 'lose2']
list6 =['win3', 'draw3', 'lose3']

def lists_combination(lists, code='_'):
    '''输入多个列表组成的列表, 输出其中每个列表所有元素符合条件的排列组合'''
    try:
        import reduce
    except:
        from functools import reduce

    def myfunc(list1, list2):
        return [str(i) + code + str(j) for i in list1 for j in list2]

    return reduce(myfunc, lists)

def mulpti_combination(lists):
    '''输入多个列表组成的列表, 输出其中每个列表所有元素符合条件的排列组合'''
    try:
        import reduce
    except:
        from functools import reduce

    def myfunc(list1, list2):
        return [ i*j for i in list1 for j in list2]

    return reduce(myfunc, lists)

ss = mulpti_combination([list1, list2, list3])
pp = lists_combination([list4, list5, list6])
df = pd.DataFrame([pp,ss]).T
today = datetime.today()
file_name = "soccer_"+today.strftime("%Y%m%d")
path = os.path.expanduser(r'..\lottery_guns\prediction_lottery\%s.csv' % file_name)
df.to_csv(path)
print pp
print ss