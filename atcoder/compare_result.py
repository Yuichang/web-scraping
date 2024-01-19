# 2人のAtCoderユーザーの名前を入力すると、共通のRatedコンテストを調べて勝敗を出す

import requests
import time
import sys
from collections import defaultdict
from sortedcontainers import SortedSet, SortedList, SortedDict

print("コンマ区切りで比較したい2人を入力してください")

usernames = list(map(str, input().split(',')))
if len(usernames) != 2:
    print("エラーが発生しました。")
    sys.exit(-1)

users = {}
for user in usernames:
    users[user] = requests.get(
        "https://atcoder.jp/users/"+user+"/history/json").json()


rated_contests = defaultdict(SortedSet)
memo_places = defaultdict()

for user in usernames:
    for i in range(len(users[user])):
        if users[user][i]["IsRated"] == True:
            rated_contests[user].add(users[user][i]["ContestScreenName"][:6])
            memo_places[(user, users[user][i]["ContestScreenName"][:6])
                        ] = users[user][i]["Place"]

valid_contests = rated_contests[usernames[0]] & rated_contests[usernames[1]]

if len(valid_contests) == 0:
    print("共通のRatedなコンテストがありません。")
    sys.exit(-1)


detail = []
w1 = w2 = 0
win_player = [usernames[0], usernames[1], "Draw"]

for contest in valid_contests:
    victory = 2
    if memo_places[(usernames[0], contest)] < memo_places[(usernames[1], contest)]:
        w1 += 1
        victory = 0
    elif memo_places[(usernames[0], contest)] > memo_places[(usernames[1], contest)]:
        w2 += 1
        victory = 1
    detail.append(
        (contest, memo_places[(usernames[0], contest)], memo_places[(usernames[1], contest)], win_player[victory]))

print(w1, w2, sep='-')
if (w1 > w2):
    print("Win "+usernames[0])
elif (w1 < w2):
    print("Win "+usernames[1])
else:
    print("Draw")

print("詳細を表示しますか？ 1:する 0:しない")

is_print_detail = input()
if is_print_detail == '1':
    print(*detail, sep='\n')
