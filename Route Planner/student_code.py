import math
import heapq
from queue import PriorityQueue


def shortest_path(M, start, goal):
    frontier = PriorityQueue()
    frontier.put( start,  None)
    explored = { start:  None}
    graph_score = { start: 0}

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            path = construct_path(explored, start, goal)

        for next in M.roads[current]:
            temp_graph_score = graph_score[current] + distance(M, current, next)
            if next not in graph_score or temp_graph_score < graph_score[next]:
                graph_score[next] = temp_graph_score
                other_score = temp_graph_score + distance(M, goal, next)
                frontier.put(next, True ,other_score)
                explored[next] = current
    return path

def construct_path(explored, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = explored[current]
        path.append(current)
    path.reverse()
    return path


def distance(M, A, B):
    return math.sqrt((M.intersections[B][0] - M.intersections[A][0]) ** 2 + (M.intersections[B][1] - M.intersections[A][1]) ** 2)