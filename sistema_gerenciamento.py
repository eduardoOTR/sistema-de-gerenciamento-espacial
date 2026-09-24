from queue import PriorityQueue
import requests

# HUFFMAN CODE
global encode_map
encode_map = {}

class HuffmanNode:
    def __init__(self, freq, data, left, right):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def count_freq(message):
    freq_map = {}
    for char in message:
        if char in freq_map.keys():
            freq_map[char] += 1
        else:
            freq_map[char] = 1
    return freq_map

def create_huffman_tree(freq_map):
    p_queue = PriorityQueue()
    for key in freq_map.keys():
        node = HuffmanNode(freq_map[key], key, None, None)
        p_queue.put((node.freq, node))

    while p_queue.qsize() > 1:
        ignore, first = p_queue.get()
        ignore, second = p_queue.get()

        parent_node = HuffmanNode(first.freq + second.freq, "-", first, second)
        p_queue.put((parent_node.freq, parent_node))

    ignore, root = p_queue.get()
    return root

def set_bit_code(node, bit_str):
    if node is None:
        return
    if node.left is None and node.right is None:
        encode_map[node.data] = bit_str
        return

    set_bit_code(node.left, bit_str + "0")
    set_bit_code(node.right, bit_str + "1")

def encode(message):
    freq_map = count_freq(message)
    root = create_huffman_tree(freq_map)
    set_bit_code(root, "")

    encoded_message = ""
    for char in message:
        encoded_message += encode_map[char]
    return encoded_message


# TRIE CODE
class TrieNode:
    def __init__(self):
        # Cada índice representa um caractere ASCII, evitando o uso de dict
        self.children = [None] * 256
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def get_index(self, char):
        return ord(char)

    def insert(self, word):
        current_node = self.root

        for char in word:
            index = self.get_index(char)

            if current_node.children[index] is None:
                current_node.children[index] = TrieNode()

            current_node = current_node.children[index]

        current_node.is_end_of_word = True

    def search_word(self, word):
        current_node = self.root

        for char in word:
            index = self.get_index(char)

            if current_node.children[index] is None:
                return False

            current_node = current_node.children[index]

        return current_node.is_end_of_word

    def search_prefix(self, prefix):
        current_node = self.root

        for char in prefix:
            index = self.get_index(char)

            if current_node.children[index] is None:
                return []

            current_node = current_node.children[index]

        results = []
        self.dfs(current_node, prefix, results)

        return results

    def dfs(self, node, current_word, results):
        if node.is_end_of_word:
            results.append(current_word)

        for index, child_node in enumerate(node.children):
            if child_node is not None:
                char = chr(index)
                self.dfs(child_node, current_word + char, results)


# FUNCTIONS
def get_all_info(category):
    url = f"{base_url}{category}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Falha ao coletar os dados. Erro: {response.status_code}")

def menu():
    print("1. Buscar pessoa por nome")
    print("2. Buscar pessoas por planeta natal")
    print("3. Buscar pessoas por prefixo do nome")
    print("4. Sair")
    while True:
        try:
            op = int(input("Digite sua escolha: "))

            if 0 < op < 5:
                return op
            else:
                print("Opção inválida. Digite sua escolha no intervalo disponível.")
        except:
            print("Opção inválida. Digite sua escolha no intervalo disponível.")


# MAIN
print("------ SISTEMA DE GERENCIAMENTO ESPACIAL STAR WARS ------")

people_trie = Trie()

base_url = "https://swapi.info/api/"

people_info = get_all_info("people")
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
                if person["name"] == name:

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
            print(f"\nNenhum personagem encontrado com o prefixo '{prefix}'.")

        print()
            
    elif op == 4:
        break