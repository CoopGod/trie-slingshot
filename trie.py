import os

class Node():
    # children: dictionary of node, value: char, end: boolean if word has ended
    def __init__(self, children, value, end):
        self.children = children
        self.value = value
        self.end = end

### Root node list will be taken from server somehow! it is just here for now...
roots = Node({}, None, False)

# used for testing
def main():
    insertWord(roots, 'Cooper')
    insertWord(roots, "coopa")
    deleteWord(roots, 'cOoper')
    findWord(roots, "cooper")
    findWord(roots, 'coopa')


# insert word into trie
def insertWord(roots, string):
    string = string.lower()
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

# find word in trie
def findWord(roots, string):
    string = string.lower()
    node = roots
    i = 0
    while i < len(string):
        if string[i] in node.children:
            node = node.children[string[i]]
            if i + 1 == len(string) and node.end == True:
                print('true')
                return True
            i += 1
        else:
            print('false')
            return False
    print("False")
    return False 


# delete word from trie
def deleteWord(roots, string):
    string = string.lower()
    node = roots
    i = 0
    parents = []
    # collect all nodes until leaf is found
    while i < len(string):
        if string[i] in node.children:
            temp = node
            node = node.children[string[i]]
            # if is branch and not leaf
            if i + 1 == len(string) and node.end == True and len(temp.children) != 1:
                node.end = False
                parents = []
            else:
                parents.append(node)
            i += 1
        else:
            print('Word not in Trie')
            return False
    
    i = 0
    parents.reverse()
    string = string[::-1]
    while i < len(parents):
        # check if branch
        if len(parents[i].children) == 1:
            print("Word Deleted")
            return True
        else:
            del parents[i+1].children[string[i]]
        i += 1
    print("Word Deleted")
    return True



if __name__ == "__main__":
    main()