import os
from typing import Dict

class Node():
    # children: dictionary of node, value: char, end: boolean if word has ended
    def __init__(self, children, value, end):
        self.children = children
        self.value = value
        self.end = end

### Root node list will be taken from server somehow! it is just here for now...
# roots is just the children 
roots = Node({}, None, False)

# used for testing
def main():
    insertWord(roots, 'Cooper')
    insertWord(roots, "Coopa")


# insert word into trie
def insertWord(roots, string):
    node = None
    length = len(string)
    # search roots for fisrt letter
    i = 0
    if string[i] in roots.children:
        node = roots.children[string[i]]
        i += 1
    else:
        newNode = Node({}, string[i], False)
        roots.children[string[i]] = newNode
        print(roots.children)
        node = roots.children[string[i]]
        i += 1
    
    # main loop for scanning all but first iterartion
    while i < length:
        if string[i] in node.children:
                node = node.children[string[i]]
                i += 1
        else:
            newNode = Node({}, string[i], False if length != i+1 else True)
            node.children[string[i]] = newNode
            node = node.children[string[i]]
            i += 1



main()