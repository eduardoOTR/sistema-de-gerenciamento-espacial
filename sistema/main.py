import requests
import unicodedata
from itertools import permutations
import matplotlib.pyplot as plt
import networkx as nx
from estruturas.trie import Trie
from estruturas.hashmap import Hashmap
from estruturas.huffman import encode, get_huffman_data
from estruturas.b_tree import BTree
from estruturas.graph import Graph

DAYS_PER_UNIT_DISTANCE = 1

# GRAPH
graph = {
    "Tatooine": {
        "Naboo": 6,
        "Dagobah": 8
    },

    "Dagobah": {
        "Hoth": 4,
        "Endor": 6,
        "Mustafar": 1,
        "Naboo": 5,
        "Tatooine": 8
    },

    "Coruscant": {
        "Alderaan": 2,
        "Naboo": 12
    },

    "Alderaan": {
        "Coruscant": 2,
        "Naboo": 14,
        "Endor": 8
    },

    "Endor": {
        "Dagobah": 6,
        "Hoth": 5,
        "Naboo": 16,
        "Mustafar": 7,
        "Alderaan": 8
    },

    "Hoth": {
        "Dagobah": 4,
        "Endor": 5,
        "Mustafar": 2
    },

    "Naboo": {
        "Alderaan": 14,
        "Coruscant": 12,
        "Mustafar": 7,
        "Tatooine": 6,
        "Endor": 16,
        "Dagobah": 5
    },

    "Mustafar": {
        "Naboo": 7,
        "Dagobah": 1,
        "Hoth": 2,
        "Endor": 7
    }
}

# FUNCTIONS
def solve_packaging(weights, values, raw_capacity):
    try:
        if str(raw_capacity).strip().lower() == "none":
            capacity = 0
        else:
            capacity = int(raw_capacity)
    except (ValueError, TypeError):
        return None, "Erro. Capacidade desconhecida."
    
    n = len(values)
    max_weight = sum(weights)

    if capacity >= max_weight:
        used = [1,2,3]
        return sum(values), used

    if capacity < min(weights):
        return 0, "Nenhuma"

    dp = [[0 for _ in range(0, capacity + 1)] for _ in range(0, n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if j >= weights[i - 1]:
                dp[i][j] = max(dp[i - 1][j], values[i - 1] + dp[i - 1][j - weights[i - 1]])
            else:
                dp[i][j] = dp[i - 1][j]

    used = []
    i = n
    w = capacity

    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            used.append(i)
            w -= weights[i - 1]
            i -= 1
        else:
            i -= 1
    used.reverse()

    return dp[n][capacity], used

def convert_mass(mass_value):
    if mass_value is None:
        return None

    try:
        mass = float(str(mass_value).replace(",", "").strip())
    except (ValueError, TypeError):
        return None
    
    if mass <= 0:
        return None
    
    return mass

def consumables_to_days(consumables):
    if consumables is None:
        return None

    value = str(consumables).strip().lower()

    if value == "unknown":
        return 30
    if value == "none":
        return 0

    parts = value.split()

    if len(parts) != 2:
        return None

    try:
        quantity = float(parts[0].replace(",", "."))
    except ValueError:
        return None

    if quantity < 0:
        return None

    unit = parts[1]

    conversion = {
        "day": 1,
        "days": 1,
        "week": 7,
        "weeks": 7,
        "month": 30,
        "months": 30,
        "year": 365,
        "years": 365
    }

    if unit not in conversion:
        return None

    return quantity * conversion[unit]

def select_starship_for_trip(starship_ids, starships_info):
    if not starships_info:
        print("Nenhuma nave disponível no sistema.")
        return None

    print("\nNaves disponíveis para viagem:")

    for starship_id, starship in enumerate(starships_info, start=1):
        consumables = consumables_to_days(starship.get("consumables"))

        if consumables == 0:
            consumables = "Nenhum"
        elif consumables is not None:
            consumables = f"{consumables:g} dias"
        else:
            consumables = "Não informado"

        print(f"{starship_id}. {starship['name']} (Consumíveis: {consumables})")

    try:
        starship_id = int(input("\nDigite o id da nave: "))
        starship = starship_ids.get_val(starship_id)

        if starship is None:
            print("Nave não encontrada.")
            return None

        return starship
    except ValueError:
        print("Id inválido.")
        return None

def check_starship_supplies(starship, distance):
    travel_days = distance * DAYS_PER_UNIT_DISTANCE

    consumables_values = starship.get("consumables")
    available_days = consumables_to_days(consumables_values)

    if available_days is None:
        print("\nNão é possível realizar a viagem. Autonomia dos consumíveis da nave não determinada.")
        return False
    if travel_days > available_days:
        print("\nNão é possível realizar a viagem. Os consumíveis da nave são insuficientes.")
        return False

    print("\nVIAGEM AUTORIZADA")

    remaining_days = available_days - travel_days
    if remaining_days == 0:
        print("Consumíveis restantes: Nenhum")
    else:
        print(f"Consumíveis restantes: {remaining_days:g} dias.")

    return True

def normalize_name(name):
    name = name.casefold()
    name = unicodedata.normalize("NFD", name)

    return "".join(char for char in name if unicodedata.category(char) != "Mn")

def traveling_salesman_brute_force(G, start_planet):
    other_planets = [planet for planet in G.nodes if planet != start_planet]
    best_route = None
    best_distance = float("inf")

    for ordering in permutations(other_planets):
        route = [start_planet, *ordering, start_planet]

        if all(G.has_edge(origin, destination) for origin, destination in zip(route, route[1:])):
            distance = nx.path_weight(G, route, weight="weight")

            if distance < best_distance:
                best_distance = distance
                best_route = route

    return best_route, best_distance

def get_all_info(category):
    url = f"{base_url}{category}/"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Falha ao coletar os dados: {error}")
        return None
    except ValueError:
        print("Erro ao interpretar os dados recebidos da API.")
        return None

def menu():
    print("1. Buscar pessoa por nome")
    print("2. Buscar pessoas por planeta natal")
    print("3. Buscar pessoas por prefixo do nome")
    print("4. Buscar veículo por id")
    print("5. Buscar pessoas por intervalo de massa corporal")
    print("6. Transmitir informações planetárias")
    print("7. Relatório de carregamento de veículos")
    print("8. Planejar viagem interplanetária")
    print("9. Encontrar caminho que visite todos os planetas apenas uma vez e retorne ao ponto de partida")
    print("10. Visualizar grafo interplanetário")
    print("0. Sair\n")

    while True:
        try:
            op = int(input("Digite sua escolha: "))

            if -1 < op < 11:
                return op
            else:
                print("Opção inválida. Digite sua escolha no intervalo disponível.")
        except ValueError:
            print("Opção inválida. Digite sua escolha no intervalo disponível.")


# MAIN
print("------ SISTEMA DE GERENCIAMENTO ESPACIAL STAR WARS ------")

people_trie = Trie()
people_mass_tree = BTree(minimum_degree=3)
planet_graph = Graph(graph)

G = nx.Graph()

for origem, destinos in graph.items():
    for destino, distancia in destinos.items():
        G.add_edge(origem, destino, weight=distancia)

base_url = "https://swapi.info/api/"

people_info = get_all_info("people")
planets_info = get_all_info("planets")
films_info = get_all_info("films")
vehicles_info = get_all_info("vehicles")
starships_info = get_all_info("starships")

if any(data is None for data in [people_info, planets_info, films_info, vehicles_info, starships_info]):
    print("Erro ao carregar dados da API.")
    exit()

planets = Hashmap()
films = Hashmap()
vehicles = Hashmap()
starships = Hashmap()

vehicle_ids = Hashmap()
starship_ids = Hashmap()

curr_id = 1
starship_curr_id = 1

if planets_info:
    for planet in planets_info:
        planets.insert(planet["url"], planet["name"])
if films_info:
    for film in films_info:
        films.insert(film["url"], film["title"])
if vehicles_info:
    for vehicle in vehicles_info:
        vehicles.insert(vehicle["url"], vehicle["name"])
        vehicle_ids.insert(curr_id, vehicle)
        curr_id += 1
if starships_info:
    for starship in starships_info:
        starships.insert(starship["url"], starship["name"])
        starship_ids.insert(starship_curr_id, starship)
        starship_curr_id += 1
if people_info:
    for person in people_info:
        people_trie.insert(normalize_name(person["name"]), person["name"])
        mass = convert_mass(person.get("mass"))
        if mass is not None:
            people_mass_tree.insert(mass, person)

while True:
    op = menu()

    if op == 1:
        name = normalize_name(input("Digite o nome que deseja buscar: "))
        if people_trie.search_word(name):
            for person in people_info:
                if normalize_name(person["name"]) == name:
                    print(f"\nNome: {person['name']}")
                    print(f"Altura: {person['height']} cm")
                    print(f"Peso: {person['mass']} kg")
                    print(f"Cabelo: {person['hair_color']}")
                    print(f"Pele: {person['skin_color']}")
                    print(f"Olhos: {person['eye_color']}")
                    print(f"Ano de nascimento: {person['birth_year']}")
                    print(f"Gênero: {person['gender']}")
                    print(f"Planeta natal: {planets.get_val(person['homeworld'])}")

                    print("\nFilmes:")
                    for film in person["films"]:
                        print(f"{films.get_val(film)}")

                    print("\nVeículos:")
                    if person["vehicles"]:
                        for vehicle in person["vehicles"]:
                            print(f"{vehicles.get_val(vehicle)}")
                    else:
                        print("Não possui")

                    print("\nNaves:")
                    if person["starships"]:
                        for starship in person["starships"]:
                            print(f"{starships.get_val(starship)}")
                    else:
                        print("Não possui")
        else:
            print(f"O nome {name} não está no sistema.")

        print()

    elif op == 2:
        planet_searched = input("Digite o planeta: ").strip()
        found_planet = False
        found_resident = False

        print()

        for planet in planets_info:
            if planet["name"].casefold() == planet_searched.casefold():
                found_planet = True
                break

        if not found_planet:
            print(f"O planeta {planet_searched} não foi encontrado no sistema.")
        else:
            for person in people_info:
                planet_name = planets.get_val(person["homeworld"])

                if planet_name and planet_name.casefold() == planet_searched.casefold():
                    print(person["name"])
                    found_resident = True

            if not found_resident:
                print(f"O planeta {planet_searched} não possui residentes.")

        print()

    elif op == 3:
        prefix = normalize_name(input("Digite o prefixo: "))
        names_found = people_trie.search_prefix(prefix)

        print()

        if names_found:
            for name in names_found:
                print(name)
        else:
            print(f"Nenhum personagem encontrado com o prefixo '{prefix}'.")

        print()

    elif op == 4:
        target_id = input("Digite o id: ")

        print()

        try:
            target_vehicle = vehicle_ids.get_val(int(target_id))
            if target_vehicle is None:
                print(f"Nenhum veículo encontrado com o id '{target_id}'.")
            else:
                print(target_vehicle["name"])
                print(f"Colisões de vehicle_ids: {vehicle_ids.collisions}")
        except ValueError:
            print("Id inválido.")

        print()

    elif op == 5:
        try:
            minimum_weight = float(input("Insira o peso mínimo (kg): ").replace(",", "."))
            maximum_weight = float(input("Insira o peso máximo (kg): ").replace(",", "."))

            if minimum_weight <= 0 or maximum_weight <= 0:
                print("Erro. Pesos devem ser maiores que 0.")
            elif minimum_weight > maximum_weight:
                print("Erro. Peso mínimo não pode ser maior que o peso máximo.")

            else:
                people_found = people_mass_tree.search_range(minimum_weight, maximum_weight)

                print(f"\nPessoas pesando entre {minimum_weight:g}kg e {maximum_weight:g}kg:")

                if people_found:
                    for weight, person in people_found:
                        print(f"Nome: {person['name']}")
                        print(f"Peso: {weight:g} kg\n")

                    print(f"Número total de pessoas encontradas: {len(people_found)}")
                    print("Total de operações de split:", people_mass_tree.splits)
                    print("Altura final da árvore:", people_mass_tree.height())
                else:
                    print("Nenhuma pessoa encontrada nessa faixa de peso.")
        except ValueError:
            print("Erro. Insira valores válidos para massa corporal.")

        print()

    elif op == 6:
        planets_string = str(planets_info).lower()
        encoded_message = encode(planets_string)

        compression_rate = (1 - (len(encoded_message) / (len(planets_string) * 8))) * 100

        huffman_data = get_huffman_data()

        print("Mensagem com as informações dos planetas enviada com sucesso!")
        print("Mensagem enviada:")
        print(encoded_message)
        print("\nTabela de frequências:")
        print(huffman_data["freq_map"])
        print("\nÁrvore de Huffman em pós ordem:")
        print(huffman_data["post_order"])
        print("\nÁrvore de Huffman em ordem simétrica:")
        print(huffman_data["in_order"])
        print("\nTabela de códigos binários:")
        print(huffman_data["encode_map"])
        print(f"\nTaxa de compressão: {compression_rate:.2f}%")

        print()

    elif op == 7:
        while True:
            try:
                weights = list(map(int, input("Digite os pesos das 3 caixas que serão carregadas (Sugestão: 10 20 30): ").split()))
                values = list(map(int, input("Digite os valores das 3 caixas (Sugestão: 60 100 120): ").split()))

                if len(weights) != 3 or len(values) != 3:
                    print("Erro. Digite exatamente 3 pesos e 3 valores separados por espaço.")
                    continue
                if any(w <= 0 for w in weights) or any(v <= 0 for v in values):
                    print("Erro. Digite somente números maiores que 0.")
                    continue

                break
            except ValueError:
                print("Erro. Digite somente números positivos separados por espaço.")

        print()

        for vehicle in vehicles_info:
            name = vehicle["name"]
            raw_capacity = vehicle["cargo_capacity"]
            max_packed_value, used_boxes = solve_packaging(weights, values, raw_capacity)
            if max_packed_value is None:
                print(f"Veículo: {name}, Capacidade: {raw_capacity}, Não foi possível calcular o carregamento.")
            else:
                print(f"Veículo: {name}, Capacidade: {raw_capacity}, Lucro total carregado: {max_packed_value} créditos, Caixas carregadas: {used_boxes}")

        print()

    elif op == 8:
        start_planet = input("Insira o planeta de partida: ")
        destination_planet = input("Insira o planeta de destino: ")

        try:
            result = planet_graph.shortest_path(start_planet, destination_planet)

            if result is None:
                print("Nenhum caminho encontrado entre os planetas inseridos.")
            else:
                path, distance = result

                print("\nMenor caminho:")
                print(" -> ".join(path))
                print(f"Distância total: {distance}")

                selected_starship = select_starship_for_trip(starship_ids, starships_info)

                if selected_starship is not None:
                    if check_starship_supplies(selected_starship, distance):
                        print(f"Nave: {selected_starship['name']}")
                        print("Trajeto: " + " -> ".join(path))
                        print(f"Tempo de viagem: {distance * DAYS_PER_UNIT_DISTANCE:g} dias")
        except ValueError as error:
            print(f"Erro: {error}")

        print()

    elif op == 9:
        start_planet = input("Insira o planeta de partida: ").strip()
        start_planet = next((p for p in G.nodes if p.lower() == start_planet.lower()), None)

        if start_planet is None:
            print("Planeta não encontrado no sistema.")
        else:
            route, total_distance = traveling_salesman_brute_force(G, start_planet)

            if route is not None:
                print("\nMenor ciclo hamiltoniano encontrado:")
                print(" -> ".join(route))
                print(f"Distância total: {total_distance:g}")
            else:
                print("Não existe ciclo hamiltoniano no grafo. Não é possível resolver o caixeiro-viajante.")

        print()

    elif op == 10:
        edge_labels = nx.get_edge_attributes(G, "weight")
        layout = nx.spring_layout(G)

        nx.draw(G, layout, with_labels=True, node_color="royalblue", node_size=2000, font_weight="bold")
        nx.draw_networkx_edge_labels(G, layout, edge_labels=edge_labels, font_color="black", font_size=9, font_weight="bold")
        plt.show()

    elif op == 0:
        break