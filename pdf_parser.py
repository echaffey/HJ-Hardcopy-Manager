import re
import sqlite3

def parse(text):
    print(text)
    WJ_num = str(re.search(r'(WJ\d{8})', text).group(1))
    date = str(re.search(r'(\d{2}-[A-Z]{3}-\d{4})', text).group(1))
    WIP_due = str(re.search(r'(WIP DUE:/s*\d{2}-[A-Z]{3}-\d{4})', text).group(1))
    print(date)
