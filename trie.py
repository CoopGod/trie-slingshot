import psycopg2


# connect to database
def connect():
    DB_USER = 'cukovzgvzwrzzb'
    DB_PASS = '89e9ce9cb2b62814123837651020c6729cc585e1eeb17bda88f73dbeb65435d1'
    DB_NAME = 'd1bmllc381j86o'
    DB_HOST = 'ec2-52-20-143-167.compute-1.amazonaws.com'
    try:
        conn =psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    except psycopg2.OperationalError:
        print("------------- Server Error -------------")
        return 0
    cur = conn.cursor()
    return {'cur': cur,'conn': conn}


# disconnect from database
def disconnect(cur, conn):
    cur.close()
    conn.close()

# used for testing
def main():
    db = connect()
    displayTrie(db)
    disconnect(db['cur'], db['conn'])


# insert word into trie
def insertWord(string, db):
    string = string.lower()
    parent = 'NULL'
    length = len(string)
    i = 0
    # main loop for scanning using all chars of string
    while i < length:
        if i == 0:
            db['cur'].execute(f"SELECT ID FROM nodes WHERE parent IS {parent} AND value='{string[i]}'")
        else:
            db['cur'].execute(f"SELECT ID FROM nodes WHERE parent = {parent} AND value='{string[i]}'")
        newNode = db['cur'].fetchall()
        # if final node, make it marked as such
        if i + 1 == length:
            # if final node exists change its wordEnd and name value
            if len(newNode) != 0:
                db['cur'].execute(f"UPDATE nodes SET word_end = True, name = '{string}' WHERE parent = {parent} AND value = '{string[i]}'")
            # if the node hasn't been created, do so
            else:
                db['cur'].execute(f"INSERT INTO nodes (parent, value, word_end, name) VALUES ({parent}, '{string[i]}', True, '{string}')")
            i += 1
        # if node exists, use it and continue
        elif len(newNode) != 0:
                parent = newNode[0][0] # get parent ID number
                i += 1
        # if node has not yet been used, create it!
        else:
            if parent == 'NULL':
                db['cur'].execute(f"INSERT INTO nodes (parent, value) VALUES (NULL, '{string[i]}')") # insert
                db['cur'].execute(f"SELECT ID FROM nodes WHERE parent IS NULL AND value='{string[i]}'") # find ID
            else:
                db['cur'].execute(f"INSERT INTO nodes (parent, value) VALUES ({parent}, '{string[i]}')") # insert
                db['cur'].execute(f"SELECT ID FROM nodes WHERE parent = {parent} AND value='{string[i]}'") # find ID
            parent = db['cur'].fetchall()[0][0] # log parent ID number
            i += 1
    db['conn'].commit()


# find word in trie
def findWord(string, db):
    string = string.lower()
    db['cur'].execute(f"SELECT id FROM nodes WHERE name = '{string}'")
    newNode = db['cur'].fetchall()
    if len(newNode) != 0:
        print('True')
        return True
    else:
        print('False')
        return False


# autocorrect word with given string (final letter of string basically becomes root)
def autocorrect(string, db):
    db['cur'].execute(f"SELECT name FROM nodes WHERE name LIKE '{string}%' ORDER BY name") # see if any full word starts with substring provided
    names = db['cur'].fetchall()
    for name in names:
        print(name[0])

# function that returns everything in trie! Uses autocorrect to gather everything from all possible root nodes
def displayTrie(db):
    # colors for pretty printing <3
    end = '\033[0m'
    color = '\033[33m'
    # for every root, print all possible words
    db['cur'].execute("SELECT value FROM nodes WHERE parent IS NULL")
    roots = db['cur'].fetchall()
    # move through root values and print pretty colors and words
    for root in roots:
        print(f"{color}{root[0].upper()} ---------------------------- {root[0].upper()}{end}")
        autocorrect(root[0], db)
    print(f"{color}--------------------------------{end}")


# delete word from trie
def deleteWord(string, db):
    string = string.lower()
    # make sure that word exists!
    if not findWord(string, db):
        print("The word does not exist!")
        return 0
    # find node of the final char in string
    db['cur'].execute(f"SELECT id, parent FROM nodes WHERE name = '{string}'")
    node = db['cur'].fetchall()
    parent = node[0][1]
    nodeID = node[0][0]
    # check if this node has children
    db['cur'].execute(f"SELECT id FROM nodes WHERE parent = {nodeID}")
    node = db['cur'].fetchall()
    if len(node) > 0:
        # remove word_end and name values
        db['cur'].execute(f"UPDATE nodes SET word_end = false, name = NULL WHERE name = '{string}'")
        print("Deleted")
        db['conn'].commit()
        return 1
    else:
        db['cur'].execute(f"DELETE FROM nodes WHERE id = {nodeID}") # delete current node
    # move through all parents checking if they have multiple children
    i = 0
    while i < len(string):
        if parent == None:
            db['cur'].execute("SELECT id FROM nodes WHERE parent IS NULL")
            children = db['cur'].fetchall()
            # see if parent has children, if yes: word is deleted, no: delete node and continue
            if len(children) > 1:
                print("Deleted")
                return 1
            else:
                db['cur'].execute(f"DELETE FROM nodes WHERE parent IS NULL AND value = '{string[i]}'") # delete current node
            i += 1
        else:
            db['cur'].execute(f"SELECT parent FROM nodes WHERE parent = {parent}")
            children = db['cur'].fetchall()
            # see if parent has children, if yes: word is deleted, no: delete node and continue
            if len(children) > 1:
                print("Deleted")
                return 1
            else:
                db['cur'].execute(f"SELECT parent FROM nodes WHERE id = {parent}") # find current node's parent node
                temp = db['cur'].fetchall()[0][0]
                db['cur'].execute(f"DELETE FROM nodes WHERE id = {parent}") # delete current node
                parent = temp
            i += 1
    db['conn'].commit()
    print("Deleted")
    return 1
    


if __name__ == "__main__":
    main()