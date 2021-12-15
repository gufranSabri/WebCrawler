import os

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(dir_name+ " created\n")

def create_and_or_write(dir_name, file_name, open_type, data):
    f = open(dir_name + file_name, open_type)
    for i in data:f.write(i+"\n")

def file_to_list(dir_name, file_name, use_set):
    results = list()
    if use_set: results = set()
    with open(dir_name + file_name, 'rt') as f:
        for line in f:
            if use_set: results.add(line.replace('\n', ''))
            else: results.append(line.replace('\n', ''))
    return results

def set_to_file(dir_name, file_name, links):
    with open(dir_name + file_name,"w") as f:
        for l in links:f.write(l+"\n")