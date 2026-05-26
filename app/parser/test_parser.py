from parser import parse_file

sample = """
import sqlite3

def login():
    query = "SELECT * FROM users"
    print(query)
"""

result = parse_file("sample.py", sample, changed_lines=[4, 5, 6])
for fact in result:
    print(fact)