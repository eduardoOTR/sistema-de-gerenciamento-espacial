from queue import PriorityQueue

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

def get_huffman_data():
    return {
        "freq_map": freq_map,
        "encode_map": encode_map,
        "post_order": huffman_post_list,
        "in_order": huffman_in_list
    }