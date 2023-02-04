import pygame
import settings
import shapely


def resize_polygon(polygon, factor):
    centroid = polygon.centroid

    resizedCoords = []
    for coord in polygon.exterior.coords:
        displacement = (coord[0] - centroid.x, coord[1] - centroid.y)
        displacement = (displacement[0] * factor, displacement[1] * factor)
        newCoord = (centroid.x + displacement[0], centroid.y + displacement[1])
        resizedCoords.append(newCoord)
    resizedPolygon = shapely.Polygon(resizedCoords)

    return resizedPolygon


def proximity_check(sourceCoordinate, rectangles, radius):
    range = pygame.Rect(
        (sourceCoordinate[0] - (radius/2), (sourceCoordinate[1] - (radius/2))), (radius, radius))
    draw_hitbox(range)
    inProximity = []
    for rectangle in rectangles:
        if pygame.Rect.colliderect(range, rectangle):
            inProximity.append(rectangle)
    return inProximity


def draw_hitbox(rect):
    for side in [(rect.topleft, rect.topright),
                 (rect.topright, rect.bottomright),
                 (rect.bottomright, rect.bottomleft),
                 (rect.bottomleft, rect.topleft)]:
        pygame.draw.line(settings.SCREEN, (255, 0, 0), side[0], side[1], 3)


def cast(source, allRectangles, radius):
    rectangles = [shapely.Polygon((rect.topleft, rect.topright, rect.bottomright, rect.bottomleft))
                  for rect in proximity_check(source, allRectangles, radius)]  # Relevant rectangles
    innerRectangles = [resize_polygon(rectangle, 0.999) for rectangle in rectangles]

    for rectangle in rectangles:
        for point in list(dict.fromkeys(rectangle.exterior.coords)):
            ray = shapely.LineString([(source), (point)])
            intersects = False
            for innerRectangle in innerRectangles:
                if ray.intersects(innerRectangle):
                    intersects = True
            if intersects == False:
                pygame.draw.line(settings.SCREEN, (255, 255, 255),
                                 ray.coords[0], ray.coords[1])
