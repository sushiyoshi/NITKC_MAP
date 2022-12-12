from curses import start_color
from tracemalloc import start
from flask import Flask, render_template
from mygraph import GraphApp
from map_linetrace import get_plot,Point
from flask import request
import sys
from mymysql import CoordinatesList,LocationList
app = Flask(__name__)

#左枠に施設を表示
def AreaTextConvert(area):
    if area[1] is None:
        #floorがNULLでなければ
        return area[0]
    else:
        #floorがNULLなら
        return area[0] + str(area[1]) + "階"
#最初の入力画面
@app.route("/")
def index():
    return render_template("index.html")
#経路表示画面
@app.route("/mappage", methods=['GET'])
def mappage():
    #ユーザー入力を受け取る
    current = request.args.get('loc1', '')
    target = request.args.get('loc2', '')
    #Location-Areaテーブルにアクセス
    location_list = LocationList(sys.argv[2])
    #LocationをAreaに変換(無効な場合、Falseを返す)
    currentArea = location_list.getArea(current)
    targetArea = location_list.getArea(target)
    #無効なLocationを取得した際、エラーページを表示
    if not(currentArea and targetArea):
        return render_template("error.html",error_text="location not found")
    #なぜか配列の中にタプルが入っている形式で返されるので、[0][0]でアクセスしている。(やばい)
    currentAreaText = currentArea[0][0]
    targetAreaText = targetArea[0][0]
    #地図左の枠に表示する用のテキストを作る
    currentAreaFloor = AreaTextConvert(currentArea[0])
    targetAreaFloor = AreaTextConvert(targetArea[0])
    #現在地から目的地への最短経路を取得
    result = get_node_path(currentAreaText,targetAreaText)
    #距離を取得
    weight = result[0]['weight']
    #経由するノードを取得
    path = result[0]['path'][::2]
    #経路を形成する点の座標リストを格納
    pathList = []
    relationships = result[1]
    #座標リストデータベースにアクセス
    coordinatesList = CoordinatesList(sys.argv[2])
    # 以下クソコ
    for current in relationships:
        re = []
        table_name=current._properties['name']
        #座標リストデータベース上に該当する座標リストが存在したら(→mymysql.py)
        if coordinatesList.isExistCoordinatesList(table_name):
            print("Get a coordinates list")
            re = coordinatesList.getCoordinatesList(table_name)
        else:
        #存在しなかったら、新たに座標リストを作成
            print("Create a new coordinates list")
            pointList =[]
            for node in current.nodes:
                #ここが一番やばい部分なので、解読しなくて良いです。

                #グラフデータベースが返したリレーションシップのリストを読み込んで、
                #リレーションシップに接続されているノードが持っている座標を取得しています。

                #ノードが複数の座標を持っていた場合、どの座標を採用するかを設定するインデックス(通常は存在しない)
                index = "index_{}".format(node.id)
                j = current._properties[index] if index in current._properties else 0
                pointList.append(Point(node._properties['y'][j],node._properties['x'][j]))
            #グラフデータベースから読み込んだ二つの座標を結ぶ経路の座標リストをOpenCVで生成(→map_linetrace.py)
            re = get_plot(pointList[0],pointList[1])
            #生成した座標リストをMySQLに登録(→mymysql.py)
            coordinatesList.createCoordinatesList(table_name,re)
        #座標リストにリレーションシップを形成する点の座標を登録
        pathList.extend(re)
    coordinatesList.close()
    return render_template("mappage.html",path=pathList,currentAreaFloor=currentAreaFloor,targetAreaFloor=targetAreaFloor)

#グラフデータベースにアクセス
def get_node_path(Area1,Area2):
    uri = "neo4j+s://cfa2fb67.databases.neo4j.io:7687"
    user = "neo4j"
    password = sys.argv[1]
    graphapp = GraphApp(uri, user, password)

    result = graphapp.find_shortestPath(Area1,Area2)
    graphapp.close()
    return result

if __name__ == "__main__":
    app.run(debug=True)