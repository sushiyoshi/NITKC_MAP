from xmlrpc.client import Boolean
import mysql.connector
import sys
from map_linetrace import get_plot,Point
cnx = None

class CoordinatesList:
    __slots__=("cnx","cursor","coordinatesList")
    def __init__(self,pswd:str):
        try:
            self.cnx = mysql.connector.connect(
                user='root',  # ユーザー名
                password=pswd,  # パスワード
                host='localhost',  # ホスト名(IPアドレス）
                db='coordinatesList'
            )
            self.cursor=self.cnx.cursor()
        except Exception as e:
            print(f"Error Occurred: {e}")

    def isExistCoordinatesList(self,name:str)->Boolean:
        sql="""
        show tables like '{nm}';
        """.format(nm=name)
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return len(rows) > 0
        except Exception as e:
            print(e)
            return False
    def getCoordinatesList(self,name:str):
        sql="""
        select x,y from {nm};
        """.format(nm=name)
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            #result = [{"x":ele[0],"y":ele[1]} for ele in rows]
            result = [Point(ele[1],ele[0]) for ele in rows]
            return result
        except Exception as e:
            Exception(e)
            return []
    def createCoordinatesList(self,table_name:str,coordinatesList):
        sql="""
            CREATE table {tbname}(
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                x float,
                y float
            );
            """.format(tbname=table_name)
        print(sql)
        try:
            self.cursor.execute(sql)
            for elem in coordinatesList:
                sql="""
                insert INTO {tbname}(x,y) values({x},{y});
                """.format(tbname=table_name,x=elem.x,y=elem.y)
                print("adasdadss")
                try:
                    self.cursor.execute(sql)
                    print("insert")
                except Exception as e:
                    Exception(e)
            self.cnx.commit()
        except Exception as e:
            print("dameka~~")
            Exception(e)

    def close(self):
        self.cnx.close()

# if __name__ == "__main__":
#     coordinatesList = CoordinatesList("kosenmap2022")
#     print(coordinatesList.isExistCoordinatesList("test"))
#     print(coordinatesList.getCoordinatesList("test222"))
#     plotList=get_plot(Point(262,593),Point(450,484))
#     print(plotList)
#     #coordinatesList.createCoordinatesList("test222",plotList)
#     coordinatesList.close()
