import tkinter as tk
import os

import ML_manager

# CONSTANTS:
UNFILLEDCELL = "unfilled cell"
FILLEDCELL = "filled cell"


class MainWindow(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.master = master

        self.model = ML_manager.Model()

        self.topFrame = tk.Frame(self)
        self.MainCanvas = DrawCanvas(self, 28, 28, 10, 1)
        self.clearButton = tk.Button(self.topFrame, text="Clear",
                                     command=self.MainCanvas.clear)
        self.helpButton = tk.Button(self.topFrame, text="Help",
                                    command=self.openHelp)
        self.bottomFrame = tk.Frame(self)
        self.AnalyzeButton = tk.Button(self.bottomFrame, text="Guess!",
                                       command=self.getNumber)
        self.NumberLabel = tk.Label(self.bottomFrame)
        self.packMe()

    def packMe(self):
        self.master.title("Number Draw")
        self.master.resizable(False, False)
        self.pack(fill="both")
        self.topFrame.pack(fill="x")
        self.clearButton.pack(side="left")
        self.helpButton.pack(side="left")
        self.MainCanvas.pack(fill="both")
        self.bottomFrame.pack(fill="both")
        self.AnalyzeButton.pack(side="left")
        self.NumberLabel.pack(side="left")

    def openHelp(self):
        os.startfile("README.md")

    def _getArray(self):
        Array = []
        for n, i in enumerate(self.MainCanvas.grid):
            Array.append([])
            for j in i:
                if j.state == UNFILLEDCELL:
                    Array[n].append(0)
                elif j.state == FILLEDCELL:
                    Array[n].append(1)
        return Array

    def getNumber(self):
        Array = self._getArray()
        for a in Array:
            print(a)
        num = self.model.check(Array)
        self.NumberLabel.configure(text=f"{str(num[0])}   {str(num[1])}% sure")


class Cell():
    def __init__(self, master, x, y, size):
        self.master = master
        self.xlocation = x
        self.ylocation = y
        self.size = size
        self.state = UNFILLEDCELL

    def SetState(self, state):
        self.state = state

    def draw(self):
        if self.master is not None:
            fill = "white"
            outline = "black"
            if self.state == UNFILLEDCELL:
                pass
            elif self.state == FILLEDCELL:
                fill = "gray20"
                outline = "gray20"
            xmin = self.xlocation * self.size
            xmax = xmin + self.size
            ymin = self.ylocation * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(
                xmin, ymin, xmax, ymax, fill=fill, outline=outline)


class DrawCanvas(tk.Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, size, *args, **kwargs):
        tk.Canvas.__init__(self, master, width=cellSize * columnNumber,
                           height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize
        self.size = size

        self.grid = []
        for row in range(rowNumber):
            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        # memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        self.bind("<Button-3>", self.handleMouseClick)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion1)
        self.bind("<B3-Motion>", self.handleMouseMotion2)
        # bind release button action - clear the memory of modified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        self.bind("<ButtonRelease-3>", lambda event: self.switched.clear())

        self.canDraw = True
        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        if row < 0:
            row = 0
        if column < 0:
            column = 0
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        if cell.state == UNFILLEDCELL and event.num == 1 and self.canDraw:
            cell.SetState(FILLEDCELL)
        elif cell.state == FILLEDCELL and event.num == 3 and self.canDraw:
            cell.SetState(UNFILLEDCELL)
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion1(self, event):
        row, column = self._eventCoords(event)
        if self.size != 0:
            for i in range(-1*self.size, self.size):
                for j in range(-1*self.size, self.size):
                    cell = self.grid[row+i][column+j]

                    if cell not in self.switched and self.canDraw:
                        if cell.state == UNFILLEDCELL:
                            cell.SetState(FILLEDCELL)
                        cell.draw()
                        self.switched.append(cell)
        else:
            cell = self.grid[row][column]
            if cell not in self.switched and self.canDraw:
                if cell.state == UNFILLEDCELL:
                    cell.SetState(FILLEDCELL)
                cell.draw()
                self.switched.append(cell)

    def handleMouseMotion2(self, event):
        row, column = self._eventCoords(event)
        if self.size != 0:
            for i in range(self.size*-1, self.size):
                for j in range(self.size*-1, self.size):
                    cell = self.grid[row+j][column+i]

                    if cell not in self.switched and self.canDraw:
                        if cell.state == FILLEDCELL:
                            cell.SetState(UNFILLEDCELL)
                        cell.draw()
                        self.switched.append(cell)
        else:
            cell = self.grid[row][column]
            if cell not in self.switched and self.canDraw:
                if cell.state == FILLEDCELL:
                    cell.SetState(UNFILLEDCELL)
                cell.draw()
                self.switched.append(cell)

    def clear(self):
        self.delete("all")
        for i in self.grid:
            for j in i:
                j.SetState(UNFILLEDCELL)
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    win = MainWindow(root)
    root.mainloop()
