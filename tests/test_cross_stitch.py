import importlib

import networkx as nx

cross_stitch_module = importlib.import_module("lib.stitches.cross_stitch")


class DummyCross:
    def __init__(self, corners):
        self.corners = corners


def test_build_double_cycle_uses_potential_node_for_row_tour(monkeypatch):
    subcrosses = [DummyCross(corners=["corner-1"])]
    cycle = ["corner-1"]
    called = {}

    def fake_build_double_row_tour(subcrosses_arg, node, nb_repeats, remove=False):
        called["row_tour_node"] = node
        # Simulate that this tour consumed all remaining crosses.
        subcrosses_arg.clear()
        return "above", ["corner-1"]

    def fake_insert_cycle_at_node(cycle_to_increase, cycle_to_insert, node):
        called["insert_node"] = node
        return cycle_to_increase

    monkeypatch.setattr(cross_stitch_module, "_build_double_row_tour", fake_build_double_row_tour)
    monkeypatch.setattr(cross_stitch_module, "insert_cycle_at_node", fake_insert_cycle_at_node)

    result = cross_stitch_module._build_double_cycle(subcrosses, cycle, nb_repeats=0)

    assert result == ["corner-1"]
    assert called["row_tour_node"] == "corner-1"
    assert called["insert_node"] == "corner-1"


def test_build_eulerian_cycles_uses_ending_corner_for_last_subgraph(monkeypatch):
    first_subgraph = nx.Graph()
    first_subgraph.add_node("fallback-first")
    last_subgraph = nx.Graph()
    last_subgraph.add_node("fallback-last")

    start_point = "START"
    end_point = "END"
    seen_starting_corners = []

    class DummyCrossGeometries:
        center_points = set()
        crosses = []

    def fake_organize(subgraphs, cross_geoms, starting_point, ending_point):
        return [], starting_point, ending_point

    def fake_find_available_crosses(subgraph, crosses):
        if subgraph is first_subgraph:
            return [DummyCross(corners=["first-corner"])]
        return [DummyCross(corners=["last-corner"])]

    def fake_get_corner(point, subcrosses):
        if point == start_point:
            return "start-corner"
        if point == end_point:
            return "end-corner"
        return "unexpected"

    def fake_row_tour(subcrosses, starting_corner, nb_repeats, remove):
        seen_starting_corners.append(starting_corner)
        return "above", [starting_corner]

    monkeypatch.setattr(cross_stitch_module, "organize", fake_organize)
    monkeypatch.setattr(cross_stitch_module, "find_available_crosses", fake_find_available_crosses)
    monkeypatch.setattr(cross_stitch_module, "get_corner", fake_get_corner)
    monkeypatch.setattr(cross_stitch_module, "_build_simple_cycles", lambda *args: args[2])

    cycles = cross_stitch_module._build_eulerian_cycles(
        [first_subgraph, last_subgraph],
        start_point,
        end_point,
        DummyCrossGeometries(),
        nb_repeats=0,
        row_tour=fake_row_tour,
        flipped=False,
    )

    assert seen_starting_corners == ["start-corner", "end-corner"]
    assert cycles == [["start-corner"], ["end-corner"]]
