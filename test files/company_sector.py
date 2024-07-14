from random import choices
import random
import json
from collections import Counter
def item_picker(items, quantities, num_to_pick):
    return choices(items, weights=quantities, k=num_to_pick)


def item_picker1(items):
  return random.choice(items)
def selector():
    l=[]
    with open(r'D:\projects\ads_selector\sampling\sampling result\thomson_result.json', 'r') as csvfile:  # Replace with your CSV file name
        csv_reader = json.load(csvfile)
        for row in csv_reader:
            row.sort()
            ct=Counter(row)
            
            # print(ct)
            k=[]
            for key, value in ct.items():
                k.append(value)
            l.append(k)  # Prints each row as a list
    return l
# print(selector())

import os

# l=[]
#     import os
#     from collections import Counter
#     import json
#     with open(r'D:\projects\ads_selector\sampling\sampling result\thomson_result.json', 'r') as csvfile:  # Replace with your CSV file name
#         csv_reader = json.load(csvfile)
#         for row in csv_reader:
#             row.sort()
#             ct=Counter(row)
            
#             # print(ct)
#             k=[]
#             for key, value in ct.items():
#                 k.append(value)
#             l.append(k)
#             # Prints each row as a list
#     r=0
#     for i in os.listdir(r"D:\projects\ads_selector\static\uploads"):
#         at=ThomsonData(i,l[r])
#         r+=1
#         db.session.add(at)
#         db.session.commit()
def rename_file_and_remove_spaces(file_path):
    # Extract the directory and filename from the given file path
    directory, filename = os.path.split(file_path)

    # Remove spaces from the filename
    new_filename = filename.replace(" ", "_")

    # Create the new file path
    new_file_path = os.path.join(directory, new_filename)

    # Rename the file
    os.rename(file_path, new_file_path)
for i in os.listdir(r"D:\projects\ads_selector\static\uploads"):
    print(i)
#     for j in os.listdir("D:/projects/ads_selector/static/uploads/"+i):
#         rename_file_and_remove_spaces("D:/projects/ads_selector/static/uploads/"+i+"/"+j)
