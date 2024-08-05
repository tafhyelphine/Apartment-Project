import subprocess

def install_pillow():
    try:
        # Use subprocess to run the pip install command
        subprocess.check_call(["pip", "install", "pillow"])
        print("Pillow installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Pillow: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")

# Call the function to install Pillow
install_pillow()

# Importing Module
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import messagebox
import pickle
import os
from collections import deque
from PIL import Image, ImageTk
import base64
from io import BytesIO
from datetime import date




# Global variables
pickled_tree = None
pickled_hash = None
block_iid = 0
floor_iid = 0
house_iid = 0
iid_var = 0
iid_var_2 = 0
iid_var_3 = 0
tree = None
tree2 = None
tree3 = None



# Declare global variables for entry fields
entry_house_no = None
entry_number_of_occupants = None
entry_contacts = None
entry_maintenance = None
entry_status = None
entry_balcony = None
entry_bhk = None
label_expenditure = None
label_savings = None
label_cumulative_savings = None
LabelError = None



# Get the user's home directory
home_dir = os.path.expanduser("~")
# Specify the desired folder and file names
folder_name = "ApartmentCode"
file_name = "realtree.bin"
maintenance_file_name = "maintenance.txt"
security_file_name = "security.txt"
sweeper_file_name = "sweeper.txt"
hash_file_name = "hashtable.bin"
cumulative_savings_file_name = "cumulative.txt"
all_expenditure_file_name = "allexpenditure.bin"



# Construct the file paths
file_path = os.path.join(home_dir, folder_name, file_name)
maintenance_file_path = os.path.join(home_dir, folder_name, maintenance_file_name)
security_file_path = os.path.join(home_dir, folder_name, security_file_name)
sweeper_file_path = os.path.join(home_dir, folder_name, sweeper_file_name)
hash_file_path = os.path.join(home_dir, folder_name, hash_file_name)
cumulative_savings_file_path = os.path.join(home_dir, folder_name, cumulative_savings_file_name)
all_expenditure_file_path = os.path.join(home_dir, folder_name, all_expenditure_file_name)



# Node class for the tree structure
class Node:
    def __init__(self, parent=None, val=None, children=[]):
        self.parent = parent
        self.val = val
        self.children = children

    def __str__(self):
        return self.val



# House class to store house information
class House:
    def __init__(self, housenum=None, parent=None, num_of_occupants=None, contact=None, maintain=None, status=None,
                 balcony=None, BHK=None, children=[]):
        self.housenum = housenum
        self.parent = parent
        self.num_of_occupants = num_of_occupants
        self.contact = contact
        self.maintain = maintain
        self.status = status
        self.balcony = balcony
        self.BHK = BHK
        self.children = None



# HashTable class for storing key-value pairs
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



# Check if the file exists and is non-empty
if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
    with open(file_path, "rb") as file:
        pickled_tree = pickle.load(file)
else:
    # Handle the case when the file is empty or does not exist
    pickled_tree = None

# Check if the file exists and is non-empty
if os.path.isfile(hash_file_path) and os.path.getsize(hash_file_path) > 0:
    with open(hash_file_path, "rb") as file:
        pickled_hash = pickle.load(file)
else:
    # Handle the case when the file is empty or does not exist
    pickled_hash = None

# Check if the file exists and is non-empty
if os.path.isfile(all_expenditure_file_path) and os.path.getsize(all_expenditure_file_path) > 0:
    with open(all_expenditure_file_path, "rb") as file:
        pickled_big_hash = pickle.load(file)
else:
    # Handle the case when the file is empty or does not exist
    pickled_big_hash = None



# Find house/node using preorder traversal (iterative approach)
def find_house(root, house_name):
    q = deque([root])
    while q != deque([]):
        temp = q.popleft()
        if isinstance(temp, Node):
            if temp.children is not None:
                for i in temp.children:
                    if isinstance(i, House):
                        if i.housenum == house_name:
                            return i
                    elif isinstance(i, Node):
                        if i.val == house_name:
                            return i
            if temp.children is not None:
                for i in temp.children[::-1]:
                    q.appendleft(i)



# To exit the app
def exit_program():
    with open(file_path, "wb") as file:
        file.truncate(0)
        pickle.dump(pickled_tree, file)
    window.destroy()



# Initialize the current frame variable
current_frame = None



# Function for showing frame
def show_frame(frame):
    global current_frame
    global update_frame
    if current_frame is not None:
        current_frame.pack_forget()
    if appartment_frame is not None:
        appartment_frame.pack_forget()
    frame.pack()
    current_frame = frame

# Function for showing options frame
def show_options_frame():
    global tree
    if tree is not None:
        tree.destroy()
    show_frame(options_frame)

# Function for showing update frame
def show_update_frame():
    show_frame(update_frame)

# Function for showing cumulative frame
def show_cumulative_frame():
    global tree3
    global current_frame
    global iid_var_3
    global label_cumulative_savings

    if current_frame is not None:
        current_frame.pack_forget()
    cumulative_frame.pack()
    current_frame = cumulative_frame

    if tree3 is None:
        # Create the TreeView widget
        tree3 = Treeview(cumulative_frame)

        tree3['columns'] = ("Reason", "Amount")

        tree3.column("#0", width=0, minwidth=0)
        tree3.column("Reason", anchor=W, width=140)  # Corrected column index
        tree3.column("Amount", anchor=CENTER, width=100)  # Corrected column index

        tree3.heading("#0", text='')
        tree3.heading("Reason", text="Reason")  # Corrected column index
        tree3.heading("Amount", text="Amount")  # Corrected column index

        # Configure the scrollbar
        scrollbar.config(command=tree3.yview)
        tree3.config(yscrollcommand=scrollbar.set)

        # Pack the TreeView widget
        tree3.pack(padx=10, pady=30)
    else:
        tree3.destroy()
        # Create the TreeView widget
        tree3 = Treeview(cumulative_frame)

        tree3['columns'] = ("Reason", "Amount")

        tree3.column("#0", width=0, minwidth=0)
        tree3.column("Reason", anchor=W, width=140)  # Corrected column index
        tree3.column("Amount", anchor=CENTER, width=100)  # Corrected column index

        tree3.heading("#0", text='')
        tree3.heading("Reason", text="Reason")  # Corrected column index
        tree3.heading("Amount", text="Amount")  # Corrected column index

        # Configure the scrollbar
        scrollbar.config(command=tree3.yview)
        tree3.config(yscrollcommand=scrollbar.set)

        # Pack the TreeView widget
        tree3.pack(padx=10, pady=30)
    global iid_var_3
    # Populate the treeview with data from pickled_big_hash
    for reason in pickled_big_hash.table:
        tree3.insert(parent = '', index = 'end', iid = iid_var_3, text = '', values = (reason, pickled_big_hash.table[reason]))
        iid_var_3 += 1  
    tree3.pack(padx=10, pady=30)

# Function for showing expenditure frame
def show_expenditure_frame():
    global tree2
    global current_frame
    global entry_reason
    global entry_amount
    global iid_var_2
    global label_expenditure, label_savings

    if current_frame is not None:
        current_frame.pack_forget()
    expenditure_frame.pack()
    current_frame = expenditure_frame
            
    # Check if the tree already exists
    if tree2 is None:
        # Get today's date
        today_date = date.today()

        # Checking if it is the start of the month
        if not(str(today_date)[-2] + str(today_date)[-1] == '01'):

            # Create the TreeView widget
            tree2 = Treeview(expenditure_frame)

            tree2['columns'] = ("Reason", "Amount")

            tree2.column("#0", width=0, minwidth=0)
            tree2.column("Reason", anchor=W, width=140)  # Corrected column index
            tree2.column("Amount", anchor=CENTER, width=100)  # Corrected column index

            tree2.heading("#0", text='')
            tree2.heading("Reason", text="Reason")  # Corrected column index
            tree2.heading("Amount", text="Amount")  # Corrected column index

            # Configure the scrollbar
            scrollbar.config(command=tree2.yview)
            tree2.config(yscrollcommand=scrollbar.set)

            # Pack the TreeView widget
            tree2.pack(padx=10, pady=30)
            if label_expenditure is None:
                expenditure_label()
                savings_label()
        # If it is the start of the month, update cumulative savings, and cumulative expenditure
        else:
            with open(all_expenditure_file_path, "wb+") as file:
                big_hashtable = file.load()
                for reason in pickled_hash.table:
                    if reason in big_hashtable:
                        big_hashtable[reason] += pickled_hash.table[reason]
                    else:
                        big_hashtable[reason] = pickled_hash.table[reason]
                with open(cumulative_savings_file_path, "w") as file:
                    for i in pickled_hash.table:
                        sum += int(pickled_hash.table[i])
                        with open(maintenance_file_path, "r") as file:
                            amt = int(file.read()) * 25
                        savings_amt = amt - sum
                    cumulative_savings_amt = int(file.read())
                    cumulative_savings_amt += savings_amt
                    file.truncate(0)
                    file.write(str(cumulative_savings_amt))
                for reason in pickled_hash.table:
                    if reason not in ('Security', 'Sweeper'):
                        del pickled_hash.table[reason]

            # Create the TreeView widget
            tree2 = Treeview(expenditure_frame)

            tree2['columns'] = ("Reason", "Amount")

            tree2.column("#0", width=0, minwidth=0)
            tree2.column("Reason", anchor=W, width=140)  # Corrected column index
            tree2.column("Amount", anchor=CENTER, width=100)  # Corrected column index

            tree2.heading("#0", text='')
            tree2.heading("Reason", text="Reason")  # Corrected column index
            tree2.heading("Amount", text="Amount")  # Corrected column index

            # Configure the scrollbar
            scrollbar.config(command=tree2.yview)
            tree2.config(yscrollcommand=scrollbar.set)

            # Pack the TreeView widget
            tree2.pack(padx=10, pady=30)
            if label_expenditure is None:
                expenditure_label()
                savings_label()

    else:
        # Get today's date
        today_date = date.today()

        if not(str(today_date)[-2] + str(today_date)[-1] == '01'):
            tree2.destroy()
            # Create the TreeView widget
            tree2 = Treeview(expenditure_frame)

            tree2['columns'] = ("Reason", "Amount")

            tree2.column("#0", width=0, minwidth=0)
            tree2.column("Reason", anchor=W, width=140)  # Corrected column index
            tree2.column("Amount", anchor=CENTER, width=100)  # Corrected column index

            tree2.heading("#0", text='')
            tree2.heading("Reason", text="Reason")  # Corrected column index
            tree2.heading("Amount", text="Amount")  # Corrected column index

            # Configure the scrollbar
            scrollbar.config(command=tree2.yview)
            tree2.config(yscrollcommand=scrollbar.set)

            # Pack the TreeView widget
            tree2.pack(padx=10, pady=30)
            if label_expenditure is None:
                expenditure_label()
                savings_label()
        # If it is the start of the month, update cumulative savings, and cumulative expenditure
        else:
            with open(all_expenditure_file_path, "wb+") as file:
                big_hashtable = file.load()
                for reason in pickled_hash.table:
                    if reason in big_hashtable:
                        big_hashtable[reason] += pickled_hash.table[reason]
                    else:
                        big_hashtable[reason] = pickled_hash.table[reason]
                with open(cumulative_savings_file_path, "w") as file:
                    for i in pickled_hash.table:
                        sum += int(pickled_hash.table[i])
                        with open(maintenance_file_path, "r") as file:
                            amt = int(file.read()) * 25
                        savings_amt = amt - sum
                    cumulative_savings_amt = int(file.read())
                    cumulative_savings_amt += savings_amt
                    file.truncate(0)
                    file.write(str(cumulative_savings_amt))
                for reason in pickled_hash.table:
                    if reason not in ('Security', 'Sweeper'):
                        del pickled_hash.table[reason]

            # Create the TreeView widget
            tree2 = Treeview(expenditure_frame)

            tree2['columns'] = ("Reason", "Amount")

            tree2.column("#0", width=0, minwidth=0)
            tree2.column("Reason", anchor=W, width=140)  # Corrected column index
            tree2.column("Amount", anchor=CENTER, width=100)  # Corrected column index

            tree2.heading("#0", text='')
            tree2.heading("Reason", text="Reason")  # Corrected column index
            tree2.heading("Amount", text="Amount")  # Corrected column index

            # Configure the scrollbar
            scrollbar.config(command=tree2.yview)
            tree2.config(yscrollcommand=scrollbar.set)

            # Pack the TreeView widget
            tree2.pack(padx=10, pady=30)
            if label_expenditure is None:
                expenditure_label()
                savings_label()  


    global iid_var_2
    # Populate the treeview with data from pickled_hash
    for reason in pickled_hash.table:
        tree2.insert(parent = '', index = 'end', iid = iid_var_2, text = '', values = (reason, pickled_hash.table[reason]))
        iid_var_2 += 1  

        # Pack the TreeView widget
    tree2.pack(padx=10, pady=30)



def show_appartment_frame():
    global current_frame, tree, block_iid, floor_iid, house_iid, iid_var, iid_var_2, pickled_tree
    if current_frame is not None:
        current_frame.pack_forget()
    appartment_frame.pack()
    current_frame = appartment_frame

    if tree is None:
        # Create the TreeView widget
        tree = Treeview(appartment_frame, columns=("Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7"))
        
        tree.heading("#0", text="Blocks")
        tree.heading("Column 1", text = "House No")
        tree.heading("Column 2", text="Number of occupants")
        tree.heading("Column 3", text="Contact information")
        tree.heading("Column 4", text="Maintenance")
        tree.heading("Column 5", text="Status")
        tree.heading("Column 6", text="Balcony")
        tree.heading("Column 7", text="BHK")

        # Configure the scrollbar
        scrollbar.config(command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)

        # Pack the TreeView widget
        tree.pack(padx=10, pady=30)
    else:
        tree.destroy()
        # Create the TreeView widget
        tree = Treeview(appartment_frame, columns=("Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7"))
        
        tree.heading("#0", text="Blocks")
        tree.heading("Column 1", text = "House No")
        tree.heading("Column 2", text="Number of occupants")
        tree.heading("Column 3", text="Contact information")
        tree.heading("Column 4", text="Maintenance")
        tree.heading("Column 5", text="Status")
        tree.heading("Column 6", text="Balcony")
        tree.heading("Column 7", text="BHK")

        # Configure the scrollbar
        scrollbar.config(command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)

        # Pack the TreeView widget
        tree.pack(padx=10, pady=30)



    # Populate the treeview with data from pickled_tree
    for block in pickled_tree.children:
        tree.insert(parent='', index='end', iid=iid_var, text=block.val, values=("", "", "", "", "", "", ""))
        iid_var += 1
        block_iid = iid_var
        for floor in block.children:
            tree.insert(parent=str(block_iid - 1), index='end', iid=iid_var, text=floor.val, values=("", "", "", "", "", "", ""))
            iid_var += 1
            floor_iid = iid_var
            for house in floor.children:
                tree.insert(parent=str(floor_iid - 1), index='end', iid=iid_var, text=house.housenum,
                            values=(house.housenum, house.num_of_occupants, house.contact, house.maintain, house.status,
                                    house.balcony, house.BHK))
                iid_var += 1
    # Pack the TreeView widget
    tree.pack(padx=10, pady=30)


# FUnction for back page
def go_back(previous_frame):
    global LabelError
    if LabelError is not None:
        LabelError.destroy()
    global current_frame
    current_frame.pack_forget()
    previous_frame.pack()
    current_frame = previous_frame



# Create the main window
window = Tk()
window.title("Sanjana's Salma Castle")
window.configure(bg="light grey")  # Light blue background color for the window


# Function to convert a string to an image
def string_to_image(image_base64):
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))
    return image


# Background image as a string
image_string = "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"

# Creating image object
image = string_to_image(image_string)

# Resize the image to fit the window size
image = image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))

# Create a PhotoImage object from the image
background_image = ImageTk.PhotoImage(image)

# Create a label with the background image
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the appartment frame
appartment_frame = Frame(window, bg="light grey")

# Create a scrollbar for the appartment frame
scrollbar = Scrollbar(appartment_frame)
scrollbar.pack(side=RIGHT, fill=X)

# Create the first frame
first_frame = Frame(window)
# Remove the border around the frame
first_frame.configure(bg="light grey")
first_frame.pack(pady=20)

# Create the welcome button
welcome_button = Button(first_frame, text="Welcome", command=show_options_frame, padx=25)
welcome_button.config(bg="purple", fg="white", font=("Arial", 16))
welcome_button.grid(row=20, column=20, padx=200, pady=100)

# Create the exit button
exit_button = Button(first_frame, text="Exit", command=exit_program, padx=20)
exit_button.config(bg="purple", fg="white", font=("Arial", 16))
exit_button.grid(row=21, column=20, padx=200, pady=100)

# Create the options frame
options_frame = Frame(window, bg="light grey")

# Create the buttons inside the options frame
button1 = Button(options_frame, text="Apartment Info" ,command=show_appartment_frame, width=25)
button1.config(bg="purple", fg="white", font=("Arial", 16))
button1.grid(row=20, column=20, pady=50)

button2 = Button(options_frame, text="Expenditure and Savings", command=show_expenditure_frame, width=50)
button2.config(bg="purple", fg="white", font=("Arial", 16))
button2.grid(row=21, column=20, pady=50)

button3 = Button(options_frame, text="Update",command=show_update_frame, width=20)
button3.config(bg="purple", fg="white", font=("Arial", 16))
button3.grid(row=22, column=20, pady=50)

button4 = Button(options_frame, text="Exit Program",command=exit_program, width=25)
button4.config(bg="purple", fg="white", font=("Arial", 16))
button4.grid(row=23, column=20, pady=50)

# Create the appartment frame
appartment_frame = Frame(window, bg="light grey")

# Create the block frame
block_frame = Frame(window, bg="light grey")

# Create the floor frame
floor_frame = Frame(window, bg="light grey")

# Create the update frame
update_frame = Frame(window, bg="light grey")

# Create the expenditure frame
expenditure_frame = Frame(window, bg = "light grey")

# Create the cumulative expenditure frame
cumulative_frame = Frame(window, bg = "light grey")


# Create back button from cumulative frame to expenditure frame
back_button_cumulative = Button(cumulative_frame, text = "Back", command = show_expenditure_frame)
back_button_cumulative.config(bg = "purple", fg = "white", font = ("Arial", 16))
back_button_cumulative.pack(pady=10)


# Back button from update frame to options frame
back_button_update = Button(update_frame, text="Back", command=show_options_frame)
back_button_update.config(bg="purple", fg="white", font=("Arial", 16))
back_button_update.pack(pady=10)


# Create the entry fields for the properties in the apartment frame
entry_reason = Entry(expenditure_frame, font=("Arial", 16), width=50)
entry_amount = Entry(expenditure_frame, font=("Arial", 16), width=20)

# Create the labels for the entry fields
label_reason = Label(expenditure_frame, text="Reason: ", font=("Arial", 16), bg="light grey")
label_amount = Label(expenditure_frame, text="Amount:", font=("Arial", 16), bg="light grey")
        
# Pack the labels and entrys
label_reason.pack(pady=0)
entry_reason.pack(pady=0)
label_amount.pack(pady=0)
entry_amount.pack(pady=0)

# Cumulative Savings Label
cumulative_savings_text = "Cumulative Savings: "
with open(cumulative_savings_file_path, "r") as file:
    cumulative_savings_text += file.read()

cumulative_savings_label = Label(cumulative_frame, text = cumulative_savings_text, font = ("Arial", 16), bg = "light grey")
cumulative_savings_label.pack(pady=0)

# View Cumulative Expenditure Button
cumulative_expenditure_button_expenditure = Button(expenditure_frame, text="View Cumulative Expenditure", command=show_cumulative_frame)
cumulative_expenditure_button_expenditure.config(bg = "purple", fg = "white", font =("Arial", 16), padx= 25)
cumulative_expenditure_button_expenditure.pack(pady=10)

# Back button
back_button_expenditure = Button(expenditure_frame, text="Back", command=lambda: go_back(options_frame))
back_button_expenditure.config(bg="purple", fg="white", font=("Arial", 16), padx=25)
back_button_expenditure.pack(pady=10)


# Function to remove selected records from Expenditure Table
def remove_element():
    global pickled_hash
    selected_items = tree2.selection()
    if selected_items:
        for item in selected_items:
            values = tree2.item(item, 'values')
            del pickled_hash.table[values[0]]
            with open(hash_file_path, "wb") as file:
                file.truncate(0)
                pickle.dump(pickled_hash, file)
            tree2.delete(item)
    global label_expenditure, label_savings
    label_expenditure.destroy()
    label_savings.destroy()
    expenditure_label()
    savings_label()


# Function to select record from Expenditure Table
def select_function_hash():
    entry_reason.delete(0,END)
    entry_amount.delete(0, END)
    selected = tree2.focus()
    values = tree2.item(selected, 'values')
    #output to entry boxes
    entry_reason.insert(0, values[0])
    entry_amount.insert(0, values[1])
        


# Function to update selected record from Expenditure Table
def update_function_hash():
    global pickled_hash
    global LabelError
    selected = tree2.focus()
    # Save new data
    tree2.item(selected, text='', values=(entry_reason.get(), entry_amount.get()))
    updated_reason = entry_reason.get()
    updated_amount = entry_amount.get()
    if updated_reason in pickled_hash.table:
        pickled_hash.update(updated_reason, updated_amount)
    else:
        LabelError = Label(expenditure_frame, text = "Cannot Update a record that isn't present!", font =("Arial", 16), bg = "light grey")
        LabelError.pack()
    # Clear the input fields
    entry_reason.delete(0, END)
    entry_amount.delete(0, END)
    # Update the pickled_tree object with the modifications
    with open(hash_file_path, "wb") as file:
        file.truncate(0)
        pickle.dump(pickled_hash, file)
    global label_expenditure, label_savings
    label_expenditure.destroy()
    label_savings.destroy()
    expenditure_label()
    savings_label()



# Function to insert record into Expenditure Table
def insert_function_hash():
    global pickled_hash, iid_var_2
    tree2.insert(parent = '', index = 'end', iid = iid_var_2 + 1, text = '', values = (entry_reason.get(), entry_amount.get()))
    iid_var_2 += 1
    inserted_reason = entry_reason.get()
    inserted_amount = entry_amount.get()
    pickled_hash.insert(inserted_reason, inserted_amount)
    #Clear the input fields
    entry_reason.delete(0, END)
    entry_amount.delete(0, END)
    with open(hash_file_path, "wb") as file:
        file.truncate(0)
        pickle.dump(pickled_hash, file)
    global label_expenditure, label_savings
    label_expenditure.destroy()
    label_savings.destroy()
    expenditure_label()
    savings_label()



# Button to Select the record
select_button_expenditure = Button(expenditure_frame, text = "Select", command = select_function_hash)
select_button_expenditure.config(bg = "purple", fg = "white", font = ("Arial", 16), padx=30)
select_button_expenditure.pack(pady=1)


# Create the Update button in the expenditure frame
update_button_expenditure = Button(expenditure_frame, text="Update", command=update_function_hash)
update_button_expenditure.config(bg="purple", fg="white", font=("Arial", 16), padx=35)
update_button_expenditure.pack(pady=1)


# Button to Insert Record
insert_button_expenditure = Button(expenditure_frame, text="Insert", command=insert_function_hash)
insert_button_expenditure.config(bg="purple", fg="white", font=("Arial", 16), padx=30)
insert_button_expenditure.pack(pady=1)


# Remove Button in expenditure frame
remove_button = Button(expenditure_frame, text="Remove", command=remove_element)
remove_button.config(bg="purple", fg="white", font=("Arial", 16), padx=30)
remove_button.pack(pady=1)


# Expenditure label in expenditure frame
def expenditure_label():
    global label_expenditure
    expenditure_label_text = ""
    sum = 0
    for i in pickled_hash.table:
        sum += int(pickled_hash.table[i])
    expenditure_label_text = str(sum)
    expenditure_label_text = "Expenditure: " + str(sum)

    label_expenditure = Label(expenditure_frame, text=expenditure_label_text, font=("Arial", 16), bg="light grey")
    label_expenditure.pack(pady=0)


# Savings label in savings frame
def savings_label():
    global label_savings
    sum = 0
    for i in pickled_hash.table:
        sum += int(pickled_hash.table[i])
    savings_label_text = ""
    with open(maintenance_file_path, "r") as file:
        amt = int(file.read()) * 25
    savings_amt = amt - sum
    savings_label_text = "Savings: " + str(savings_amt)

    label_savings = Label(expenditure_frame, text = savings_label_text, font=("Arial", 16), bg="light grey")
    label_savings.pack(pady=0)


# Create the buttons in the update frame
# Creating functions for updating maintenance value at large

# Create the entry fields for the properties in the apartment frame
entry_house_no = Entry(appartment_frame, font = ("Arial", 16))
entry_number_of_occupants = Entry(appartment_frame, font=("Arial", 16))
entry_contacts = Entry(appartment_frame, font=("Arial", 16))
entry_maintenance = Entry(appartment_frame, font=("Arial", 16))
entry_status = Entry(appartment_frame, font=("Arial", 16))
entry_balcony = Entry(appartment_frame, font=("Arial", 16))
entry_bhk = Entry(appartment_frame, font=("Arial", 16))

# Create the labels for the entry fields
label_house_no = Label(appartment_frame, text="House No", font=("Arial", 16), bg="light grey")
label_number_of_occupants = Label(appartment_frame, text="Number of Occupants", font=("Arial", 16), bg="light grey")
label_contacts = Label(appartment_frame, text="Contacts", font=("Arial", 16), bg="light grey")
label_maintenance = Label(appartment_frame, text="Maintenance", font=("Arial", 16), bg="light grey")
label_status = Label(appartment_frame, text="Status", font=("Arial", 16), bg="light grey")
label_balcony = Label(appartment_frame, text="Balcony", font=("Arial", 16), bg="light grey")
label_bhk = Label(appartment_frame, text="BHK", font=("Arial", 16), bg="light grey")

# Pack the labels and entry fields in the apartment frame
label_house_no.pack(pady=0)
entry_house_no.pack(pady=0)
label_number_of_occupants.pack(pady=0)
entry_number_of_occupants.pack(pady=0)
label_contacts.pack(pady=0)
entry_contacts.pack(pady=0)
label_maintenance.pack(pady=0)
entry_maintenance.pack(pady=0)
label_status.pack(pady=0)
entry_status.pack(pady=0)
label_balcony.pack(pady=0)
entry_balcony.pack(pady=0)
label_bhk.pack(pady=0)
entry_bhk.pack(pady=0)
back_button_appartment = Button(appartment_frame, text="Back", command=lambda: go_back(options_frame))
back_button_appartment.config(bg="purple", fg="white", font=("Arial", 16))
back_button_appartment.pack(pady=10)


# Function to select a record
def select_function():
    global entry_number_of_occupants
    global entry_balcony
    global entry_bhk
    global entry_contacts
    global entry_status
    global entry_maintenance
    global entry_house_no
    entry_house_no.delete(0, END)
    entry_number_of_occupants.delete(0,END)
    entry_contacts.delete(0, END)
    entry_maintenance.delete(0,END)
    entry_status.delete(0,END)
    entry_balcony.delete(0, END)
    entry_bhk.delete(0,END)
    #grabbing record number
    selected = tree.focus()
    values = tree.item(selected, 'values')
    #output to entry boxes
    entry_house_no.insert(0, values[0])
    entry_number_of_occupants.insert(0, values[1])
    entry_contacts.insert(0, values[2])
    entry_maintenance.insert(0, values[3])
    entry_status.insert(0, values[4])
    entry_balcony.insert(0, values[5])
    entry_bhk.insert(0, values[6])


# Function to update a record
def update_function():
    global entry_number_of_occupants
    global entry_balcony
    global entry_bhk
    global entry_contacts
    global entry_status
    global entry_maintenance
    global pickled_tree
    global entry_house_no
    # Creating Conditions to check for valid input
    house_no_condition = entry_house_no.get()[0] in ("G", "F", "S", "T") and entry_house_no.get()[1] in ("1", "2", "3", "4", "5", "6") and entry_house_no.get() != "T6"
    contact_condition_all_numbers = True
    for i in entry_contacts.get():
        if not(ord(i) > 47 and ord(i) < 58):
            contact_condition_all_numbers = False
            break
    contact_condition = (len(entry_contacts.get()) != 10 or len(entry_contacts.get()) != 8) and contact_condition_all_numbers
    # If valid input
    if house_no_condition and contact_condition:
        selected = tree.focus()
        # Save new data
        tree.item(selected, text=entry_house_no.get(), values=(entry_house_no.get(), entry_number_of_occupants.get(), entry_contacts.get(), entry_maintenance.get(), entry_status.get(), entry_balcony.get(), entry_bhk.get()))
        # Find the house and update its attributes
        updated_house = find_house(pickled_tree, entry_house_no.get())
        updated_house.num_of_occupants = entry_number_of_occupants.get()
        updated_house.contact = entry_contacts.get()
        updated_house.maintain = entry_maintenance.get()
        updated_house.status = entry_status.get()
        updated_house.balcony = entry_balcony.get()
        updated_house.BHK = entry_bhk.get()
        # Clear the input fields
        entry_house_no.delete(0, END)
        entry_number_of_occupants.delete(0, END)
        entry_contacts.delete(0, END)
        entry_maintenance.delete(0, END)
        entry_status.delete(0, END)
        entry_balcony.delete(0, END)
        entry_bhk.delete(0, END)
        # Update the pickled_tree object with the modifications
        with open(file_path, "wb") as file:
            file.truncate(0)
            pickle.dump(pickled_tree, file)
    # If not valid input, display error
    else:
        messagebox.showinfo("Error", "Please Enter Correct Details!")


# Select the record
select_button_apartment = Button(appartment_frame, text = "Select", command = select_function)
select_button_apartment.config(bg = "purple", fg = "white", font = ("Arial", 16))
select_button_apartment.pack(pady=1)

# Create the Update button in the apartment frame
update_button_appartment = Button(appartment_frame, text="Update", command=update_function)
update_button_appartment.config(bg="purple", fg="white", font=("Arial", 16))
update_button_appartment.pack(pady=1)


# Function to update maintenance value of all houses to 0
def update_all_0():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        global pickled_tree
        root = pickled_tree
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = 0
        show_frame(first_frame)


update_all_0_update = Button(update_frame, text="Update All to 0", command=update_all_0, width=30)
update_all_0_update.config(bg="purple", fg="white", font=("Arial", 16))
update_all_0_update.pack(pady=10)


# Function to update maintenance value of A block to 0
def update_A_0():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        global pickled_tree
        root = pickled_tree.children[0]
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = 0
        show_frame(first_frame)

update_A_0_update = Button(update_frame, text="Update A block to 0", command=update_A_0, width=27)
update_A_0_update.config(bg="purple", fg="white", font=("Arial", 16))
update_A_0_update.pack(pady=10)


# Function to update maintenance value of B block to 0
def update_B_0():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        global pickled_tree
        root = pickled_tree.children[1]
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = 0
        show_frame(first_frame)

update_B_0_update = Button(update_frame, text="Update B block to 0", command=update_B_0, width=24)
update_B_0_update.config(bg="purple", fg="white", font=("Arial", 16))
update_B_0_update.pack(pady=10)


# Function to update maintenance value of C block to 0
def update_C_0():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        global pickled_tree
        root = pickled_tree.children[2]
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = 0
        show_frame(first_frame)

update_C_0_update = Button(update_frame, text="Update C block to 0", command=update_C_0, width=27)
update_C_0_update.config(bg="purple", fg="white", font=("Arial", 16))
update_C_0_update.pack(pady=10)


# Function to update maintenance value of all houses to paid
def update_all_paid():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        with open(maintenance_file_path, "r") as file:
            maintain_val = int(file.read())
        global pickled_tree
        root = pickled_tree
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = maintain_val
        show_frame(first_frame)

update_all_paid_update = Button(update_frame, text="Update All to paid", command=update_all_paid, width=30)
update_all_paid_update.config(bg="purple", fg="white", font=("Arial", 16))
update_all_paid_update.pack(pady=10)


# Function to update maintenance value of A block to paid
def update_A_paid():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        with open(maintenance_file_path, "r") as file:
            maintain_val = int(file.read())
        global pickled_tree
        root = pickled_tree.children[0]
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = maintain_val
        show_frame(first_frame)

update_A_paid_update = Button(update_frame, text="Update A block to paid", command=update_A_paid, width=34)
update_A_paid_update.config(bg="purple", fg="white", font=("Arial", 16))
update_A_paid_update.pack(pady=10)


# Function to update maintenance value of B block to paid
def update_B_paid():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        with open(maintenance_file_path, "r") as file:
            maintain_val = int(file.read())
        global pickled_tree
        root = pickled_tree.children[1]
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = maintain_val
        show_frame(first_frame)

update_B_paid_update = Button(update_frame, text="Update B block to paid", command=update_B_paid, width=37)
update_B_paid_update.config(bg="purple", fg="white", font=("Arial", 16))
update_B_paid_update.pack(pady=10)


# Function to update maintenance value of C block to paid
def update_C_paid():
    answer = messagebox.askyesno("Confirmation", "Are you sure that you want to update?")
    if answer:
        with open(maintenance_file_path, "r") as file:
            maintain_val = int(file.read())
        global pickled_tree
        root = pickled_tree.children[2]
        global tree
        q = deque([root])
        while q != deque([]):
            temp = q.pop()
            if isinstance(temp, Node):
                for i in temp.children[::-1]:
                    q.append(i)
            elif isinstance(temp, House):
                temp.maintain = maintain_val
        show_frame(first_frame)

update_C_paid_update = Button(update_frame, text="Update C block to paid", command=update_C_paid, width=40)
update_C_paid_update.config(bg="purple", fg="white", font=("Arial", 16))
update_C_paid_update.pack(pady=10)

#Label for set maintenance
label_set_maintenance = Label(update_frame, text="Set maintenance to:", font=("Arial", 16), bg="light grey")
label_set_maintenance.pack(pady=10)

#Entry for set maintenance
entry_set_maintenance = Entry(update_frame, font=("Arial", 16), width=45)
entry_set_maintenance.pack(pady=10)


# Function for updating maintenance amount collected from each house
def update_maintenance():
    to_be_updated_to = entry_set_maintenance.get()
    with open(maintenance_file_path, "w") as file:
        file.truncate(0)
        file.write(to_be_updated_to)


#Button for set maintenance
button_set_maintenance = Button(update_frame, text = "Set Maintenance", command = update_maintenance, width=40)
button_set_maintenance.config(bg="purple", fg="white", font=("Arial", 16))
button_set_maintenance.pack(pady = 10)

# Start with the first frame
show_frame(first_frame)

# Start the main loop
window.mainloop()