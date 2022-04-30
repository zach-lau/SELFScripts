#! /usr/bin/env python3

import PyPDF2
file = "SELF-A1-Application.pdf"

reader = PyPDF2.PdfFileReader(file)
print(reader.getFields().keys())
