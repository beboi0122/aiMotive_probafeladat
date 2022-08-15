import os
import sys
import sensorParser
import statistics

def menu(frames):
    sensorParser.clear_console()
    print("Menu options:")
    print("\t0 --> CLOSE THE PROGRAM")
    print()
    print("\t1 --> Run full statistics")
    print()
    print("\t2 --> Statistics about how well the wall is detected by the LiDAR")
    print()
    print("\t3 --> Statistics about how well the cylinder is detected by the LiDAR")
    print()

    inp = input("Choose menu option: ")
    if inp == "0":
        exit(0)
    if inp == "1":
        full_statistics(frames)
        return
    if inp == "2":
        wall_statistics(frames)
        return
    if inp == "3":
        cylinder_statistics(frames)
        return
    else:
        sensorParser.clear_console()
        print("Incorrect menu option! Press enter to return the menu.")
        input()

def full_statistics(frames):
    c = 0
    for frame in frames:
        stat = statistics.FrameStatistic(frame)
        print("\u0332".join(frame.loc))
        print()
        print("\u0332".join("Statistics about the frame"))
        print("\tPoint where x coordinate is minimum: (" + str(stat.min_x_point.point_x) + " , " +
              str(stat.min_x_point.point_y) + " , " +
              str(stat.min_x_point.point_z) + ") \n\tPoint where x coordinate is maximum: (" +
              str(stat.max_x_point.point_x) + " , " +
              str(stat.max_x_point.point_y) + " , " +
              str(stat.max_x_point.point_z) + ")")
        print("\n\tPoint where y coordinate is minimum: (" + str(stat.min_y_point.point_x) + " , " +
              str(stat.min_y_point.point_y) + " , " +
              str(stat.min_y_point.point_z) + ")  \n\tPoint where y coordinate is maximum: (" +
              str(stat.max_y_point.point_x) + " , " +
              str(stat.max_y_point.point_y) + " , " +
              str(stat.max_y_point.point_z) + ")")
        print("\n\tPoint where x coordinate is minimum: (" + str(stat.min_z_point.point_x) + " , " +
              str(stat.min_z_point.point_y) + " , " +
              str(stat.min_z_point.point_z) + ")  \n\tPoint where z coordinate is maximum: (" +
              str(stat.max_z_point.point_x) + " , " +
              str(stat.max_z_point.point_y) + " , " +
              str(stat.max_z_point.point_z) + ")")
        print("")

        for num in range(0, 5):
            print("\tLaser ID: " + str(num) + "\t\tNumber of points: " +
                  str(stat.points_by_ID[num]) + "\t\t Number of fails: " +
                  str(stat.points_by_ID_fail[num]))

        print("")

        print("\u0332".join("Statistics about how well the wall is detected by the LiDAR"))
        wall_points = list()
        cylinder_points = list()
        for point in frame.points:
            # selecting the points, that belongs to the wall
            # Z coordinates should not contain the points of the floor
            if point.point_x > 5.7 and 3.6 > point.point_y > -2.75 and point.point_z > -0.92:
                wall_points.append(point)

            if 4.5 > point.point_x > 4.25 and 2.5 > point.point_y > 2.1:
                cylinder_points.append(point)

        wallStat = statistics.WallDetection(wall_points)
        print("\tEquation of a Plane from the points of the Wall:")
        print("\t\tz = " + str(wallStat.plane[0]) + "x + " + str(wallStat.plane[1]) + "y + " + str(wallStat.plane[2]))

        print("\tAverage Deviation in distance between the points of the wall and the Plane of the wall:")
        print("\t\t" + str(wallStat.avg_dist))

        print("")

        print("\u0332".join("Statistics about how well the cylinder is detected by the LiDAR"))
        cylStat = statistics.CylinderDetection(cylinder_points, wall_points)
        print("\t" + "Height of the cylinder:")
        print("\t\t" + str(cylStat.height))
        print("\t" + "Width of the cylinder:")
        print("\t\t" + str(cylStat.width))
        print("\t" + "Width / Height:")
        c += cylStat.width / cylStat.height
        print("\t\t" + str(cylStat.width / cylStat.height))
        print("\n\n\n")


    print()
    print("Press enter to return the menu.")
    input()

def wall_statistics(frames):
    for frame in frames:
        print("\u0332".join(frame.loc))
        print()
        print("\u0332".join("Statistics about how well the wall is detected by the LiDAR"))
        wall_points = list()
        cylinder_points = list()
        for point in frame.points:
            # selecting the points, that belongs to the wall
            # Z coordinates should not contain the points of the floor
            if point.point_x > 5.7 and 3.6 > point.point_y > -2.75 and point.point_z > -0.92:
                wall_points.append(point)

            if 4.5 > point.point_x > 4.25 and 2.5 > point.point_y > 2.1:
                cylinder_points.append(point)

        wallStat = statistics.WallDetection(wall_points)
        print("\tEquation of a Plane from the points of the Wall:")
        print("\t\tz = " + str(wallStat.plane[0]) + "x + " + str(wallStat.plane[1]) + "y + " + str(wallStat.plane[2]))

        print("\tAverage Deviation in distance between the points of the wall and the Plane of the wall:")
        print("\t\t" + str(wallStat.avg_dist))
        print("\n\n\n")

    print()
    print("Press enter to return the menu.")
    input()

def cylinder_statistics(frames):
    ratio_sum = 0
    for frame in frames:
        wall_points = list()
        cylinder_points = list()
        for point in frame.points:
            # selecting the points, that belongs to the wall
            # Z coordinates should not contain the points of the floor
            if point.point_x > 5.7 and 3.6 > point.point_y > -2.75 and point.point_z > -0.92:
                wall_points.append(point)

            if 4.5 > point.point_x > 4.25 and 2.5 > point.point_y > 2.1:
                cylinder_points.append(point)
        print("\u0332".join(frame.loc))
        print()
        print("\u0332".join("Statistics about how well the cylinder is detected by the LiDAR"))
        cylStat = statistics.CylinderDetection(cylinder_points, wall_points)
        print("\t" + "Height of the cylinder:")
        print("\t\t" + str(cylStat.height))
        print("\t" + "Width of the cylinder:")
        print("\t\t" + str(cylStat.width))
        print("\t" + "Width / Height:")
        ratio_sum += cylStat.width / cylStat.height
        print("\t\t" + str(cylStat.width / cylStat.height))
        print("\n\n\n")

    print("average ratio of the height and the width:", ratio_sum / len(frames))

    print()
    print("Press enter to return the menu.")
    input()


"""
    main function, entry point of the program 
"""

def main():
    # checking if the program has any Command Line Argument. IF not the program stops
    """the location of the directory, or the cvs file should be given as Command Line Argument"""
    if len(sys.argv) == 1:
        print("You have to give a file or directory location as Command Line Argument")
        exit(0)

    fpath = sys.argv[1]
    filenames = list()

    """checking if the direction points to a file or a directory """
    if os.path.isdir(fpath):
        filenames = sensorParser.file_list_from_dir(fpath)
    else:
        filenames.append(fpath)

    # list of the frames in the directory. (if it was only a file it is a list with one element)
    frames = sensorParser.frame_list(filenames)


    while 1:
        menu(frames)


if __name__ == '__main__':
    main()
