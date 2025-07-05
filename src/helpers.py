import pygame, math, random

def pointInPolygon(x,y,polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def rotatePoint(point, angleX, angleY, angleZ):
    x, y, z = point
    # Rotate around X-axis
    y, z = (y * math.cos(angleX) - z * math.sin(angleX), 
            y * math.sin(angleX) + z * math.cos(angleX))
    # Rotate around Y-axis
    x, z = (x * math.cos(angleY) + z * math.sin(angleY), 
            -x * math.sin(angleY) + z * math.cos(angleY))
    # Rotate around Z-axis
    x, y = (x * math.cos(angleZ) - y * math.sin(angleZ), 
            x * math.sin(angleZ) + y * math.cos(angleZ))
    return [x, y, z]

def project3dTo2d(x, y, z, distance):
    factor = distance / (distance + z)
    projX = int(x * factor * 15)
    projY = int(y * factor * 15)
    return projX, projY

def getNormalVector(face, vertices):
    if len(face) < 3:
        return [0, 0, 1]
    p0, p1, p2 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
    v1 = [p1[i] - p0[i] for i in range(3)]
    v2 = [p2[i] - p0[i] for i in range(3)]
    normal = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]
    length = math.sqrt(sum(n**2 for n in normal))
    return [n / length if length > 0 else 0 for n in normal]