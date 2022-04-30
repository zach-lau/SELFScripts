#! /usr/bin/env python3
"""
This file contains functions to grab the description of each event from the pdf
"""
from unicodedata import category
from parse import *

def print_description(app):
    print(f"""{app.activity}
    Category: {app.category}
    Club: {app.club}
    Start date: {app.start}
    End date: {app.end}
    Description: {app.description}
    """)

if __name__ == "__main__":
    # Assume that we have already performed the unzipping and we just need
    # to find the applications
    zipfolder = "/home/zachary/Desktop/ESS/SELF/Applications/Feb"
    run_for_each(zipfolder, print_description)
    