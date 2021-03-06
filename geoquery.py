#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# geoquery.py
# Sample Wi2 Geo query demo script

# Query for overlapping geofences based on current location of user mobile device
# このスクリプトは、Wi2パートナーフェンスのジオスペースクエリを表示します。
# ユーザーは、GPSが重複したり、近くのジオフェンスを見つけるために、座標を選択しました
# この機能は、すぐにモバイルデバイスの位置の正しいパートナーの場所を取得することです

import json
import requests
from pprint import pprint
from sys import exit
from time import time

def main():
    myAccount = "bradwbonn"
    print "\n デモンストレーションの種類を選択してください"
    print " 1: 複雑なジオフェンス    (complex geofence)"
    print " 2: 単純な座標            (simple coordinates)"
    demoType = int(raw_input(" (1-2) > "))
    if demoType == 1:    
        myDB = "fencemaster" # 複雑なジオフェンスオブジェクトのデータベース
        myAuth = ("tinetiffeencesidetteryto","1d181a41ebbe621ad2cf7fd5780261efeae17c7e") # APIキーは読み取り専用です
    elif demoType ==2:
        myDB = "testfences" # 座標点のデータベース
        myAuth = ("ieuredislonlyeacticullea","e346439405bc87a5ea7adb3941f5f92bcf83a3c2")
    else:
        exit(" 無効入力 ...\n")
    myDDoc = "geoIdx"
    myIndex = "newGeoIndex"
    limit = 20 # データベースから返されたパートナーフェンスの数
    myCoords = chooseCoordinates()
    myRelation = getRelationType()
    myQuery = showQuery(myCoords, myRelation, myAccount, myDB, myDDoc, myIndex, limit)
    myJSON = getFences(myQuery, myAuth)
    showResponse(myJSON)
    
def chooseCoordinates():
    print "\n 以下のオプションから座標を選択してください:"
    print " 1. 羽田空港ターミナル Haneda Airport Terminal"
    print " 2. 大仏鎌倉 Great Buddha Kamakura"
    print " 3. Wi2 企業のオフィス"
    print " 4. カスタム選択"
    menuOption = int(raw_input(" (1-4) > "))
    if menuOption == 1:
        return [139.78111267089844, 35.55436500410275]
    if menuOption == 2:
        return [139.535700, 35.316698]
    if menuOption == 3:
        return [139.769246, 35.673325]
    if menuOption == 4:
        longitude = raw_input(" 入力経度してください: ")
        latitude = raw_input(" 入力してください緯度: ")
        return [longitude, latitude]

def getRelationType():
    print "\n オプションを選択してください: "
    print " 1. contains 含む"
    print " 2. intersects 交わる"
    print " 3. nearest 最寄り"
    print " 4. radius 半径"
    return int(raw_input(" (1-4) > "))

def showQuery(coords, relation, account, db, ddoc, index, limit):
    WKT = "point({0}+{1})".format(coords[0],coords[1])
    queryString = "https://{0}.cloudant.com/{1}/_design/{2}/_geo/{3}?g={4}&limit={5}".format(account,db,ddoc,index,WKT,limit)
    if relation == 1:
        queryString = queryString + "&relation=contains"
    elif relation == 2:
        queryString = queryString + "&relation=intersects"
    elif relation == 3:
        queryString = "{0}&nearest=true".format(queryString)
    elif relation == 4:
        radius = int(raw_input(" 検索する点の周りの半径 (メートル) > "))
        queryString = "https://{0}.cloudant.com/{1}/_design/{2}/_geo/{3}?lat={4}&lon={5}&radius={6}&limit={7}".format(
            account,
            db,
            ddoc,
            index,
            coords[1],
            coords[0],
            radius,
            limit
        )
    print "\n データベースクエリURI: "
    print queryString
    return queryString

def getFences(query,myAuth):
    startTime = time()
    r = requests.get(
        query,
        headers = {'Content-Type': 'application/json'},
        auth = myAuth
    )
    endTime = time()
    print "\n 実行パフォーマンス: {0} 秒".format(round((endTime - startTime),2))
    if r.status_code != 200:
        exit("\n データベースエラー HTTP {0}".format(r.status_code))
    jsonResponse = r.json()
    if len(jsonResponse['rows']) == 0:
        exit("\n 一致する地理空間エンティティはありません No geo entities match\n")
    return jsonResponse

def showResponse(jsonResponse):
    print "\n この場所はジオフェンスにあります"
    for row in jsonResponse['rows']:
        print " " + row['id']
    showMe = raw_input("\n JSONを見たいですか？(y/n) > ")
    if showMe == "y" or showMe == "Y":
        print "\n JSONレスポンス:"
        pprint(jsonResponse)

if __name__ == "__main__":
    main()