import requests
from estruturas.trie import Trie
from estruturas.hashmap import Hashmap
from estruturas.huffman import encode, get_huffman_data

def solve_packaging(weights, values, raw_capacity):
    try:
        capacity = int(raw_capacity)
    except (ValueError, TypeError):
        capacity = 0
    n = len(values)
    max_weight = sum(weights)

    if capacity >= max_weight:
        return sum(values)

    dp = [[0 for _ in range(0, capacity + 1)] for _ in range(0, n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if j >= weights[i - 1]:
                dp[i][j] = max(dp[i - 1][j], values[i - 1] + dp[i - 1][j - weights[i - 1]])
            else:
                dp[i][j] = dp[i - 1][j]
    return dp[n][capacity]

def get_all_info(category):
    url = f"{base_url}{category}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Falha ao coletar os dados. Erro: {response.status_code}")
        return None

def menu():
    print("1. Buscar pessoa por nome")
    print("2. Buscar pessoas por planeta natal")
    print("3. Buscar pessoas por prefixo do nome")
    print("4. Transmitir informações planetárias")
    print("5. Buscar veículo por id")
    print("6. Relatório de carregamento de veículos")
    print("7. Sair")
    while True:
        try:
            op = int(input("Digite sua escolha: "))

            if 0 < op < 8:
                return op
            else:
                print("Opção inválida. Digite sua escolha no intervalo disponível.")
        except ValueError:
            print("Opção inválida. Digite sua escolha no intervalo disponível.")


# MAIN
print("------ SISTEMA DE GERENCIAMENTO ESPACIAL STAR WARS ------")

people_trie = Trie()

base_url = "https://swapi.info/api/"

people_info = get_all_info("people")

if not people_info:
    print("Não foi possível carregar os dados dos personagens.")
    exit()

planets_info = get_all_info("planets")
films_info = get_all_info("films")
vehicles_info = get_all_info("vehicles")
starships_info = get_all_info("starships")

planets = Hashmap()
films = Hashmap()
vehicles = Hashmap()
starships = Hashmap()
vehicle_ids = Hashmap()
curr_id = 1

if planets_info:
    for planet in planets_info:
        planets.insert(planet["url"], planet["name"])
if films_info:
    for film in films_info:
        films.insert(film["url"], film["title"])
if vehicles_info:
    for vehicle in vehicles_info:
        vehicles.insert(vehicle["url"], vehicle["name"])
        vehicle_ids.insert(curr_id, vehicle["name"])
        curr_id += 1
if starships_info:
    for starship in starships_info:
        starships.insert(starship["url"], starship["name"])
if people_info:
    for person in people_info:
        people_trie.insert(person["name"])

while True:
    op = menu()

    if op == 1:
        name = input("Digite o nome que deseja buscar: ")
        if people_trie.search_word(name):
            for person in people_info:
                if person["name"].lower() == name.lower():
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
        planet_searched = input("Digite o planeta: ")
        found = False

        print()

        for person in people_info:
            planet_name = planets.get_val(person["homeworld"])
            if planet_name and planet_name.lower() == planet_searched.lower():
                print(person["name"])
                found = True
        if not found:
            print(f"O planeta {planet_searched} não foi encontrado no sistema.")

        print()

    elif op == 3:
        prefix = input("Digite o início do nome: ")
        names_found = people_trie.search_prefix(prefix)

        print()

        if names_found:
            for name in names_found:
                print(name)
        else:
            print(f"Nenhum personagem encontrado com o prefixo '{prefix}'.")

        print()

    elif op == 4:
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

    elif op == 5:
        target_id = input("Digite o id: ")
        try:
            target_vehicle = vehicle_ids.get_val(int(target_id))
            if target_vehicle is None:
                print(f"Nenhum veículo encontrado com o id '{target_id}'.")
            else:
                print(target_vehicle)
                print(f"Colisões de vehicle_ids: {vehicle_ids.collisions}")
        except ValueError:
            print("Id inválido.")

        print()

    elif op == 6:
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
                print("Erro. Digite somente numeros positivos separados por espaço.")

        for vehicle in vehicles_info:
            name = vehicle["name"]
            raw_capacity = vehicle["cargo_capacity"]
            max_packed_value = solve_packaging(weights, values, raw_capacity)
            print(f"Veículo: {name}, Capacidade: {raw_capacity}, Lucro total carregado: {max_packed_value} créditos")

        print()

    elif op == 7:
        break