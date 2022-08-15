import sensorParser
import numpy as np

"""
    class that create and contains statistics about points of a frame
"""


class FrameStatistic:
    def __init__(self, frame):
        self.frame_loc = frame.loc
        self.point_num = len(frame.points)
        self.analyze_points(frame)

    """
        all the analytics that need to check every point is in a single loop
        so the program should go throw the points only once
    """

    def analyze_points(self, frame):
        # x, y and z coordinates max and min value
        tmp_min_x = frame.points[0]
        tmp_max_x = frame.points[0]
        tmp_min_y = frame.points[0]
        tmp_max_y = frame.points[0]
        tmp_min_z = frame.points[0]
        tmp_max_z = frame.points[0]

        self.points_by_ID = list()
        self.points_by_ID_fail = list()

        for num in range(0, 5):
            self.points_by_ID_fail.append(0)
            self.points_by_ID.append(0)

        # loop throw all the points in the frame
        for point in frame.points:

            # min and max checking
            if point.point_x < tmp_min_x.point_x:
                tmp_min_x = point
            if point.point_x > tmp_max_x.point_x:
                tmp_max_x = point

            if point.point_y < tmp_min_y.point_y:
                tmp_min_y = point
            if point.point_y > tmp_max_y.point_y:
                tmp_max_y = point

            if point.point_z < tmp_min_z.point_z:
                tmp_min_z = point
            if point.point_z > tmp_max_z.point_z:
                tmp_max_z = point

            # faults by laser ID
            self.points_by_ID[int(point.laser_id)] += 1
            if (point.point_x == 0.0 and point.point_y == 0.0 and point.point_z == 0.0):
                self.points_by_ID_fail[int(point.laser_id)] += 1

        self.min_x_point = tmp_min_x
        self.max_x_point = tmp_max_x

        self.min_y_point = tmp_min_y
        self.max_y_point = tmp_max_y

        self.min_z_point = tmp_min_z
        self.max_z_point = tmp_max_z


"""
    returns the Equation of a Plane as a lits
    Equation of a Plane: Z = A x + B Y + D
        A = retVal[0]
        B = retVal[1]
        D = retVal[2]
        (retVal means return value)
"""
def plane_from_points(points):
    tmp_A = list()
    tmp_B = list()
    rtn_list = list()
    for i in range(len(points)):
        tmp_A.append([points[i].point_x, points[i].point_y, 1])
        tmp_B.append(points[i].point_z)
    b = np.matrix(tmp_B).T
    A = np.matrix(tmp_A)
    tmp_mtx = (A.T * A).I * A.T * b
    rtn_list.append(float(tmp_mtx[0]))
    rtn_list.append(float(tmp_mtx[1]))
    rtn_list.append(float(tmp_mtx[2]))
    return rtn_list

"""
    returns the average deviation in distance between the points of the wall and the Plane of the wall
"""
def avg_dev_point_plane(plane, points):
    point_num = len(points)
    dist_sum = 0
    for point in points:
        numerator = np.abs(plane[0] * point.point_x + plane[1] * point.point_y + -1 * point.point_z + plane[2])
        denominator = np.sqrt((plane[0] * plane[0]) + (plane[1] * plane[1]) + (-1 * -1))
        dist = numerator / denominator
        dist_sum += dist

    return dist_sum / point_num


"""
    class that contains statistics about how well it is the wall detected by the LiDAR
"""
class WallDetection:
    def __init__(self, wall_points):
        self.wall_points = wall_points
        self.plane = plane_from_points(self.wall_points)
        self.avg_dist = avg_dev_point_plane(self.plane, self.wall_points)



"""
    returns the height of the cylinder
    parameter is a list with points of the cylinder
    it selects the points of the cylinder which has the minimum and maximum z value and the difference is the 
        height of the cylinder
"""
def get_height(cylinder_points):
    min_z = cylinder_points[0].point_z
    max_z = cylinder_points[0].point_z
    for point in cylinder_points:
        if point.point_z < min_z:
            min_z = point.point_z
        if point.point_z > max_z:
            max_z = point.point_z
    return max_z - min_z


"""
    returns the width of the cylinder
    parameters are the a list with points of the cylinder and a list with points of the wall
"""
def get_width(cylinder_points, wall_points):
    point_upper_min = sensorParser.Point(0, 0, 0, 0, 0, 0, np.inf, 0)
    point_lower_max = sensorParser.Point(0, 0, 0, 0, 0, 0, -np.inf, 0)

    # selecting the tow edge of the shadow of the cylinder
    for point in wall_points:
        if point.point_z < 0 and point.point_y > 3:
            if point.point_y < point_upper_min.point_y:
                point_upper_min = point
        if point.point_z < 0 and point.point_y < 3:
            if point.point_y > point_lower_max.point_y:
                point_lower_max = point

    # equation of line that goes through the origin (0, 0, 0)
    #           and the upper edge of the shadow of the cylinder
    line1_a = point_upper_min.point_y / point_upper_min.point_x
    line1_b = -1
    line1_c = 0

    # equation of line that goes through the origin (0, 0, 0)
    #           and the lower edge of the shadow of the cylinder
    line2_a = point_lower_max.point_y / point_lower_max.point_x
    line2_b = -1
    line2_c = 0

    closest = cylinder_points[0]
    closest_dist = abs((line2_a * closest.point_x + line2_b * closest.point_y + line2_c)) / (
        np.sqrt(line2_a * line2_a + line2_b * line2_b))

    # searching the point which is the closest to the lower line
    for point in cylinder_points:
        new_dist = abs((line2_a * point.point_x + line2_b * point.point_y + line2_c)) / (
            np.sqrt(line2_a * line2_a + line2_b * line2_b))
        if closest_dist > new_dist:
            closest = point
            closest_dist = new_dist

    # calculate the distance between the point which is the closest to the lower line
    #       and the upper line. It is the width of the cylinder
    dis = np.abs((line1_a * closest.point_x + line1_b * closest.point_y + line1_c)) / (
        np.sqrt(line1_a * line1_a + line1_b * line1_b))

    return dis

"""
    class that contains statistics about how well it is the cylinder detected by the LiDAR
"""
class CylinderDetection:
    def __init__(self, cylinder_points, wall_points):
        self.height = get_height(cylinder_points)
        self.width = get_width(cylinder_points, wall_points)




