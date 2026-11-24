from bisect import bisect_left

class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.values = []
        self.children = []
        self.leaf = leaf

class BTree:
    def __init__(self, minimum_degree=3):
        if minimum_degree < 2:
            raise ValueError("Erro. O grau mínimo deve ser de um valor maior ou igual a 2.")

        self.minimum_degree = minimum_degree
        self.root = BTreeNode()

    def insert(self, weight, person):
        root = self.root

        if len(root.keys) == 2 * self.minimum_degree - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root

        self.insert_non_full(self.root, weight, person)

    def insert_non_full(self, node, weight, person):
        index = bisect_left(node.keys, weight)

        if index < len(node.keys) and node.keys[index] == weight:
            node.values[index].append(person)
            return

        if node.leaf:
            node.keys.insert(index, weight)
            node.values.insert(index, [person])
            return

        if len(node.children[index].keys) == 2 * self.minimum_degree - 1:
            self.split_child(node, index)

            if weight == node.keys[index]:
                node.values[index].append(person)
                return

            if weight > node.keys[index]:
                index += 1

        self.insert_non_full(node.children[index], weight, person)

    def split_child(self, parent, child_index):
        degree = self.minimum_degree
        full_child = parent.children[child_index]

        right_child = BTreeNode(leaf=full_child.leaf)

        middle_key = full_child.keys[degree - 1]
        middle_values = full_child.values[degree - 1]

        right_child.keys = full_child.keys[degree:]
        right_child.values = full_child.values[degree:]

        full_child.keys = full_child.keys[:degree - 1]
        full_child.values = full_child.values[:degree - 1]

        if not full_child.leaf:
            right_child.children = full_child.children[degree:]
            full_child.children = full_child.children[:degree]

        parent.keys.insert(child_index, middle_key)
        parent.values.insert(child_index, middle_values)

        parent.children.insert(child_index + 1, right_child)

    def search_range(self, min_weight, maximum_weight):
        if min_weight > maximum_weight:
            raise ValueError("Erro. min_weight não pode ser maior que max_weight.")

        results = []
        self.recursive_search_range(self.root, min_weight, maximum_weight, results)

        return results

    def recursive_search_range(self, node, min_weight, max_weight, results):
        index = bisect_left(node.keys, min_weight)

        if not node.leaf:
            self.recursive_search_range(node.children[index], min_weight, max_weight, results)

        while index < len(node.keys) and node.keys[index] <= max_weight:
            weight = node.keys[index]

            for person in node.values[index]:
                results.append((weight, person))
            if not node.leaf:
                self.recursive_search_range(node.children[index + 1], min_weight, max_weight, results)

            index += 1