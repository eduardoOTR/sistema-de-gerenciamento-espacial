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
        visited_nodes = 0

        for char in word:
            index = self.get_index(char)

            if current_node.children[index] is None:
                print(f"{visited_nodes} nós visitados.")
                return False

            current_node = current_node.children[index]
            visited_nodes += 1

        print(f"Nós visitados: {visited_nodes}")
        return current_node.is_end_of_word

    def search_prefix(self, prefix):
        prefix = prefix.lower()
        current_node = self.root
        visited_nodes = 0

        for char in prefix:
            index = self.get_index(char)

            if current_node.children[index] is None:
                print(f"Nós visitados: {visited_nodes}")
                return []

            current_node = current_node.children[index]
            visited_nodes += 1

        results = []

        if current_node.is_end_of_word:
            results.append(current_node.original_word)

        for child_node in current_node.children:
            if child_node is not None:
                visited_nodes += self.dfs(child_node, results)

        print(f"Nós visitados: {visited_nodes}")
        return results

    def dfs(self, node, results):
        visited_nodes = 1

        if node.is_end_of_word:
            results.append(node.original_word)

        for child_node in node.children:
            if child_node is not None:
                visited_nodes += self.dfs(child_node, results)

        return visited_nodes