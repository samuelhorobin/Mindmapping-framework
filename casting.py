import pygame
import settings
import shapely
import math


class AmbiguityError(Exception):
    ''' Raised when two conflicting values are entered '''

    def __init__(self, *args: object) -> None:
        self.message = f"{args} are conflicting values"
        super().__init__(self.message)


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
    return inProximity, range


def draw_hitbox(rect):
    for side in [(rect.topleft, rect.topright),
                 (rect.topright, rect.bottomright),
                 (rect.bottomright, rect.bottomleft),
                 (rect.bottomleft, rect.topleft)]:
        pygame.draw.line(settings.SCREEN, (255, 0, 0), side[0], side[1], 3)


def cast(source, allRectangles, radius):

    proximityRects, rangePygameRect = proximity_check(
        source, allRectangles, radius)

    shapelyRangeRect = shapely.Polygon((rangePygameRect.topleft, rangePygameRect.topright, rangePygameRect.bottomright, rangePygameRect.bottomleft))

    rectangles = [shapely.Polygon((rect.topleft, rect.topright, rect.bottomright, rect.bottomleft))
                  for rect in proximityRects]  # Relevant rectangles
    innerRectangles = [resize_polygon(rectangle, 0.999)
                       for rectangle in rectangles]

    points = []

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

                if rangePygameRect.collidepoint(point):
                    points.append(point)
                    extentedRay = scale_line(
                        ray.coords[0], ray.coords[1], -500)

                    for rectangle in rectangles:
                        try:
                            intersection = shapely.LineString(
                                extentedRay).intersection(rectangle).coords[0]
                            if rangePygameRect.collidepoint(intersection):
                                points.append(intersection)
                        except:  # No intersection
                            lines = []
                            for i in range(len(shapelyRangeRect.exterior.coords) - 1):
                                line = shapely.LineString(
                                    [shapelyRangeRect.exterior.coords[i], shapelyRangeRect.exterior.coords[i + 1]])
                                lines.append(line)
                            for line in lines:
                                if shapely.LineString(extentedRay).intersects(shapely.LineString(line)):
                                    intersection = shapely.LineString(extentedRay).intersection(
                                        shapely.LineString(line)).coords[0]

                                    intersect = False
                                    for rectangle in rectangles:
                                        if shapely.LineString(extentedRay).intersects(rectangle):
                                            intersect = True
                                    if intersect == False:
                                        points.append(intersection)
                                # pass

                    pygame.draw.line(settings.SCREEN, (255, 255, 255),
                                     extentedRay[0], extentedRay[1])
        for point in shapelyRangeRect.exterior.coords:
            if not shapely.LineString([(source), (point)]).intersects(rectangle):
                points.append(point)

    for point in points:
        pygame.draw.rect(settings.SCREEN, (255, 255, 255),
                         ((point[0]-5, point[1]-5), (10, 10)))


    scope = shapely.Polygon(points)



def scale_line(anchor, extendedPoint, newLength):
    deltaX = anchor[0] - extendedPoint[0]
    deltaY = anchor[1] - extendedPoint[1]
    length = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
    multiplier = newLength / length
    newDeltaX, newDeltaY = deltaX * multiplier, deltaY * multiplier
    newExtended = ((anchor[0] + newDeltaX), (anchor[1] + newDeltaY))
    return (anchor, newExtended)
