import cv2
import numpy as np
import typing

path = "map2.png"
img = cv2.imread(path)
print(img)
def check_point(input,
                point: typing.Tuple,color:typing.Tuple):
    
    square = [(point[0] + dy, point[1] + dx)
            for dy in range(3)
            for dx in range(3)]
    output = np.ndarray.copy(input)
    for p in square:
        output[p] = color  # 適当な灰色
    return output

#start_point = (200, 595)
#goal_point = (380, 240)
#goal_point = (336,358)
#start_point = (90,200)
start_point = (427,488)
goal_point = (454,484)
img = check_point(img, start_point,(150,0,0))
img = check_point(img, goal_point,(0,0,150))
print(img.dtype)
cv2.imshow("output-3.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()