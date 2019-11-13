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
from itertools import combinations
try:
    import reduce
except:
    from functools import reduce

def keyfunc(list1, list2, code='_'):
    return [str(i) + code + str(j) for i in list1 for j in list2]

def productfunc(list1, list2):
    return [i*j for i in list1 for j in list2]

class Soccer_Combi_pre(object):
    """
    重点针对混合过关玩法
    """

    def __init__(self, odds_pools, key_pools):
        self.odds_pools=odds_pools
        self.key_pools=key_pools

    def comb(self, pools, N):
        """
        :param N:  按照几串1进行组合
        :return:
        """
        return [x for x in combinations(pools, N)]

    def key_comb(self, N=3):
        """
        对索引进行排列
        """
        if len(self.key_pools)<N:
            print "not enough!!"
            return None
        elif N<=2:
            lists = self.comb(self.key_pools,N)
            return [keyfunc(i[0], i[-1]) for i in lists]
        else:
            lists = self.comb(self.key_pools,N)
            return [reduce(keyfunc, x) for x in lists]

    def product_comb(self, N=3):
        """
        对赔率进行乘积排列
        """
        if len(self.odds_pools)<N:
            print "not enough!!"
            return None
        elif N<=2:
            lists = self.comb(self.odds_pools,N)
            return [productfunc(i[0], i[-1]) for i in lists]
        else:
            lists = self.comb(self.odds_pools,N)
            return [reduce(productfunc, x) for x in lists]

    def data2csv(self, N=3):
        """建立数据档案并2csv;
           对乘积进行排序筛选后给出理想场次
        """
        try:
            keys_list = np.concatenate(np.array(self.key_comb(N)))
            product_odds_list = np.concatenate(np.array(self.product_comb(N)))
            df = pd.DataFrame(product_odds_list, keys_list)
            df.columns = ['odds_product']
            # 筛选
            standard_odds = pow(3, N)+1
            choice_df = df[df['odds_product']>standard_odds].sort_index()
            print choice_df
            today = datetime.today()
            file_name = "soccer_"+today.strftime("%Y%m%d")+"_$_{}".format(N)
            path = os.path.expanduser(r'..\lottery_guns\prediction_lottery\%s.csv' % file_name)
            choice_df.to_csv(path)
        except Exception as e:
            print e

def run():
    'setttings'
    match_1 = {
        'win1': 2.7,
        'draw1': 3.5,
        'lose1': 2.13
    }
    match_2 = {
        'win2': 2.85,
        'draw2': 3.55,
        'lose2': 2.02
    }
    match_3 = {
        'win3': 2.69,
        'draw3': 3.4,
        'lose3': 2.2
    }
    match_4 = {
        'win4': 2.78,
        'draw4': 3.35,
        'lose4': 2.16
    }

    odds_pools = [
        [match_1['win1'], match_1['draw1'], match_1['lose1']],
        [match_2['win2'], match_2['draw2'], match_2['lose2']],
        #[match_3['win3'], match_3['draw3'], match_3['lose3']],
        #[match_4['win4'], match_4['draw4'], match_4['lose4']],
    ]

    key_pools = [
        [match_1['win1'], match_1['draw1'], match_1['lose1']],
        [match_2['win2'], match_2['draw2'], match_2['lose2']],
        #[match_3['win3'], match_3['draw3'], match_3['lose3']],
        #[match_4['win4'], match_4['draw4'], match_4['lose4']],
    ]
    engine = Soccer_Combi_pre(odds_pools, key_pools)
    engine.data2csv(N=2)

if __name__ == "__main__":
    run()