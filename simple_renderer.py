# -*- coding: utf-8 -*-
"""
    Simple VTK Rendering sample of a Cone

    Instantiates a basic VTK Rendering pipeline:
        Source/Reader -> Filter -> Mapper -> Actor
        -> Rendered -> RenderWindow -> Interactor

    Author: Jari Honkanen

"""

import vtk

if __name__ == "__main__":
    name = "Simple VTK Renderer Pipeline Example"
    print(name)
    print(vtk.vtkVersion.GetVTKSourceVersion())

    # Create VTK Pipeline
    # VTK flow: Source/reader -> filter -> mapper -> actor
    #            -> renderer -> renderWindow -> interactor

    # SOURCE:
    # Generate polygon data for a cube
    #my_obj = vtk.vtkCubeSource()
    #my_obj = vtk.vtkSphereSource()
    my_obj = vtk.vtkConeSource()

    # MAPPER:
    # Create a mapper for the cube data
    my_mapper = vtk.vtkPolyDataMapper()
    my_mapper.SetInputConnection(my_obj.GetOutputPort())

    # ACTOR:
    # Connect Mapper to Actor
    my_actor = vtk.vtkActor()
    my_actor.SetMapper(my_mapper)
    my_actor.GetProperty().SetColor(1.0, 0.0, 1.0)

    # RENDERER:
    # Create a renderer for actor
    my_renderer = vtk.vtkRenderer()
    my_renderer.SetBackground(1.0, 1.0, 1.0)
    my_renderer.AddActor(my_actor)

    # RENDERWINDOW:
    # Create Render Window
    my_render_window = vtk.vtkRenderWindow()
    my_render_window.SetWindowName(name)
    my_render_window.SetSize(600, 600)
    my_render_window.AddRenderer(my_renderer)

    # INTERACTOR
    # Create interactor
    my_interactor = vtk.vtkRenderWindowInteractor()
    my_interactor.SetRenderWindow(my_render_window)

    # Rendering Loop
    my_interactor.Initialize()
    my_render_window.Render()
    my_interactor.Start()

    msg = "Adios"
    print(msg)

