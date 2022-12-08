from xmlrpc.client import Boolean
import mysql.connector
import sys
from map_linetrace import get_plot,Point
cnx = None
class LocationList:
    __slots__=("cnx","cursor")
    def __init__(self,pswd:str):
        try:
            self.cnx = mysql.connector.connect(
                user='root',  # ユーザー名
                password=pswd,  # パスワード
                host='localhost',  # ホスト名(IPアドレス）
                db='locationList'
            )
            self.cursor=self.cnx.cursor()
        except Exception as e:
            print(f"Error Occurred: {e}")
    def getArea(self,location):
        sql="""
        select area from locationList where location = "{nm}";
        """.format(nm=location)
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if len(rows)>0 and len(rows[0])>0:
                return rows[0][0]
            else:
                print(sql)
                return False
        except Exception as e:
            print(e)
            return False
    def close(self):
        self.cnx.close()

class CoordinatesList:
    __slots__=("cnx","cursor")
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
        try:
            self.cursor.execute(sql)
            for elem in coordinatesList:
                sql="""
                insert INTO {tbname}(x,y) values({x},{y});
                """.format(tbname=table_name,x=elem.x,y=elem.y)
                try:
                    self.cursor.execute(sql)
                    print("insert")
                except Exception as e:
                    Exception(e)
            self.cnx.commit()
        except Exception as e:
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

if __name__ == "__main__":
    location_list = LocationList(sys.argv[1])
    location_name = input("Enter the location name: ")
    result = location_list.getArea(location_name)
    if result:
        print(f"The area of the location is: {result}")
    else:
        print(f"Could not find the location: {location_name}")
    location_list.close()