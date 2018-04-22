#!/usr/bin/env python3
"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""

import sys
from geo.segment import load_segments
from geo.tycat import tycat
from geo.point import Point

precision = 0.5*10**(-6)

class Cell_eq:
    """
    cell of the event_queue
    """
    def __init__(self, value, point_list, cel):
        # value is a real number representing the abscisse
        self.value = value
        # point list is a pointer on the first element of an ordered list of point
        self.point_list = point_list
        # the next cellule
        self.next = cel

class Cell_point:
    """
    cell of list of point
    """
    def __init__(self, ordinate, nature, segment1, segment2, next_point, precedent_point):
        # point ordinate (y)
        self.ordinate = ordinate
        # nature equal -1, 0, 1 : -1 segment beginning, 0 intersection, 1 segment end
        self.nature = nature
        # segment containing the point, two segments if intersection
        self.segment1 = segment1
        self.segment2 = segment2
        self.next = next_point
        self.precedent = precedent_point

class Event_Queue:
    """
    liste chainée de point
    """
    def __init__(self, tete, queue):
        self.tete = tete
        self.queue = queue

    def insert(self, point, nature, segment1, segment2):
        cel = self.tete
        #case where we insert a new tete for the list or when we change the tete
        if cel is None:
            self.tete = Cell_eq(point.coordinates[0], None, None)
            self.queue = self.tete
            self.tete.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, None, None)
        elif point.coordinates[0] == cel.value:
            pivot = cel.point_list
            #no reason to append because the cel is not None
            if pivot is None:
                cel.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, None, None)
            elif point.coordinates[1] < pivot.ordinate:
                cel.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot, None)
                pivot.precedent = cel.point_list
            elif point.coordinates[1] == pivot.ordinate:
                if pivot.nature == 1:
                    pivot.next = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot.next, pivot)
                else:
                    cel.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot, None)
                    pivot.precedent = cel.point_list
            else:
                while (pivot.next is not None) and (point.coordinates[1] > pivot.next.ordinate):
                    pivot = pivot.next
                new = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot.next, pivot)
                pivot.next = new
                if new.next is not None:
                    new.next.precedent = new
        elif point.coordinates[0] < cel.value:
            new = Cell_eq(point.coordinates[0], None, self.tete)
            self.tete = new
            self.tete.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, None, None)
        #case where we insert an other cel or change one after the tete of the list
        else:
            while (cel.next is not None) and (point.coordinates[0] > cel.next.value):
                cel = cel.next
            if cel.next is None:
                self.queue = Cell_eq(point.coordinates[0], None, None)
                self.queue.point_list= Cell_point(point.coordinates[1], nature, segment1, segment2, None, None)
                cel.next = self.queue
            elif point.coordinates[0] == cel.next.value:
                pivot = cel.next.point_list
                if pivot is None:
                    cel.next.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, None, None)
                elif point.coordinates[1] < pivot.ordinate:
                    cel.next.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot, None)
                    pivot.precedent = cel.next.point_list
                elif point.coordinates[1] == pivot.ordinate:
                    if pivot.nature == 1:
                        pivot.next = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot.next, pivot)
                    else:
                        cel.next.point_list = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot, pivot.precedent)
                        pivot.precedent = cel.next.point_list
                else:
                    while (pivot.next is not None) and (point.coordinates[1] > pivot.next.ordinate):
                        pivot = pivot.next
                    new = Cell_point(point.coordinates[1], nature, segment1, segment2, pivot.next, pivot)
                    pivot.next = new
                    if new.next is not None:
                        new.next.precedent = new
            else:
                new_eq = Cell_eq(point.coordinates[0], Cell_point(point.coordinates[1], nature, segment1, segment2, None, None), cel.next)
                cel.next = new_eq
                if new_eq.next is None:
                    self.queue = new_eq

    def possess(self, intersec):
        """
        return true if the intersec is in the list
        """
        cel = self.tete
        while cel is not None:
            if cel.value < (intersec.coordinates[0] + precision) and cel.value > (intersec.coordinates[0] - precision) :
                pivot = cel.point_list
                while pivot is not None:
                    if pivot.ordinate < (intersec.coordinates[1] + precision) and pivot.ordinate > (intersec.coordinates[1] - precision):
                        return True
                    pivot = pivot.next
            cel = cel.next
        return False

    def add_segment(self, segment):
        """
        add the two points of a segment in the event list
        """
        if segment.endpoints[0].coordinates[0] < (segment.endpoints[1].coordinates[0] - precision):
            self.insert(segment.endpoints[0], -1, segment, None)
            self.insert(segment.endpoints[1], 1, segment, None)
        elif segment.endpoints[0].coordinates[0] > (segment.endpoints[1].coordinates[0] + precision):
            self.insert(segment.endpoints[1], -1, segment, None)
            self.insert(segment.endpoints[0], 1, segment, None)
        else:
            if segment.endpoints[0].coordinates[1] < (segment.endpoints[1].coordinates[1] - precision):
                self.insert(segment.endpoints[0], -1, segment, None)
                self.insert(segment.endpoints[1], 1, segment, None)
            else:
                self.insert(segment.endpoints[1], -1, segment, None)
                self.insert(segment.endpoints[0], 1, segment, None)

    def parcourir(self):
        """
        function to verify the content of event_queue_list
        """
        cel = self.tete
        while cel is not None:
            print('cellule d abscisse "{}"'.format(cel.value))
            pivot = cel.point_list
            while pivot is not None:
                print("ordonnée {}, nature {}, {}".format(pivot.ordinate, pivot.nature, pivot.segment1))
                pivot = pivot.next
            print("point_list over")
            cel = cel.next
        print("event_queue_list over")

class Sweep_Line:
    """
    list of segment
    """
    def __init__(self, tete, queue):
        self.tete = tete
        self.queue = queue

    def insert(self, segment, abscisse):
        """
        insert an element at the end of the sweep_line and return this element
        """
        if self.tete is None:
            self.tete = Cell_sl(segment, None, None)
            self.queue = self.tete
            return self.queue
        else:
            if self.tete.is_above(segment, abscisse) == True:
                self.tete.precedent = Cell_sl(segment, self.tete, None)
                self.tete = self.tete.precedent
                return self.tete
            else:
                cel = self.tete
                while cel.next is not None and cel.next.is_above(segment, abscisse) == False:
                    cel = cel.next
                if cel.next is None:
                    cel.next = Cell_sl(segment, None, cel)
                    self.queue = cel.next
                    return self.queue
                else:
                    cel.next.precedent = Cell_sl(segment, cel.next, cel)
                    cel.next = cel.next.precedent
                    return cel.next

    def parcourir(self):
        """
        function to verify the content of the sweep_line
        """
        print("sweep_line parcour")
        cel = self.tete
        while cel is not None:
            print(cel.segment)
            cel = cel.next
            print("next segment")

class Cell_sl:
    """
    cell of the sweep_line list
    """
    def __init__(self, segment, next_cel, precedent_cel):
        self.segment = segment
        self.precedent = precedent_cel
        self.next = next_cel

    def is_above(self, segment, abscisse):
        # if the segment already in the sweep_line is vertical it's automaticaly below the new segment
        if abs(self.segment.endpoints[0].coordinates[0] - self.segment.endpoints[1].coordinates[0]) < (0 + precision):
            return False
        else:
            #we find the value of the ordinate of the beginning of the segment
            if segment.endpoints[0].coordinates[0] < (segment.endpoints[1].coordinates[0] - precision):
                val = 0
            elif segment.endpoints[0].coordinates[0] > (segment.endpoints[1].coordinates[0] + precision):
                val = 1
            else:
                if segment.endpoints[0].coordinates[1] < segment.endpoints[1].coordinates[1]:
                    val = 0
                else:
                    val = 1
            if segment.endpoints[val] == self.segment.endpoints[0]:
                if val == 0:
                    val = 1
                else:
                    val = 0
                if segment.endpoints[val].coordinates[1] < self.segment.endpoints[1].coordinates[1]:
                    return True
                else:
                    return False
            elif segment.endpoints[val] == self.segment.endpoints[1]:
                if val == 0:
                    val = 1
                else:
                    val = 0
                if segment.endpoints[val].coordinates[1] < self.segment.endpoints[0].coordinates[1]:
                    return True
                else:
                    return False
            elif ((self.segment.endpoints[0].coordinates[1]
                - self.segment.endpoints[1].coordinates[1])/(self.segment.endpoints[0].coordinates[0]
                - self.segment.endpoints[1].coordinates[0])*(abscisse - self.segment.endpoints[0].coordinates[0])
                + self.segment.endpoints[0].coordinates[1]) == segment.endpoints[val].coordinates[1]:
                if (segment.endpoints[0].coordinates[0] - segment.endpoints[1].coordinates[0]) == 0:
                    return False
                elif ((self.segment.endpoints[0].coordinates[1]
                    - self.segment.endpoints[1].coordinates[1])/(self.segment.endpoints[0].coordinates[0]
                    - self.segment.endpoints[1].coordinates[0])) < ((segment.endpoints[0].coordinates[1]
                    - segment.endpoints[1].coordinates[1])/(segment.endpoints[0].coordinates[0] - segment.endpoints[1].coordinates[0])):
                    return False
                else:
                    return True
            elif ((self.segment.endpoints[0].coordinates[1]
                - self.segment.endpoints[1].coordinates[1])/(self.segment.endpoints[0].coordinates[0]
                - self.segment.endpoints[1].coordinates[0])*(abscisse - self.segment.endpoints[0].coordinates[0])
                + self.segment.endpoints[0].coordinates[1]) < segment.endpoints[val].coordinates[1]:
                return False
            else:
                return True

def parcourir_liste(liste):
    """
    function used to print the content of the intersection list
    """
    print("Here is the intersection list :")
    for i in range(0, len(liste)):
        print(liste[i])
        print("next intersection")
    print("end of the intersection list")

def test(filename):
    """
    run bentley ottmann
    """
    #debug = True --> debug version, debug = False --> no debug option version
    debug = False
    #print the event_queue_list before the suppression
    debug1 = False
    #print details when the event is an intersection
    debug2 = False
    #print the event_queue in the beginning
    debug3 = False
    #print the intersections
    debug4 = False
    #print details when the event is an ending segment point
    debug5 = False
    adjuster, segments = load_segments(filename)
    tycat(segments)
    event_queue_list = Event_Queue(None, None)
    intersections = []
    for seg in segments:
        event_queue_list.add_segment(seg)
        if debug3:
            print("{}".format(seg))
            print("")
            event_queue_list.parcourir()
            print("")
            print("")
    if debug3:
        event_queue_list.parcourir()
    event_queue = event_queue_list.tete
    sweep_line = Sweep_Line(None, None)
    current_event = event_queue.point_list
    iteration = 0
    while event_queue is not None:
        if debug:
            print("je suis passé par le début")
        while current_event is not None:
            #case where event is the beginnig of a segment
            if (current_event.nature == -1):
                if debug:
                    print("the algo take the way of a first segment point")
                seg = sweep_line.insert(current_event.segment1, event_queue.value)
                seg_above = seg.next
                seg_below = seg.precedent
                seg = seg.segment
                if seg_above != None:
                    seg_above = seg_above.segment
                    intersec = seg.intersection_with(seg_above)
                    if intersec is not None:
                        if intersec == seg_above.endpoints[0] or intersec == seg_above.endpoints[1] or intersec == seg.endpoints[0] or intersec == seg.endpoints[1]:
                            intersec = None
                    if intersec is not None:
                        event_queue_list.insert(intersec, 0, seg, seg_above)
                if seg_below != None:
                    seg_below = seg_below.segment
                    intersec = seg.intersection_with(seg_below)
                    if intersec is not None:
                        if intersec == seg_below.endpoints[0] or intersec == seg_below.endpoints[1] or intersec == seg.endpoints[0] or intersec == seg.endpoints[1]:
                            intersec = None
                    if intersec is not None:
                        event_queue_list.insert(intersec, 0, seg_below, seg)
            #case when event is the end of a segment
            elif (current_event.nature == 1):
                if debug:
                    print("the algo take the way of an ending segment point")
                seg = sweep_line.tete
                while seg.segment != current_event.segment1:
                    seg = seg.next
                seg_above = seg.next
                seg_below = seg.precedent
                if debug5:
                    print(seg_below == None)
                    print(seg_above == None)
                seg = seg.segment
                if seg_below is None and seg_above is None:
                    sweep_line.tete = None
                    sweep_line.queue = None
                elif seg_below is None:
                    seg_above.precedent = None
                    sweep_line.tete = seg_above
                elif seg_above is None:
                    seg_below.next = None
                    sweep_line.queue = seg_below
                else:
                    seg_below.next = seg_above
                    seg_above.precedent = seg_below
                    seg_below = seg_below.segment
                    seg_above = seg_above.segment
                    intersec = seg_below.intersection_with(seg_above)
                    if intersec is not None:
                        if intersec == seg_below.endpoints[0] or intersec == seg_below.endpoints[1] or intersec == seg_above.endpoints[0] or intersec == seg_above.endpoints[1]:
                            intersec = None
                    if intersec is not None:
                        if not event_queue_list.possess(intersec):
                            event_queue_list.insert(intersec, 0, seg_below, seg_above)
            #case when event is an intersection
            else:
                if debug:
                    print("the algo take the way of an intersection point")
                intersections.append(Point([event_queue.value, current_event.ordinate]))
                if debug2:
                    print(current_event.ordinate)
                    print(current_event.segment1)
                    print(current_event.segment2)
                seg_above = sweep_line.tete
                while seg_above.segment != current_event.segment2:
                    if debug2:
                        print(seg_above.segment)
                    seg_above = seg_above.next
                    if seg_above is None:
                        break
                seg_below = sweep_line.tete
                if debug2:
                    print(seg_below.segment)
                while seg_below.segment != current_event.segment1:
                    if debug2:
                        print(seg_below.segment)
                    seg_below = seg_below.next
                    if seg_below is None:
                        break
                if seg_below is None:
                    if debug2:
                        print("seg_below is None")
                elif seg_above is None:
                    if debug2:
                        print("seg_above is None")
                else:
                    if debug2:
                        print(seg_below.segment)
                        print(seg_above.segment)
                    seg_below.segment, seg_above.segment = seg_above.segment, seg_below.segment
                    seg_above2 = seg_above.next
                    seg_below2 = seg_below.precedent
                    if debug2:
                        print(seg_below.segment)
                        print(seg_above.segment)
                        if seg_below2 is not None:
                            print(seg_below2.segment)
                        else:
                            print("SEG_BELOW2 IS NONE")
                        if seg_above2 is not None:
                            print(seg_above2.segment)
                        else:
                            print("SEG_ABOVE2 IS NONE")
                    if seg_above2 is not None:
                        intersec =  seg_above.segment.intersection_with(seg_above2.segment)
                        if intersec is not None:
                            if intersec == seg_above.segment.endpoints[0] or intersec == seg_above.segment.endpoints[1] or intersec == seg_above2.segment.endpoints[0] or intersec == seg_above2.segment.endpoints[1]:
                                intersec = None
                        if intersec is not None:
                            if not event_queue_list.possess(intersec):
                                event_queue_list.insert(intersec, 0, seg_above.segment, seg_above2.segment)
                    if seg_below2 is not None:
                        intersec =  seg_below.segment.intersection_with(seg_below2.segment)
                        if intersec is not None:
                            if intersec == seg_below.segment.endpoints[0] or intersec == seg_below.segment.endpoints[1] or intersec == seg_below2.segment.endpoints[0] or intersec == seg_below2.segment.endpoints[1]:
                                intersec = None
                        if intersec is not None:
                            if not event_queue_list.possess(intersec):
                                event_queue_list.insert(intersec, 0, seg_below2.segment, seg_below.segment)
            #exit the current point_list
            if debug1:
                print("BEFORE THE SUPPRESSION")
                print(event_queue.value)
                event_queue_list.parcourir()
            if (current_event.next is None) and (current_event.precedent is None):
                event_queue.point_list = None
                event_queue = event_queue.next
                if event_queue is not None:
                    current_event = event_queue.point_list
                else:
                    current_event = None
            elif current_event.next is None:
                current_event.precedent.next = None
                current_event = current_event.precedent
            elif current_event.precedent is None:
                current_event.next.precedent = None
                current_event = current_event.next
                event_queue.point_list = current_event
            else:
                current_event.precedent.next = current_event.next
                current_event.next.precedent = current_event.precedent
                current_event = current_event.next
            iteration += 1
            if debug:
                #some prints allows the text color to change in the terminal, it's easier to debug
                #print ('\033[1;32m\033[1;m')
                print("IT IS ITERATION NUMBER '{}'".format(iteration))
                #print ('\033[1;37m\033[1;m')
                #print ('\033[1;35m\033[1;m')
                event_queue_list.parcourir()
                #print ('\033[1;37m\033[1;m')
                sweep_line.parcourir()
                print("")
            if debug4:
                parcourir_liste(intersections)
                print("")
    if debug:
        print(iteration)
    tycat(segments, intersections)
    print('le nombre d intersections (= le nombre de points differents) est "{}"'.format(len(intersections)))
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)


def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
