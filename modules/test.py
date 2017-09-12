import math
from pyecharts import Polar

data = []
for i in range(101):
    theta = i / 100 * 360
    r = 5 * (1 + math.sin(theta / 180 * math.pi))
    data.append([r, theta])
hour = [i for i in range(1, 25)]
polar = Polar("极坐标系示例", width=1200, height=600)
polar.add("Love", data, angle_data=hour, boundary_gap=False,start_angle=0)
# polar.render()