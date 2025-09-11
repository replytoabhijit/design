class btreeNode:
    def __init__(self, order, leaf = False):
        self.order = order
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.values = []

        # self.lock = None    
        # 

class BTree:    
    def __init__(self, order):
        self.root = btreeNode(order, True)
        self.order = order

    def insert(self, key):
        root = self.root

        if len(root.keys) < self.order:
            self._insert_non_full(root, key)
        else:
            self.insert_full(root, key)
        


    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        
    def insert_full(self, node, key):
        i = len(node.keys) - 1


        pass

        # if self.root is None:
        #     self.root = self._create_node(is_leaf=True)
        #     self.root['keys'].append(key)
        #     self.root['values'].append(value)
        #     self.leaf = self.root
        # else:
        #     root = self.root
        #     if len(root['keys']) == self.max_keys:
        #         new_root = self._create_node(is_leaf=False)
        #         new_root['children'].append(self.root)
        #         self._split_child(new_root, 0)
        #         self.root = new_root
        #         self._insert_non_full(new_root, key, value)
        #     else:
        #         self._insert_non_full(root, key, value)

def main():
    a = [10, 20, 5, 6, 12, 30, 7, 17, 14, 4, 8]
    b = BTree(3)
    for i in a:
        b.insert(i, str(i))

if __name__ == "__main__":
    main()
