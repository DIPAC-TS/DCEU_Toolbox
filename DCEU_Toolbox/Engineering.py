import ezdxf

from honeybee.face import Face
from honeybee.aperture import Aperture
from honeybee.shade import Shade
from honeybee.room import Room
from honeybee.model import Model
from honeybee.boundarycondition import boundary_conditions, Surface, Outdoors, Ground

from ladybug_geometry.geometry2d.pointvector import Point2D, Vector2D
from ladybug_geometry.geometry2d.polygon import Polygon2D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.polyface import Polyface3D

class ThermalModel(object):
    @classmethod
    def __getAdjustVector(cls, DXFfile, layername):
        dxf = ezdxf.readfile(DXFfile)
        msp = dxf.modelspace()
        plines = msp.query("LWPOLYLINE[layer=='" + layername + "']")
        minX = plines[0][0][0]
        minY = plines[0][0][1]
        for pline in plines:
            vertices = []
            for pnt in pline:
                if pnt[0] < minX:
                    minX = pnt[0]
                if pnt[1] < minY:
                    minY = pnt[1]
        print("X_min: {}".format(minX))
        print("Y_min: {}".format(minY))
        return Vector2D(-minX, -minY)

    @classmethod
    def __get_faceZones_from_plines(cls, plines, prefix="TZ-", movingVector=Vector2D(0.0, 0.0)):
        polygons = {}
        faceZones = {}
        for pline in plines:
            vertices = []
            if len(pline) < 3:
                continue
            for pnt in pline:
                vertices.append(Point2D(pnt[0], pnt[1]))
            if Polygon2D._are_clockwise(vertices):
                vertices.reverse()
            polygons[pline.dxf.handle] = Polygon2D(vertices)
        if (movingVector != Vector2D(0.0, 0.0)):
            for zonename, polygon in polygons.items():
                faceZones[zonename] = polygon.move(movingVector)
            return faceZones
        return polygons
    
    @classmethod
    def __create_XYface(cls, polygon, z_level = 0.0, faceName="name"):
        pts3D = []
        for xypnt in polygon.vertices:
            pts3D.append(Point3D(xypnt.x, xypnt.y, z_level))
        return Face(faceName, Face3D(pts3D))
    
    @classmethod
    def __extrude_wall(cls, point1, point2, z_level = 0.0, height = 3.0, wallName = "wallName"):
        pts3D = []
        pts3D.append(Point3D(point1.x, point1.y, z_level))
        pts3D.append(Point3D(point2.x, point2.y, z_level))
        pts3D.append(Point3D(point2.x, point2.y, z_level + height))
        pts3D.append(Point3D(point1.x, point1.y, z_level + height))
        return Face(wallName, Face3D(pts3D))
    
    @classmethod
    def __extrudeRoom(cls, polygon, z_level = 0.0, height = 3.0, roomName="room"):
        faces = []
        faces.append(cls.__create_XYface(polygon.reverse(), z_level = z_level, faceName = (roomName + "_floor")))
        for i in range(len(polygon.vertices) - 1):
            faces.append(cls.__extrude_wall(polygon.vertices[i], polygon.vertices[i + 1], z_level = z_level, height = height, wallName=(roomName + "_wall" + str(i))))
            if i == len(polygon.vertices) - 2:
                faces.append(cls.__extrude_wall(polygon.vertices[i + 1], polygon.vertices[0], z_level = z_level, height = height, wallName=(roomName + "_wall" + str(i + 1))))
        faces.append(cls.__create_XYface(polygon, z_level = z_level + height, faceName = (roomName + "_roof")))
        return Room(roomName, faces, 0.001, 0.1)
    
    @classmethod
    def __create_rooms_from_DXF(cls, DXFfile, z_level = 0.0, height = 3.0, roomPrefix = "room", movingVector = Vector2D(0.0, 0.0), layername = "M-ENER-ZONE-N"):
        dxf = ezdxf.readfile(DXFfile)
        msp = dxf.modelspace()
        plines = msp.query("LWPOLYLINE[layer=='" + layername + "']")
        print("Number of zones identified: {}".format(len(plines)))
        geomFaces = cls.__get_faceZones_from_plines(plines, movingVector = movingVector)
        rooms = []
        for zonename, polygon in geomFaces.items():
            rooms.append(cls.__extrudeRoom(polygon, z_level = z_level, height = height, roomName = roomPrefix + zonename))
            print(roomPrefix + zonename + " created")
        return rooms
    
    @classmethod
    def create_model_from_DXFs(cls, dxfdict, z_level = 0.0, IDFname = "in.idf", adjustOrigin = True, layername="M-ENER-ZONE-N"):
        initial_level = z_level
        rooms = []
        movingVector = Vector2D(0.0, 0.0)
        for filename, height in dxfdict.items():
            if z_level == initial_level and adjustOrigin:
                movingVector = cls.__getAdjustVector(filename + ".dxf", layername=layername)
            rooms.extend(cls.__create_rooms_from_DXF(filename + ".dxf",
                                               z_level = z_level,
                                               height = height,
                                               roomPrefix = filename,
                                               movingVector = movingVector,
                                               layername = layername))
            z_level += height
        #Room.solve_adjacency(rooms)
        model = Model('Mymodel', rooms, tolerance = 0)
        idf_str = model.to.idf(model)
        with open(IDFname, "w") as file:
            file.write(idf_str)
    
    @classmethod
    def delete_default_constructions(cls, osmpath):
        with open(osmpath, "r") as file:
            lista = file.readlines()
        bandera = False
        for i in range(len(lista)):
            if (lista[i].startswith("OS:Surface")):
                bandera = True
            if ("Construction Name" in lista[i] and bandera):
                lista[i] = "  ," + lista[i].split(",")[1]
                bandera = False
        with open(osmpath, "w") as file:
            for linea in lista:
                file.write(linea)

def getMCA(load, v=200., ph=1):
  import math
  if ph == 1:
    return load / v * 1.25
  else:
    return load / v / math.sqrt(3.) * 1.25
 
def getMOB(load, v=200., ph=1):
  import math
  if ph == 1:
    return load / v * 1.4
  else:
    return load / v / math.sqrt(3.) * 1.4
  
def airflow_parking(cars:int,
                    area:float,
                    CO_emission:float = 700.0,
                    time_of_op:float = 120., 
                    CO_acceptable:int = 35) -> float:
    """
    arguments:
    ----------
    cars - number of cars $N$ in operation during peak hour use
    area - total floor area of parking facility $A_f$, m^2
    CO_emission - average CO emission rate $E$ for a typical car, g/h
    time_of_op - average length of operation and travel time $\theta$ for a typical car, s
    CO_acceptable - acceptable CO concenctration CO_max in the garage, ppm
    
    returns:
    --------
    required ventilation rate of parking, L/s
    """
    G_0 = 26.7 # g/(h-m^2)
    C = {15:1.204E-3, 25:0.692E-3, 35:0.481E-3} #(L/s)/(m^2/s))
    G = cars * CO_emission / area #g/(h-m^2)
    f = 100. * G / G_0    
    return C[CO_acceptable] * f * time_of_op * area