import networkx as nx

class Graph:
    def __init__(self, adjacency_list):
        self.graph = nx.Graph()
        for planet, connections in adjacency_list.items():
            for neighbor, distance in connections.items():
                if distance < 0:
                    raise ValueError("Erro. A distância não pode ser negativa.")

                self.graph.add_edge(planet, neighbor, weight=distance)

    def shortest_path(self, start_planet, destination_planet):
        planets = {planet.casefold(): planet for planet in self.graph.nodes}

        start_planet = planets.get(start_planet.strip().casefold())
        destination_planet = planets.get(destination_planet.strip().casefold())

        if start_planet is None:
            raise ValueError("Planeta de partida não encontrado.")
        if destination_planet is None:
            raise ValueError("Planeta de destino não encontrado.")

        try:
            distance, path = nx.single_source_dijkstra(self.graph, source=start_planet, target=destination_planet, weight="weight")
            return path, distance
        except nx.NetworkXNoPath:
            return None