from queue import PriorityQueue
import requests

# HUFFMAN CODE
encode_map = {}
freq_map = {}
huffman_post_list = []
huffman_in_list = []

class HuffmanNode:
    def __init__(self, freq, data, left, right):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def count_freq(message):
    for char in message:
        if char in freq_map.keys():
            freq_map[char] += 1
        else:
            freq_map[char] = 1

def create_huffman_tree():
    p_queue = PriorityQueue()

    for key in freq_map.keys():
        node = HuffmanNode(freq_map[key], key, None, None)
        p_queue.put((node.freq, node))

    while p_queue.qsize() > 1:
        _, first = p_queue.get()
        _, second = p_queue.get()
        parent_freq = first.freq + second.freq

        parent_node = HuffmanNode(parent_freq, str(parent_freq), first, second)
        p_queue.put((parent_node.freq, parent_node))

    _, root = p_queue.get()
    return root

def set_bit_code(node, bit_str):
    if node is None:
        return
    if node.left is None and node.right is None:
        if bit_str == "":
            bit_str = "0"

        encode_map[node.data] = bit_str
        return

    set_bit_code(node.left, bit_str + "0")
    set_bit_code(node.right, bit_str + "1")

def post_in_traversal(node):
    if node is None:
        return
    post_in_traversal(node.left)
    huffman_in_list.append(node.data)
    post_in_traversal(node.right)
    huffman_post_list.append(node.data)

def encode(message):
    global encode_map
    global freq_map
    global huffman_post_list
    global huffman_in_list
    encode_map = {}
    freq_map = {}
    huffman_post_list = []
    huffman_in_list = []

    if not message:
        return ""

    count_freq(message)
    root = create_huffman_tree()
    post_in_traversal(root)
    set_bit_code(root, "")

    return "".join(encode_map[char] for char in message)

# TRIE CODE
class TrieNode:
    def __init__(self):
        # Cada índice representa um caractere ASCII, evitando o uso de dict
        self.children = [None] * 256
        self.is_end_of_word = False
        self.original_word = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def get_index(self, char):
        return ord(char)

    def insert(self, word):
        original_word = word
        word = word.lower()
        current_node = self.root

        for char in word:
            index = self.get_index(char)

            if current_node.children[index] is None:
                current_node.children[index] = TrieNode()

            current_node = current_node.children[index]

        current_node.is_end_of_word = True
        current_node.original_word = original_word

    def search_word(self, word):
        word = word.lower()
        current_node = self.root

        for char in word:
            index = self.get_index(char)

            if current_node.children[index] is None:
                return False

            current_node = current_node.children[index]

        return current_node.is_end_of_word

    def search_prefix(self, prefix):
        prefix = prefix.lower()
        current_node = self.root

        for char in prefix:
            index = self.get_index(char)

            if current_node.children[index] is None:
                return []

            current_node = current_node.children[index]

        results = []
        self.dfs(current_node, results)

        return results

    def dfs(self, node, results):
        if node.is_end_of_word:
            results.append(node.original_word)

        for child_node in node.children:
            if child_node is not None:
                self.dfs(child_node, results)

# FUNCTIONS
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

        print("Mensagem com as informações dos planetas enviada com sucesso!")
        print("Mensagem enviada:")
        print(encoded_message)
        print("\nTabela de frequências:")
        print(freq_map)
        print("\nÁrvore de Huffman em pós ordem:")
        print(huffman_post_list)
        print("\nÁrvore de Huffman em ordem simétrica:")
        print(huffman_in_list)
        print("\nTabela de códigos binários:")
        print(encode_map)
        print(f"\nTaxa de compressão: {compression_rate:.2f}%")

        print()
            
    elif op == 5:
        break