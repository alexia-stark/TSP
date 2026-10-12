from os import listdir
from os.path import isfile, join

class Manage_File:

    def __init__(self, filename = None):
        self.__filename = filename
        self.__path = './data'
        
    def get_files(self):
        """
        Gets all the files in the data folder
        :return list of strings : the filenames of the files
        """
        files = []
        for file in listdir(self.__path):
            if isfile(join(self.__path, file)):
                files.append(file)
        return files

    def read_file_and_create_points(self):
        """
        Reads a given file from the file list.
        :raises NameError: if the file does not exist in the folder
        :return (points, maxX, maxY): the tuple consisting of the points coordonates and the maxx and maxy
        """
        the_file = self.__filename
        if the_file in self.get_files():
            the_file =  join(self.__path, the_file)
            points = []
            maxX = -1.0
            maxY = -1.0
            with open(the_file) as f:
                for line in f:
                    point_coordonates = line.split()
                    px = float(point_coordonates[1])
                    py = float(point_coordonates[2])
                    if self.__filename != 'berlin52.txt':
                        px = px * 2
                        py = py* 2
                    points.append( (px, py))
                    if px > maxX:
                        maxX = px
                    if py > maxY:
                        maxY = py
            
            return (points,maxX,maxY)
        else:
            raise NameError
        