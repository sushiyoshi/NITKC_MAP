#参考：
# https://qiita.com/ikngtty/items/ffef099b1d81f3bff5c2、
# https://github.com/ikngtty/solve_maze

import cv2
import numpy as np
import collections
import math
import heapq as hq
import typing
Point = collections.namedtuple("Point","y x")
Point._delta_udlr = (
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1)
)
def _Point____add__(self, other):
    return Point(self.y + other.y,self.x + other.x)

def _Point__udlr(self):
    return [self + delta for delta in self._delta_udlr]

Point.__add__ = _Point____add__
Point.udlr = _Point__udlr

def heuristic_cost(point1:Point,point2:Point) -> float:
    return math.sqrt(pow(point1.x-point2.x,2) + pow(point1.y-point2.y,2))

def is_passable(pixel) -> bool:
    return pixel > 200

class Node:
    __slots__ = ("point","cost","heuristic_cost","parent")
    def __init__(self,point:Point,cost:int,heuristic_cost:float,parent):
        self.point = point
        self.cost = cost
        self.heuristic_cost = heuristic_cost
        self.parent = parent

    @property
    def priority_score(self):
        return self.cost + self.heuristic_cost

    @property
    def _compare_values(self):
        return (self.priority_score,self.cost,self.point)
    
    def __eq__(self, other):
        return self._compare_values < other._compare_values

    def __lt__(self, other):
        return self._compare_values < other._compare_values

def get_path(img,start_point:Point,goal_point:Point) -> typing.List[Point]:
    goal_node = _get_goal_node(img,start_point,goal_point)
    if goal_node is None:
        raise Exception("The goal is not found")

def _get_goal_node(img,start_point:Point,goal_point:Point) -> Node:
    def is_goal(node:Node):
        return node.point == goal_point
    
    start_node=Node(point=start_point,cost=0,heuristic_cost=heuristic_cost(goal_point,start_point),parent=None)
    if is_goal(start_node):
        return start_node
    shape=img.shape
    #print(is_passable(img[start_point][0]))
    open_node_map={start_node.point:start_node}
    node_hq=[start_node]
    while (len(node_hq) > 0):
        center_node = hq.heappop(node_hq)
        next_cost = center_node.cost+1
        next_nodes = [Node(point=p,
        cost=next_cost,
        heuristic_cost=heuristic_cost(goal_point,p),
        parent=center_node)
        for p in center_node.point.udlr()
            if p.y>=0
            and p.x>=0
            and p.y < shape[0]
            and p.x < shape[1]
            and open_node_map.get(p) is None
            and is_passable(img[p])]
        for node in next_nodes:
            if is_goal(node):
                return node
            open_node_map[node.point] = node
            hq.heappush(node_hq,node)
    return None

def get_path(img,start_point: Point,goal_point: Point)-> typing.List[Point]:
    goal_node = _get_goal_node(img, start_point, goal_point)
    if goal_node is None:
        raise Exception("The goal is not found.")
    path_reverse = [goal_node.point]
    parent_node = goal_node.parent
    while(parent_node is not None):
        path_reverse.append(parent_node.point)
        parent_node = parent_node.parent
    return list(reversed(path_reverse))

def draw_path_fromto(input, start_point, goal_point):
    path = get_path(input, start_point, goal_point)
    delta_square = [Point(y, x)
                    for y in range(3)
                    for x in range(3)]
    spread_path = [p + d
                for p in path
                for d in delta_square]
    output = np.ndarray.copy(input)
    for p in spread_path:
        output[p] = 150
    return output
def paint_path(input):
    output = np.ndarray(shape=input.shape + (3,))
    for iy, row in enumerate(input):
        for ix, grayscale in enumerate(row):
            if grayscale > 200:
                output[iy, ix] = [255, 255, 255]
            elif grayscale < 50:
                output[iy, ix] = [0, 0, 0]      
            else:
                output[iy, ix] = [255, 0, 0]
    return output

def get_plot(start_point, goal_point):
    img1 = cv2.imread("map22.png")
    img1gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret,mask=cv2.threshold(img1gray,250,255,cv2.THRESH_BINARY)
    cv2.imwrite("output-3.png", mask)
    path = get_path(mask, start_point, goal_point)
    return path[::5]

#テスト用コード。読まなくて良い
if __name__ == "__main__":
    img1 = cv2.imread("map22.png")
    img1gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret,mask=cv2.threshold(img1gray,250,255,cv2.THRESH_BINARY)
    cv2.imwrite("output-3.png", mask)
    start_point = Point(230, 519)
    goal_point = Point(250,545)
    output = draw_path_fromto(mask,start_point,goal_point)
    #output = output[::5]
    output = paint_path(output)
    cv2.imshow("output-3.png", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()