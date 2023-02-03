import pygame


def proximity_check(sourceCoordinate, rectangles, radius):
    range = pygame.Rect((sourceCoordinate[0] - (radius/2), (sourceCoordinate[1] - (radius/2))), (radius, radius))
    inProximity = []
    for rectangle in rectangles:
        if pygame.Rect.colliderect(range, rectangle):
            inProximity.append(rectangle)
    return inProximity


class Line:
    def __init__(self, coords1, coords2):
        self.coords1 = coords1
        self.coords2 = coords2
        
    def line_intersection(self, line2):
        x1, y1 = self.coords1
        x2, y2 = self.coords2
        x3, y3 = line2.coords1
        x4, y4 = line2.coords2

        den = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
        if den == 0:
            return None

        ua = (((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))) / den
        ub = (((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))) / den
        print(f"ua: {ua}, ub: {ub}")

        if (ua >= 0 and ua <= 1) and (ub >= 0 and ub <= 1):
            x = x1 + (ua * (x2 - x1))
            y = y1 + (ua * (y2 - y1))
            if (x,y) == self.coords1 or (x,y) == self.coords2:
                return None
            return (x, y)

        else:
            return None