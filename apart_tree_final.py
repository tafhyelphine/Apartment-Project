import os
import pickle
import base64
from io import BytesIO

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Specify the desired folder name
folder_name = "ApartmentCode"

# Specify the desired file names
file_name = "realtree.bin"
maintenance_file_name = "maintenance.txt"
security_file_name = "security.txt"
sweeper_file_name = "sweeper.txt"
hash_file_name = "hashtable.bin"
cumulative_savings_file_name = "cumulative.txt"
all_expenditure_file_name = "allexpenditure.bin"

# Create the directory in the user's computer
folder_file_path = os.path.join(home_dir, folder_name)
#os.mkdir(folder_file_path)


# Construct the file path
file_path = os.path.join(home_dir, folder_name, file_name)
maintenance_file_path = os.path.join(home_dir, folder_name, maintenance_file_name)
security_file_path = os.path.join(home_dir, folder_name, security_file_name)
sweeper_file_path = os.path.join(home_dir, folder_name, sweeper_file_name)
hash_file_path = os.path.join(home_dir, folder_name, hash_file_name)
cumulative_savings_file_path = os.path.join(home_dir, folder_name, cumulative_savings_file_name)
all_expenditure_file_path = os.path.join(home_dir, folder_name, all_expenditure_file_name)


# Creating Node Class
class Node:
    def __init__(self, parent = None, val = None, children = []):
        self.parent = parent
        self.val = val
        self.children = children
    def __str__(self):
        return "TESTPLEASE"


# Creating House Class
class House:
    def __init__(self, housenum = None, parent = None, num_of_occupants = None, contact = None, maintain = None, status = None, balcony = None, BHK = None, children = []):
        self.housenum = housenum
        self.parent = parent
        self.num_of_occupants = num_of_occupants
        self.contact = contact
        self.maintain = maintain
        self.status = status
        self.balcony = balcony
        self.BHK = BHK
        self.children = None

    def __str__(self):
        return str(self.housenum) + str(self.parent) + str(self.num_of_occupants) + str(self.contact) + str(self.maintain) + str(self.status) + str(self.balcony) + str(self.BHK)


# Creating HashTable Class
class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value

    def delete(self, key):
        if key in self.table:
            del self.table[key]

    def search(self, key):
        return self.table.get(key, None)

    def update(self, key, value):
        if key in self.table:
            self.table[key] = value
        else:
            raise KeyError("Key not found in the hash table.")


# Populating the root node
root_node = Node(None, "Root", None)

A_Block = Node(root_node, "A Block", None)
A_Floor = Node(A_Block, "Floor", None)
A_Block.children = [A_Floor]

B_Block = Node(root_node, "B Block", None)
B_Ground = Node(B_Block, "B - Ground")
B_First = Node(B_Block, "B - First")
B_Second = Node(B_Block, "B - Second")
B_Third = Node(B_Block, "B - Third")
B_Block.children = [B_Ground, B_First, B_Second, B_Third]

C_Block = Node(root_node, "C Block", None)
C_Ground = Node(C_Block, "C - Ground")
C_First = Node(C_Block, "C - First")
C_Second = Node(C_Block, "C - Second")
C_Third = Node(C_Block, "C - Third")
C_Block.children = [C_Ground, C_First, C_Second, C_Third]

root_node.children = [A_Block, B_Block, C_Block]

A_Block_1 = House("A1", A_Floor)
A_Block_2 = House("A2", A_Floor)
A_Floor.children = [A_Block_1, A_Block_2]

G1 = House("G1", B_Ground)
G2 = House("G2", B_Ground)
G3 = House("G3", B_Ground)
B_Ground.children = [G1, G2, G3]

G4 = House("G4", C_Ground)
G5 = House("G5", C_Ground)
G6 = House("G6", C_Ground)
C_Ground.children = [G4, G5, G6]

F1 = House("F1", B_First)
F2 = House("F2", B_First)
F3 = House("F3", B_First)
B_First.children = [F1, F2, F3]

F4 = House("F4", C_First)
F5 = House("F5", C_First)
F6 = House("F6", C_First)
C_First.children = [F4, F5, F6]

S1 = House("S1", B_Second)
S2 = House("S2", B_Second)
S3 = House("S3", B_Second)
B_Second.children = [S1, S2, S3]

S4 = House("S4", C_Second)
S5 = House("S5", C_Second)
S6 = House("S6", C_Second)
C_Second.children = [S4, S5, S6]

T1 = House("T1", B_Third)
T2 = House("T2", B_Third)
B_Third.children = [T1, T2]

T3 = House("T3", C_Third)
T4 = House("T4", C_Third)
T5 = House("T5", C_Third)
C_Third.children = [T3, T4, T5]


# Populating the HashTable with initial values
hashtable = HashTable()
hashtable.insert("Security", 13000)
hashtable.insert("Sweeper", 4500)


# Cumulative HashTable, initially empty
big_hashtable = HashTable()


# Storing Root Node
with open(file_path, "wb") as file:
    file.truncate(0)
    pickle.dump(root_node, file)


# Storing Value of Maintenance
with open(maintenance_file_path, "w") as file:
    file.truncate(0)
    file.write("1800")


# Storing Value of Security Expense
with open(security_file_path, "w") as file:
    file.truncate(0)
    file.write("13000")


# Storing Value of Sweeper Expense
with open(sweeper_file_path, "w") as file:
    file.truncate(0)
    file.write("4500")


# Storing Monthly Expenditure HashTable
with open(hash_file_path, "wb") as file:
    file.truncate(0)
    pickle.dump(hashtable, file)


# Storing Cumulative Savings
with open(cumulative_savings_file_path, "w") as file:
    file.truncate(0)
    file.write("0")


# Storing Cumulative Expenditure HashTable
with open(all_expenditure_file_path, "wb") as file:
    file.truncate(0)
    pickle.dump(big_hashtable, file)