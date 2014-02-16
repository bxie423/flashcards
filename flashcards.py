# flashcards.py - A simple flashcard program.
# usage: flashcards.py <optional stack file>

import random
import re
import sys
import os
import shutil

class flashcard():
    def __init__(self, word, defn):
        self.word = word
        self.defn = defn

class fstack():
    def __init__(self):
        self.lst = []
    def num_of_cards(self):
        return len(self.lst)
    def get_card(self, idx):
        return self.lst[idx-1]
    def add_card(self, card):
        self.lst.append(card)
    def view_stack(self):
        if self.lst == []:
            print("There are no cards in the stack yet!")
        else:
            for i,card in enumerate(self.lst):
                print("{:6s}{:60s}\t{:120s}".format(str(i+1) + ".", card.word, card.defn))
    def remove_card(self, idx): # Not safe - assumes card index exists
        self.lst.pop(idx-1)
    def edit_card(self, idx, new): # Not safe - assumes card index exists
        self.lst[idx-1].defn = new
    def move_card(self, old, new):
        item = self.lst.pop(old-1)
        self.lst.insert(new-1, item)

#### Function definitions

def main_menu():
    option = input("""- (N)ew stack
- (L)oad stack from file
- (Q)uit
Please select an option: """)[0].lower() # Tests the first letter of user input
    if option == 'n':
        flashcard_main(fstack(), " ") # If filename is ' ', then we know no file was loaded
    elif option == 'l':
        fname = input("Please input a file name: ")
        stack = load_stack(fname)
        flashcard_main(stack, fname)
    elif option == 'q':
        pass
    else:
        print("Invalid input.  Please try again.")
        main_menu()

def flashcard_main(stack, filename):
    optionlist = """- (V)iew cards
- (A)dd card
- (D)elete card
- (E)dit card
- (M)ove card
- (T)est yourself
- (S)ave cards
- (Q)uit"""
    print(optionlist)
    while True:
        option = input("Please select an option: ")[0].lower() # matching the first character
        if option == 'v':
            stack.view_stack()
        elif option == 'a':
            key = input("Input an item: ")
            value = input("Input an answer: ")
            stack.add_card(flashcard(key,value))
        elif option == 'd':
            idx = int(input("Which card do you want to delete?  Enter a card number: "))
            if idx <= stack.num_of_cards() and idx != 0:
                stack.remove_card(int(idx))
            else:
                print("Invalid card number!")
        elif option == 'e':
            idx = int(input("Which card do you want to edit?  Enter a card number: "))
            if idx <= stack.num_of_cards() and idx != 0:
                newstring = input("What should its new answer be? ")
                stack.edit_card(idx, newstring)
                card = stack.get_card(idx)
                print("Answer for '" + card.word + "' changed to '" + card.defn + "'")
            else:
                print("Invalid card number!")
        elif option == 'm':
            old = int(input("Which card number do you want to move? "))
            new = int(input("Where do you want to move it to? "))
            if old <= stack.num_of_cards() and old != 0 and new <= stack.num_of_cards() and new != 0:
                stack.move_card(old, new)
            else:
                print("Invalid card number!")
        elif option == 't':
            if stack.lst == []:
                print("Cannot test on empty deck!")
            else:
                test_stack(stack)
        elif option == 's':
            print("Saving file...")
            write_to_file(stack, filename)
        elif option == 'q': # not using the yes_or_no function because I want a default of yes
            if input("Do you want to save this deck? (y/n) ")[0].lower() == 'n':
                break
            else:
                print("Saving file...")
                write_to_file(stack, filename)
                break
        else:
            print(optionlist)

# Takes the name of a file and returns a stack
def load_stack(filename):
    stack = fstack()
    if not os.path.isfile(filename):
        print("Invalid file name.  Defaulting to empty flashcard stack.")
        return stack
    f = open(filename, 'r')
    for i,line in enumerate(f):
            pair = re.split('\t', line)
            if not pair[0][0] == '#':
                l = len(pair)
                if l > 1:
                    stack.add_card(flashcard(pair[0], pair[l-1].rstrip('\n')))
    f.close()
    return stack

# Writes a stack to a file, depending on whether we want the user to specify a file name
def write_to_file(stack, filename):
    if not filename == " ": # create a temporary file for safety
        shutil.copy2(filename, "tempfile.txt")
        write_stack(stack, filename)
        os.remove("tempfile.txt")
    else:
        fname = input("Which file do you want to save these flashcards as?")
        write_stack(stack, fname)

def write_stack(stack, filename):
    f = open(filename, 'w') # should erase everything inside the file
    for card in stack.lst:
        f.write(card.word + "\t" + card.defn + "\n")
    f.close()
    print("Done!")

def test_stack(stack):
    correct = 0
    testlist = stack.lst
    print(testlist)
    if yes_or_no("Do you want to be tested in a random order?"):
        random.shuffle(testlist)
    else:
        if yes_or_no("Do you want to be tested in alphabetical order?"):
            testlist = sorted(testlist, key=lambda stack: stack.word)
    if yes_or_no("Do you want to switch items and answers?"):
        switch = True
    else:
        switch = False
    print(testlist)
    for card in testlist:
        print(("Item" if switch else "Answer") + " for " + (card.defn if switch else card.word))
        userans = input()
        if userans == (card.word if switch else card.defn).lower():
            print("Correct!")
            correct += 1
        else:
            print("The correct " + ("item" if switch else "answer") + " was " + (card.word if switch else card.defn))
            if yes_or_no("Did you answer correctly?"):
                correct += 1
    print("You got " + str(correct) + " out of " + str(stack.num_of_cards()) + " correct, or " + str(round(100*correct/stack.num_of_cards())) + "%!")

# Returns True if yes, and False if no.  Any string not beginning with 'y' will be a no
def yes_or_no(string):
    option = input(string + " (y/n) ")
    if option == "":
        return False
    elif option[0].lower() == 'y':
        return True
    else:
        return False

#### Main execution

if len(sys.argv) == 1: # No command line arguments
    main_menu()
elif len(sys.argv) == 2: # The argument should be a file name
    fname = sys.argv[1]
    flashcard_main(load_stack(fname), fname)
else:
    print("usage: flashcards.py <optional stack file>")
