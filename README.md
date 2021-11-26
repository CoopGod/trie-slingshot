# Trie: A Slingshot 'Take Home Challenge'
### *How* It's Hosted 🏠
The server for this project is hosted using Heroku's PostgreSQL add-on.
### *How* The CLI Interacts 🧭
The python file, when run, connects to the postgreSQL database using the python library **psycopg2.** The allows the CLI to read everything from the trie. When deleting or inserting nodes into the trie, the CLI will commit changes after it has confirmed that the change is needed, rather than attemp to insert nodes that already exist, or delete nodes that are usful to the trie.
### Installation Guide 📁
1. Be sure you have downloaded the latest version of python.
2. Download this repository.
3. Launch your OS command line and navigate to the directory in which you've saved this repository.
4. Run the following command: ```pip install -r requirements.txt``` to install the library required.
5. Run the following command ```python trie.py``` to launch the CLI.
6. After the database has connected, run any of the commands listed below. Happy *trie-ing*!
### CLI Commands 🔧
**HELP** - Refer to this when you need a reminder on command names and their details.

**INSERT** - Use this command to insert a word into the trie! After selecting it, the system will prompt you to type in the word to be inserted.

**FIND** - Use this command to see if a word exists in the trie. After selecting it, the system will prompt you to type in the word to be located. Returns True or False.

**DELETE** - Use this command to remove a word from the trie! After selecting it, the system will prompt you to type in the word to be deleted.
            Will return true if word is located and will confirm deletion after process is completed.
            
**AUTO** - Use this command to locate a substring in the trie. This can be used to autocorrect for words. After selecting it, the system will prompt you to type in the 
            substring to be located. This command will return all words that begin witht he provided string.

**DISPLAY** - This command will display all complete words in the trie and where they sprout off from.      

**QUIT** - Used to exit the trie's database.
