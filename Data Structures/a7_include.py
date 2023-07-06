# Course: CS261 - Data Structures
# Assignment: 7
# Description: 'Helper' data structures


class SLNode:
    def __init__(self, key: str, value: object) -> None:
        """
        Singly Linked List Node class
        DO NOT CHANGE THIS CLASS IN ANY WAY
        """
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        """ Return content of the node in human-readable form """
        return '(' + str(self.key) + ': ' + str(self.value) + ')'


class LinkedList:
    """
    Class implementing a Singly Linked List
    Supported methods are: insert, remove, contains, length, iterator

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self) -> None:
        """ Init new SLL """
        self.head = None
        self.size = 0

    def __str__(self) -> str:
        """ Return content of SLL in human-readable form """
        content = ''
        if self.head is not None:
            content = str(self.head)
            cur = self.head.next
            while cur is not None:
                content += ' -> ' + str(cur)
                cur = cur.next
        return 'SLL [' + content + ']'

    def insert(self, key: str, value: object) -> None:
        """ Insert new node at the beginning of the list """
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key: str) -> bool:
        """
        Remove first node with matching key
        Return True is some node was removed, False otherwise
        """
        prev, cur = None, self.head
        while cur is not None:
            if cur.key == key:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def contains(self, key: str) -> SLNode:
        """
        If node with matching key in the list -> return pointer
        to that node (SLNode), otherwise return None
        """
        cur = self.head
        while cur is not None:
            if cur.key == key:
                return cur
            cur = cur.next
        return cur

    def length(self) -> int:
        """ Return the length of the list """
        return self.size

    def __iter__(self) -> SLNode:
        """
        Provides iterator capability for the SLL class
        so it can be used in for ... in ... type of loops.
        EXAMPLE:
            for node in my_list:
                print(node.key, node.value)
        """
        cur = self.head
        while cur is not None:
            yield cur
            cur = cur.next


class DynamicArrayException(Exception):
    pass


class DynamicArray:
    """
    Class implementing a Dynamic Array
    Supported methods are:
    append, pop, swap, get_at_index, set_at_index, length

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self, arr=None):
        """ Initialize new dynamic array """
        self.data = arr.copy() if arr else []

    def __iter__(self):
        """
        Disable iterator capability for DynamicArray class
        This means loops and aggregate functions like
        those shown below won't work:

        arr = StaticArray()
        for value in arr:     # will not work
        min(arr)              # will not work
        max(arr)              # will not work
        sort(arr)             # will not work
        """
        return None

    def __str__(self) -> str:
        """ Return content of dynamic array in human-readable form """
        return str(self.data)

    def append(self, value: object) -> None:
        """ Add new element at the end of the array """
        self.data.append(value)

    def pop(self) -> object:
        """ Removes element from end of the array and return it """
        return self.data.pop()

    def swap(self, i: int, j: int) -> None:
        """ Swaps values of two elements given their indicies """
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def get_at_index(self, index: int) -> object:
        """ Return value of element at a given index """
        if index < 0 or index >= self.length():
            raise DynamicArrayException
        return self.data[index]

    def __getitem__(self, index: int) -> object:
        """ Return value of element at a given index using [] syntax """
        return self.get_at_index(index)

    def set_at_index(self, index: int, value: object) -> None:
        """ Set value of element at a given index """
        if index < 0 or index >= self.length():
            raise DynamicArrayException
        self.data[index] = value

    def __setitem__(self, index: int, value: object) -> None:
        """ Set value of element at a given index using [] syntax """
        self.set_at_index(index, value)

    def length(self) -> int:
        """ Return the length of the DA """
        return len(self.data)
