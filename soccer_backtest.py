# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: soccer_backtest.py
@Time: 2019/11/13 9:36
@Motto：I have a bad feeling about this.
20191113:回测平台
"""
from config import settings
import pandas as pd
import numpy as np
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

str_add = lambda x,y:x+y

def str_combination(lists, N):
    pools = [x for x in combinations(lists, N)]
    return [reduce(str_add, i) for i in pools]

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
            #file_name = "soccer_"+today.strftime("%Y%m%d")+"_$_{}".format(N)
            #path = os.path.expanduser(r'..\lottery_guns\prediction_lottery\%s.csv' % file_name)
            #choice_df.to_csv(path)
        except Exception as e:
            print e

def run():
    'setting'
    result_dict={
        '1':'draw',
        '0':'lose',
        '3':'win'
    }
    path = settings.database
    keys = pd.read_csv(settings.keyspath, index_col=0)
    ss = '/20110103'
    df = pd.read_hdf(path, ss)
    df['win_index'] = df['match_id']+'win'
    df['draw_index'] = df['match_id']+'draw'
    df['lose_index'] = df['match_id']+'lose'
    df['result'] = df['match_id']+df['result'].apply(lambda x:result_dict[x])
    # 赔率池
    odds_pools = np.array(df[['win', 'draw', 'lose']], dtype=np.float).tolist()
    keys_pools = np.array(df[['win_index', 'draw_index', 'lose_index']]).tolist()
    # 赛果标准
    app = df['result'].tolist()
    result_3_1 = str_combination(app, 3)
    print result_3_1
    print len(result_3_1)
if __name__ == "__main__":
    run()

