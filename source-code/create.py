import random

from PIL import Image, ImageDraw, ImageColor
import random as rnd
import re


class Maze:
    class __MazeTile:
        def __init__(self, X, Y, isWall=True):

            self.workedOn = False

            self.wall = isWall
            self.coordinateX = X
            self.coordinateY = Y

            self.connectTo = []

        def __str__(self):
            return "X: " + str(self.coordinateX) + " " + "Y: " + str(self.coordinateY) + " " + str(self.connectTo)

        def __repr__(self):
            return "__MazeTile, wall = {}, worked on = {} ,x = {}, y = {} ---".format(self.wall, self.workedOn,
                                                                                      self.coordinateX,
                                                                                      self.coordinateY)

    class __MazeError(Exception):
        def __init__(self, string, errorcode):
            self.string = string
            self.errorcode = errorcode

        def __str__(self):
            return (str(self.string) + " |Errorcode: {}".format(self.errorcode))

    def __init__(self, dimensionX, dimensionY, difficulty=0, mazeName="maze"):

        if not isinstance(dimensionX, int) or not isinstance(dimensionY, int):
            raise self.__MazeError(
                "Maze dimensions have to be an integer > 0", 1)

        if dimensionX < 1 or dimensionY < 1:
            raise self.__MazeError(
                "Maze dimensions have to be an integer > 0", 1)

        if not isinstance(mazeName, str):
            raise self.__MazeError(
                "The name of the Maze has to be a string", 1)

        self.sizeX = dimensionX

        self.sizeY = dimensionY

        self.name = mazeName

        self.__mazeIsDone = False

        self.mazeList = []

        self.wallList = []

        self.tileList = []

        self.mazeString = ""

        self.difficulty = difficulty

        if (self.difficulty == 0):
            self.makeMazeGrowTree(weightHigh=50, weightLow=50)
            self.makeMazeBraided(50)
        elif (self.difficulty == 1):
            self.makeMazeGrowTree(weightHigh=70, weightLow=70)
            self.makeMazeBraided(25)
        else:
            self.makeMazeGrowTree(weightHigh=100, weightLow=100)
            self.makeMazeBraided(0)

        self.name = self.saveImage(self.makePP())

    def __str__(self):
        self.mazeString = ""

        for row in self.mazeList:

            for tile in row:
                self.mazeString += "{:^20}".format(str(tile.connectTo))

            self.mazeString += "\n"

        return self.mazeString

    def __repr__(self):
        return "This is a Maze with width of {} and height of {}".format(self.sizeX, self.sizeY)

    def __getNextTiles(self, X, Y):
        if X < 0 or Y < 0:

            raise self.__MazeError("Inputs have to be an integer > 0", 1)

        templist = []

        try:
            if Y == 0:
                pass
            else:
                templist.append(self.mazeList[Y - 1][X])

        except(IndexError):
            pass

        try:
            templist.append(self.mazeList[Y + 1][X])
        except(IndexError):
            pass

        try:
            if X == 0:
                pass
            else:
                templist.append(self.mazeList[Y][X - 1])
        except(IndexError):
            pass

        try:
            templist.append(self.mazeList[Y][X + 1])
        except(IndexError):
            pass

        return templist

    def __connectTiles(self, tileA, tileB):
        X1 = tileA.coordinateX
        Y1 = tileA.coordinateY

        X2 = tileB.coordinateX
        Y2 = tileB.coordinateY

        if X1 == X2:

            if Y1 < Y2:

                tileA.connectTo.append("S")
                tileB.connectTo.append("N")

            elif Y1 > Y2:
                tileA.connectTo.append("N")
                tileB.connectTo.append("S")

        else:
            if X1 < X2:

                tileA.connectTo.append("E")
                tileB.connectTo.append("W")

            else:
                tileA.connectTo.append("W")
                tileB.connectTo.append("E")

        return True

    def __connectTilesWithString(self, tile, direction):
        if direction == "N":

            try:

                if tile.coordinateY == 0:
                    raise IndexError

                self.mazeList[tile.coordinateY -
                              1][tile.coordinateX].connectTo.append("S")
                tile.connectTo.append("N")

            except(IndexError):
                raise self.__MazeError(
                    "This tile can not connect in this direction", 2)

        elif direction == "S":

            try:
                self.mazeList[tile.coordinateY +
                              1][tile.coordinateX].connectTo.append("N")
                tile.connectTo.append("S")

            except(IndexError):
                raise self.__MazeError(
                    "This tile can not connect in this direction", 2)

        elif direction == "W":

            try:
                if tile.coordinateX == 0:
                    raise IndexError
                self.mazeList[tile.coordinateY][tile.coordinateX -
                                                1].connectTo.append("E")
                tile.connectTo.append("W")

            except(IndexError):
                raise self.__MazeError(
                    "This tile can not connect in this direction", 2)

        elif direction == "E":

            try:
                self.mazeList[tile.coordinateY][tile.coordinateX +
                                                1].connectTo.append("W")
                tile.connectTo.append("E")

            except(IndexError):
                raise self.__MazeError(
                    "This tile can not connect in this direction", 2)

        else:
            raise self.__MazeError("This was not a direction string", 1)

        return True

    def __makeEntryandExit(self, random=False):
        if random:

            tile = rnd.choice(self.mazeList[0])
            tile.connectTo.append("N")

            tile = rnd.choice(self.mazeList[-1])
            tile.connectTo.append("S")
        else:
            self.mazeList[0][0].connectTo.append("N")
            self.mazeList[-1][-1].connectTo.append("S")

        return True

    def makeMazeSimple(self):
        if self.__mazeIsDone:
            raise self.__MazeError("Maze is already done", 3)

        for indexY in range(0,
                            self.sizeY):
            templist = []

            for indexX in range(0, self.sizeX):
                newTile = self.__MazeTile(indexX, indexY, isWall=False)
                templist.append(newTile)

            self.mazeList.append(templist)

        frontList = []

        startingtile = rnd.choice(rnd.choice(self.mazeList))

        startingtile.workedOn = True

        frontList += self.__getNextTiles(startingtile.coordinateX,
                                         startingtile.coordinateY)

        while len(
                frontList) > 0:

            newFrontTiles = []
            workedOnList = []

            rnd.shuffle(frontList)
            nextTile = frontList.pop()
            nextTile.workedOn = True

            tempList = self.__getNextTiles(
                nextTile.coordinateX, nextTile.coordinateY)

            for tile in tempList:
                if tile.workedOn:

                    workedOnList.append(tile)

                else:

                    if not tile in frontList:
                        newFrontTiles.append(tile)

            frontList += newFrontTiles

            if len(workedOnList) > 1:
                connectTile = rnd.choice(workedOnList)

            else:
                connectTile = workedOnList[0]

            self.__connectTiles(nextTile, connectTile)

        self.__makeEntryandExit()
        self.__mazeIsDone = True
        return True

    def makeMazeGrowTree(self, weightHigh=99, weightLow=97):
        if self.__mazeIsDone:
            raise self.__MazeError("Maze is already done", 3)

        for indexY in range(0,
                            self.sizeY):
            templist = []

            for indexX in range(0, self.sizeX):
                newTile = self.__MazeTile(indexX, indexY, isWall=False)
                templist.append(newTile)

            self.mazeList.append(templist)

        startingtile = rnd.choice(rnd.choice(self.mazeList))
        startingtile.workedOn = True

        choiceList = [startingtile]

        while len(choiceList) > 0:

            choice_ = rnd.random() * 100

            if choice_ <= weightLow:
                nextTile = choiceList[-1]
            elif weightLow < choice_ < weightHigh:
                nextTile = rnd.choice(choiceList)
            else:
                nextTile = choiceList[0]

            neiList = []

            for tile in self.__getNextTiles(nextTile.coordinateX, nextTile.coordinateY):

                if not tile.workedOn:
                    neiList.append(tile)

            if len(neiList) == 0:
                choiceList.remove(nextTile)

            else:
                connectTile = rnd.choice(neiList)
                connectTile.workedOn = True
                choiceList.append(connectTile)
                self.__connectTiles(nextTile, connectTile)

        self.__makeEntryandExit()
        self.__mazeIsDone = True
        return True

    def makeMazeBraided(self, weightBraid=-1):
        if not self.__mazeIsDone:
            raise self.__MazeError("Maze needs to be formed first", 4)

        if not isinstance(weightBraid, int) or weightBraid < -1 or weightBraid > 100:
            raise self.__MazeError("weightBraid has to be >= -1", 1)

        elif weightBraid == -1:
            for row in self.mazeList:
                for tile in row:

                    if len(tile.connectTo) == 1:

                        directionList = ["N", "S", "W", "E"]
                        directionList.remove(tile.connectTo[0])

                        rnd.shuffle(directionList)
                        for direction in directionList:

                            try:
                                self.__connectTilesWithString(tile, direction)
                                break

                            except self.__MazeError as mazeExcept:
                                if mazeExcept.errorcode == 2:
                                    pass

                                else:
                                    raise
        else:
            for row in self.mazeList:
                for tile in row:

                    if weightBraid >= (rnd.random() * 100):

                        directionList = ["N", "S", "W", "E"]
                        for connection in tile.connectTo:
                            directionList.remove(connection)

                        rnd.shuffle(directionList)
                        for direction in directionList:

                            try:
                                self.__connectTilesWithString(tile, direction)
                                break

                            except self.__MazeError as mazeExcept:
                                if mazeExcept.errorcode == 2:
                                    pass

                                else:
                                    raise

        return True

    def makePP(self, mode="1", colorWall=0, colorFloor=1, pixelSizeOfTile=1, ):
        if not self.__mazeIsDone:
            raise self.__MazeError("There is no Maze yet", 4)

        if mode == "1":
            if colorWall in (1, 0) and colorFloor in (1, 0):
                pass
            else:
                raise self.__MazeError(
                    "In mode \'1\' the color vaules have to be 0 for black or 1 for white", 1)

        elif mode == "RGB":

            try:
                if isinstance(colorWall, str):
                    colorWall = ImageColor.getrgb(colorWall)

                elif isinstance(colorWall, tuple) and len(colorWall) == 3:
                    for i in colorWall:
                        if not isinstance(i, int) or (i < 0 or i > 255):
                            raise self.__MazeError(
                                "RGB mode excepts only 8-bit integers", 1)

                else:
                    raise self.__MazeError(
                        "RGB Mode only excepts color strings or 3x8bit tulpels", 1)

                if isinstance(colorFloor, str):
                    colorFloor = ImageColor.getrgb(colorFloor)

                elif isinstance(colorFloor, tuple) and len(colorFloor) == 3:
                    for i in colorFloor:
                        if not isinstance(i, int) or (i < 0 or i > 255):
                            raise self.__MazeError(
                                "RGB mode excepts only 8-bit integers", 1)

                else:
                    raise self.__MazeError(
                        "RGB Mode only excepts color strings or 3x8bit tulpels", 1)

            except ValueError:
                raise self.__MazeError(
                    "RGB mode excepts 140 common html color strings. This was not one of them", 1)

        else:
            raise self.__MazeError(
                "The mode was not recognized. Only \'1\' or \'RGB\' are allowed", 1)

        if not isinstance(pixelSizeOfTile, int) or pixelSizeOfTile <= 0:
            raise self.__MazeError("the size of the tiles has to be an integer > 0",
                                   1)

        size = (pixelSizeOfTile * (self.sizeX * 2 + 1),
                pixelSizeOfTile * (self.sizeY * 2 + 1))

        image = Image.new(mode, size, colorWall)
        drawImage = ImageDraw.Draw(image)

        for row in self.mazeList:

            for tile in row:

                x = ((tile.coordinateX + 1) * 2 - 1) * pixelSizeOfTile
                y = ((tile.coordinateY + 1) * 2 - 1) * pixelSizeOfTile
                drawImage.rectangle(
                    [x, y, x + pixelSizeOfTile - 1, y + pixelSizeOfTile - 1], fill=colorFloor)

                if "N" in tile.connectTo:
                    drawImage.rectangle(
                        [x, y - pixelSizeOfTile, x + pixelSizeOfTile - 1, y - 1], fill=colorFloor)

                if "S" in tile.connectTo:
                    drawImage.rectangle(
                        [x, y + pixelSizeOfTile, x + pixelSizeOfTile - 1,
                            y + pixelSizeOfTile + pixelSizeOfTile - 1],
                        fill=colorFloor)

                if "W" in tile.connectTo:
                    drawImage.rectangle(
                        [x - pixelSizeOfTile, y, x - 1, y + pixelSizeOfTile - 1], fill=colorFloor)

                if "E" in tile.connectTo:
                    drawImage.rectangle(
                        [x + pixelSizeOfTile, y, x + pixelSizeOfTile +
                            pixelSizeOfTile - 1, y + pixelSizeOfTile - 1],
                        fill=colorFloor)

        return image

    def saveImage(self, image, name=None, format=None, pixelSizeOfTile=1):
        if name == None:

            tempName = re.sub(r'[^a-zA-Z0-9_]', '', self.name)
            if len(tempName) > 120:
                tempName = tempName[0:120]
            size = (pixelSizeOfTile * (self.sizeX * 2 + 1),
                    pixelSizeOfTile * (self.sizeY * 2 + 1))
            name = "mazes/" + tempName + "-" + \
                str(size[0]) + "_" + str(size[1]) + ".png"

        image.save(name, format)

        return name
