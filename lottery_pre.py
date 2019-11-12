# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: lottery_pre.py
@Time: 2019/11/12 22:00
@Motto：I have a bad feeling about this.
"""
#https://datachart.500.com/ssq/history/outball.shtml
import random
import time
import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime

def rolling_window(a, window):
    "rolling 切块"
    a = np.asanyarray(a)
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

class Lottery_choice(object):
    """
    随机跑数据, 生产数据的先后顺序与上期相符，则提供下一步选号；运行出10组数据，选择重复数量最多的数据作为购买备选号码
    """
    def __init__(self, prize_num):
        self.prize_num = prize_num # 上期中奖号码
        self.circle_num = 0 # 循环次数
        self.start_time = time.clock()
        self.num = 0
        self.choice_nums_array = []

    def engine(self, lottery="ssq"):
        "跑数主引擎"
        while True:
            if lottery=="ssq": # 双色球
                red_ball = range(1, 34)
                blue_ball = range(1, 17)
                length = len(self.prize_num)
                alternate_num = random.sample(red_ball, length)
                if len(alternate_num)!=len(self.prize_num):
                    print "not enough!"
                else:
                    if np.array(alternate_num).prod() == np.array(self.prize_num).prod() and np.sum(alternate_num)==np.sum(self.prize_num): # 等于上期中奖号码
                        choice_num = random.sample(red_ball, length)
                        self.choice_nums_array.extend(choice_num)
                        self.circle_num+=1
                    else:
                        pass
                if self.circle_num>=20:
                    elapsed = (time.clock() - self.start_time)
                    print("Time used:", elapsed)
                    finalnum = pd.Series(Counter(self.choice_nums_array)).sort_values(ascending= False)
                    today = datetime.today()
                    file_name = "ssq_"+today.strftime("%Y%m%d")
                    finalnum.to_csv(r'..\lottery-machine-gun\prediction_lottery\%s.csv' % file_name)
                    break

            elif lottery=="dlt": # 大乐透
                red_ball = range(1, 36)
                blue_ball = range(1, 13)
                length = len(self.prize_num)
                alternate_num = random.sample(red_ball, length)
                if len(alternate_num) != len(self.prize_num):
                    print "not enough!"
                else:
                    if np.array(alternate_num).prod() == np.array(self.prize_num).prod() and np.sum(
                            alternate_num) == np.sum(self.prize_num):  # 等于上期中奖号码
                        choice_num = random.sample(red_ball, length)
                        self.choice_nums_array.extend(choice_num)
                        self.circle_num += 1
                    else:
                        pass
                if self.circle_num>=20:
                    elapsed = (time.clock() - self.start_time)
                    print("Time used:", elapsed)
                    finalnum = pd.Series(Counter(self.choice_nums_array)).sort_values(ascending= False)
                    today = datetime.today()
                    file_name = "dlt_"+today.strftime("%Y%m%d")
                    finalnum.to_csv(r'..\lottery_guns\prediction_lottery\%s.csv' % file_name)
                    break #

def run_ssq():
    '双色球预测'
    "settings"
    last_red_num = [4, 10, 15, 19, 21, 23] # 上期蓝球顺序
    last_blue_num = []
    "run"
    llt = Lottery_choice(last_red_num)
    #llt.roll_slip_data(2)
    llt.engine("ssq")

def run_dlt():
    '大乐透预测'
    "settings"
    last_red_num = [5,19,25,31,33] # 上期蓝球顺序
    last_blue_num = []
    "run"
    llt = Lottery_choice(last_red_num)
    #llt.roll_slip_data(2)
    llt.engine("dlt")

if __name__ == "__main__":
    #run_ssq()
    run_dlt()