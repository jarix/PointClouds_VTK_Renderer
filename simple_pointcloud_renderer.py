# -*- coding: utf-8 -*-
"""
    VTK Rendering of Point CLouds 

    Instantiates a basic VTK Rendering pipeline for point clouds
        Source/Reader -> Filter -> Mapper -> Actor
        -> Rendered -> RenderWindow -> Interactor

    Author: Jari Honkanen

"""

import vtk
import numpy as np
import math
import sys

class PointCloud:
    """ PointCloud class holding pointcloud data, mapper, and actor
    """
    def __init__(self, minRange=1.0, maxRange=300, maxNumPoints = 800000):
        """ Initializer
        """
        print("in PointCloud __init__")
        self.minRange = minRange
        self.maxRange = maxRange
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCellArray = vtk.vtkCellArray()
        self.vtkDepthArray = vtk.vtkDoubleArray()
        self.vtkDepthArray.SetName("PointCloud")
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCellArray)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepthArray)
        self.vtkPolyData.GetPointData().SetActiveScalars("PointCloud")

        # MAPPER:
        self.vtkMapper = vtk.vtkPolyDataMapper()
        self.vtkMapper.SetInputData(self.vtkPolyData)
        self.vtkMapper.SetScalarRange(self.minRange, self.maxRange)
        self.vtkMapper.SetScalarVisibility(True)
        self.vtkMapper.SetColorModeToDefault()
        
        # ACTOR:
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.vtkMapper)

        print("out PointCloud __init__")


    def insertPoint(self, point):
        """ Insert one x,y,z point into point cloud
        """
        pointId = self.vtkPoints.InsertNextPoint(point[:])
        self.vtkDepthArray.InsertNextValue(point[2])
        self.vtkCellArray.InsertNextCell(1)
        self.vtkCellArray.InsertCellPoint(pointId)


    def makeEllipseCloud(self):
        """ Create an ellipse shape point cloud for testing
        """
        for Z in np.arange(-1.0, 1.0, 0.05):
    
            for angle in np.arange(0.0, 2*math.pi, 0.05):
        
                x = 0.5 * math.cos(angle)
                y = math.sin(angle)
                z = Z
                point = [x, y, z]

                self.insertPoint(point)


    def readXYZData( self, fileName):
        """ Read point cloud file in X Y Z format, values sepated by space. 
            Lines in the beginning starting with # skipped
        """
        print("Reading file: ", fileName)
        rawData = np.genfromtxt( fileName, dtype=float, comments='#', skip_header=0, usecols=[0,1,2])
        print("Read ", len(rawData), " points")

        for k in range(np.size(rawData,0)):
            point = rawData[k]
            self.insertPoint(point)

    def readPCDXYZData( self, fileName):
        """ Read PCD point cloud file in with XYZ points 
            11 Lines of header in the beginning of the file is skipped
        """
        print("Reading file: ", fileName)
        rawData = np.genfromtxt( fileName, dtype=float, skip_header=11, usecols=[0,1,2])
        print("Read ", len(rawData), " points")

        for k in range(np.size(rawData,0)):
            point = rawData[k]
            #print("k = ",k," point = ",point)
            self.insertPoint(point)


def keypressCallback(obj, ev):
    """ Keypress event handler
    """
    key = obj.GetKeySym()
    print(key, " pressed!")


if __name__ == "__main__":
    name = "Simple VTK PointCloud Renderer Example"
    print(name)
    print(vtk.vtkVersion.GetVTKSourceVersion())

    if (len(sys.argv) < 2):
        print("Usage: simple_pointcloud_renderer <fileName>")
        sys.exit

    # Instantiate Point Cloud Class with Mapper and Actor, and Read in Data
    my_pointCloud = PointCloud()
    my_pointCloud.readPCDXYZData(sys.argv[1])
    #my_pointCloud.readXYZData(sys.argv[1])
    #my_pointCloud.makeEllipseCloud()

    # Create rest of VTK Pipeline: renderer -> renderWindow -> interactor
    
    # RENDERER:
    # Create a renderer for actor
    my_renderer = vtk.vtkRenderer()
    #my_renderer.SetBackground(1.0, 1.0, 1.0)
    my_renderer.SetBackground(0, 0, 0)
    my_renderer.AddActor(my_pointCloud.vtkActor)

    # RENDERWINDOW:
    # Create Render Window
    my_render_window = vtk.vtkRenderWindow()
    my_render_window.SetWindowName(name)
    my_render_window.SetSize(600, 600)
    my_render_window.AddRenderer(my_renderer)

    # INTERACTOR
    # Create interactor
    my_interactor = vtk.vtkRenderWindowInteractor()
    my_interactor.AddObserver('KeyPressEvent', keypressCallback, 1.0)
    my_interactor.SetRenderWindow(my_render_window)

    # Print the list of rehistered observers
    #print(my_interactor)

    # Rendering Loop
    my_interactor.Initialize()
    my_render_window.Render()
    my_interactor.Start()

    msg = "Adios"
    print(msg)

