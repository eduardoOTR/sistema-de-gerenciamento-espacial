import requests
from estruturas.trie import Trie
from estruturas.huffman import encode, get_huffman_data

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
    print("5. Sair")
    while True:
        try:
            op = int(input("Digite sua escolha: "))

            if 0 < op < 6:
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

planets = {}
films = {}
vehicles = {}
starships = {}

if planets_info:
    for planet in planets_info:
        planets[planet["url"]] = planet["name"]
if films_info:
    for film in films_info:
        films[film["url"]] = film["title"]
if vehicles_info:
    for vehicle in vehicles_info:
        vehicles[vehicle["url"]] = vehicle["name"]
if starships_info:
    for starship in starships_info:
        starships[starship["url"]] = starship["name"]
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
                    print(f"Planeta natal: {planets[person['homeworld']]}")

                    print("\nFilmes:")
                    for film in person["films"]:
                        print(f"{films[film]}")

                    print("\nVeículos:")
                    if person["vehicles"]:
                        for vehicle in person["vehicles"]:
                            print(f"{vehicles[vehicle]}")
                    else:
                        print("Não possui")

                    print("\nNaves:")
                    if person["starships"]:
                        for starship in person["starships"]:
                            print(f"{starships[starship]}")
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
            planet_name = planets.get(person["homeworld"])
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
        break