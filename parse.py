#! /usr/bin/env python3

import PyPDF2
import zipfile
import os
import re

# Helper methods

def load_field(reader, key):
    """
    Get a value from the pdf fillable fields or return None
    """
    fields = reader.getFields() # Hopefully shallow copy?
    if not fields:
        return None
    if key in fields:
        val = fields[key].value # In case we have bytes object
        if type(val) == PyPDF2.generic.ByteStringObject:
            val = val.decode("utf-8")
        val = val.replace("\n", " ")
        return val
    return None
    
# Classes

class Application():
    def __init__(self, file):
        reader = PyPDF2.PdfFileReader(file)
        self.club = load_field(reader, "ClubTeam Name")
        # Name is more complicated
        try:
            self.name = " ".join((load_field(reader, "First Name"), load_field(reader, "Last Name"),))
        except TypeError:
            self.name = ""
        self.email = load_field(reader, "UCalgary Email")
        self.activity = load_field(reader, "Activity Name")
         # TODO map these to the letter values if possible
        self.category = load_field(reader, "Type of Activity SELF Category")
        # TODO Improve date parsing
        self.start = load_field(reader, "Start Date of Activity") 
        self.end = load_field(reader, "End Date of Activity")
        self.location = load_field(reader, "Location of Activity")
        # This has a really messed up name
        self.description = load_field(reader, "Description of Activity 50100 wordsRow1")
    def to_string(self):
        """
        Print out so it is applicable to paste into a csv
        """
        return ", ".join(["\""+str(val)+"\"" for val in (self.club, self.name, self.email, self.activity, self.category, self.start, self.end, self.location)])

# Some procedural functions

def unzip(dir):
    """
    Recursively unzip the given folder
    """
    # First unzip all the zips
    for child in os.listdir(dir):
        child = os.path.join(dir, child) # Get the abs path back
        _, ext = os.path.splitext(child)
        if ext == ".zip":
            print("Unzipping to " + dir)
            with zipfile.ZipFile(child, "r") as zip_ref:
                zip_ref.extractall(dir)
    # unzip any zips in child dirs
    for child in os.listdir(dir):
        child = os.path.join(dir, child) # Abspath basically 
        if os.path.isdir(child):
            unzip(child)

def find_application(dir):
    """
    Tries to find the self application in a directory. If it it fails returns None
    """
    # First look in the top level
    pattern = f"SELF.*\.pdf" 
    contents = os.listdir(dir)
    apps = [os.path.join(dir,f) for f in contents if re.search(pattern, f)]
    # Now check children
    for child in os.listdir(dir):
        child = os.path.join(dir, child)
        if os.path.isdir(child):
            apps.extend(find_application(child))
    return apps

def interpret(dir, outfile):
    """
    Spits out a csv line for each application
    dir - parent folder containing all our applications
    """
    for child in os.listdir(dir):
        child = os.path.join(dir, child)
        if os.path.isdir(child):
            print(child)
            pdfs = find_application(child) # Get all the applications
            apps = [Application(pdf) for pdf in pdfs]
            for app in apps:
                outfile.write(app.to_string())
                outfile.write("\n")

def run_for_each(zipfolder : str, func):
    """
    Run `func` for each application found in `zipfolder`

    Args:
        zipfolder: path to parent folder of the root folder containing all
            applications
        func: funciton taking an application argument
    """
    parents = [os.path.join(zipfolder, x) for x in os.listdir(zipfolder)] # Get children
    parents = list(filter(os.path.isdir, parents)) # Get only dirs
    p = parents[0] # Assume there's only one valid dir. This is kinda bad but ok for now
    for child in os.listdir(p):
        child = os.path.join(p, child)
        if os.path.isdir(child):
            pdfs = find_application(child) # Get all the applications
            for pdf in pdfs:
                try:
                    app = Application(pdf)
                except:
                    print("Error reading file")
                func(app)

if __name__ == "__main__":
    # TODO Add parsing of the excel files to figure out the amount requested
    zipfolder = "/home/zachary/Desktop/ESS/SELF/March"
    children = [os.path.join(zipfolder, x) for x in os.listdir(zipfolder)] # Get children
    children = list(filter(os.path.isdir, children)) # Get only dirs
    child = children[0] # Assume there's only one valid dir. This is kinda bad but ok for now
    # unzip(zipfolder) # Uncomment if you need to unzip
    with open("output", "w") as outfile:
        interpret(child, outfile)
