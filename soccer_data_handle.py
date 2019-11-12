# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: soccer_data_handle.py
@Time: 2019/11/12 22:01
@Motto：I have a bad feeling about this.
"""
from bs4 import BeautifulSoup
import os
import pandas as pd

NoneDef = lambda x: OutRange(x) if not None else None
OutRange = lambda x: x.contents[0].encode('utf-8') if len(x.contents)!=0 else None

class soccer_data(object):

    def __init__(self):
        pass

    def jiexi(self, html):
        soup = BeautifulSoup(open(html), "html.parser")
        if len(soup.find_all("tr", class_="each_match"))!=0:
            date = filter(str.isdigit,  os.path.split(html)[-1]) # 日期
            day_soccre_data = []
            win, draw, lose = "0", "0", "0"
            for txt in soup.find_all("tr", result="100"):
                match = txt['type'].encode('utf-8') # 赛事
                match_id = txt['matchid'].encode('utf-8')
                hometeam = txt.find("a", class_="ctrl_homename") # 主名
                awayteam = txt.find("a", class_="ctrl_awayname") # 客名
                homescore = txt.find("b", class_="font_red ctrl_homescore") # 主队得分
                awayscore = txt.find("b", class_="font_red ctrl_awayscore")  # 主队得分
                betopt_list = [] # 胜平负赔率
                for betopts in txt.find("td", class_="ctrl_self_betopt").find_all("span"):
                    betopt_list.append(betopts.contents[0])
                if len(betopt_list)!=0:
                    win = betopt_list[0].encode('utf-8') # 胜率
                    draw = betopt_list[1].encode('utf-8') # 平局
                    lose = betopt_list[-1].encode('utf-8') # 负
                result = txt.find("td", class_="ctrl_result fontb font_red") # 赛果
                print [date, match, match_id, hometeam, awayteam, homescore, awayscore, win, draw, lose, result]
                print NoneDef(hometeam)
                print NoneDef(awayteam)
                print NoneDef(homescore)
                print NoneDef(awayscore)
                print NoneDef(result)
                day_soccre_data.append([date, match, match_id, NoneDef(hometeam), NoneDef(awayteam), NoneDef(homescore), NoneDef(awayscore), win, draw, lose, NoneDef(result)])
                # date, match, match_id, hometeam, awayteam, homescore, awayscore, win, draw, lose, result
            td_df = pd.DataFrame(day_soccre_data)
            if td_df.empty:
                pass
            else:
                td_df.columns = ["date", "match", "match_id", "hometeam", "awayteam", "homescore", "awayscore", "win", "draw", "lose", "result"]
                self.data2hdf(date, td_df)
        else:
            pass

    def data2hdf(self, date, df):
        key = '/%s' % (date)
        df.to_hdf(r"D:\database\soccer_jc_lottery.h5", key=date, complevel=9, complib='zlib', format='table')
        print "{}".format(key)

def run(path):
    path = os.path.expanduser(path)
    for (dirname, subdir, subfile) in os.walk(path):
        for f in subfile:
            fl = os.path.join(dirname, f)
            ss = soccer_data()
            ss.jiexi(fl)

if __name__ == "__main__":
    #path = r"C:\Users\Administrator\Downloads\html\2011"
    #s_html = r"C:\Users\Administrator\Downloads\html\2011\01\2011-01-03.html"
    year = "2017"
    path = r"C:\Users\Administrator\Downloads\html\{}".format(year)
    run(path)