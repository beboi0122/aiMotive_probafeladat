import os
from sys import platform

def clear_console():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')

"""
    Class that contains data of a point 
"""
# It stores the position of the point (X, Y, Z coordinate)'
# and other data like intensity, laser ID,  pitch, yaw and distance between the point and the origin.
class Point:
    def __init__(self, intensity, laser_id, pitch, yaw, distance_m, point_x, point_y, point_z):
        self.intensity = intensity
        self.laser_id = laser_id
        self.pitch = pitch
        self.yaw = yaw
        self.distance_m = distance_m
        self.point_x = point_x
        self.point_y = point_y
        self.point_z = point_z


"""
    class that contains data of a Frame
"""
class Frame:
    def __init__(self, loc, raw_list):
        self.loc = loc
        self.raw_list = raw_list
        self.raw_list_to_points(raw_list)

    """
        from string list makes list of points 
    """
    def raw_list_to_points(self, raw_list):
        raw_list.pop(0)
        self.points = list()
        for line in raw_list:
            self.points.append(Point(
                intensity=float(line[3]),
                laser_id=float(line[4]),
                pitch=float(line[5]),
                yaw=float(line[6]),
                distance_m=float(line[7]),
                point_x=float(line[8]),
                point_y=float(line[9]),
                point_z=float(line[10])
            ))

"""
    function that reads the cvs file, split every raw and returns as a list
    parameter is the location of the file 
"""
def point_list(file_location):
    points = list()
    f = open(file_location)
    for line in f:
        points.append(line.split(','))
    f.close()
    return points

"""
    function that returns a list of multipla frames 
    parameter is a string list of the file locations
"""
def frame_list(file_location_list):
    num = 0
    frame_num = len(file_location_list)
    frames = list()
    for loc in file_location_list:
        print("LOADING FRAMES...")
        print(loc)
        print(str(num) + "  /  " + str(frame_num))
        frames.append(Frame(loc=loc, raw_list=point_list(loc)))
        num += 1
        clear_console()

    return frames

"""
    function that returns all file locations of the files in a directory 
    parameters are the location of the directory, and the extension of the files we are looking for. 
"""
def file_list_from_dir(dir_loc, endswith=".csv"):
    tmp = list()
    for file in os.listdir(dir_loc):
        if file.endswith(endswith):
            tmp.append(os.path.join(dir_loc, file))
    tmp.sort()
    return tmp
