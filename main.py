
from multithread_crawler import Crawler
from graph import *
import file_handler
import validators
import os

def create_new_corpus():
    name, url, path = '', '', ''
    no_of_pages_between_quit_prompt = -1

    while len(name)==0:name = input("Enter corpus name (recommended: seed name)> ")

    while True:
        url = input("Enter seed (starting url)> ")
        if not validators.url(url):print("Invalid url!")
        else: break
    
    try:
        no_of_pages_between_quit_prompt = int(input("Enter no of pages after which you are prompted to stop crawling (min:1, max:500)> "))
        no_of_pages_between_quit_prompt = max(no_of_pages_between_quit_prompt,1)
        no_of_pages_between_quit_prompt = min(no_of_pages_between_quit_prompt,500)
    except Exception as e:
        pass
        
    print("\nAfter visiting " + str(no_of_pages_between_quit_prompt)+" pages, you will be asked if you want to stop crawling\n")
    Crawler(path, name+"_seed", url, no_of_pages_between_quit_prompt)

def make_graph(seed_name):
    print("\nProcessing text files...")
    graph_skeleton_dirty = os.listdir(seed_name)
    graph_skeleton_clean=[]

    for i in graph_skeleton_dirty:
        try:
            int(i.replace(".txt", ""))
            graph_skeleton_clean.append(i)
        except Exception as e:
            pass
    
    links = []
    for i in graph_skeleton_clean:
        l = file_handler.file_to_list(seed_name,"\\"+i, False)
        links.append(l)

    print("Files processed\n")

    g = Graph(links)

    while True:
        print("\n 1. Get shortest path")
        print("-1. Go back\n")

        opt = int(input(">"))
        if opt == -1: return
        else:
            src, target = '', ''

            while True:
                src = input("\nEnter starting url> ")
                if not validators.url(src):print("Invalid url!")
                else: break
            
            while True:
                target = input("Enter end url> ")
                if not validators.url(target):print("Invalid url!")
                else: break
            
            g.get_shortest_path(src, target)
        
def operate_on_existing_corpus():
    print("\nCorpus Menu")
    for i in range(len(items)):print(" "+str(i+1)+". "+ items[i])
    print("-1. Go back\n")
    
    while True:
        try:
            c_option = int(input(">"))
            if c_option == -1:break

            print("\nChoose operation")
            print(" 1. Continue crawling")
            print(" 2. Make web graph")
            print("-1. Go back\n")

            o_option = int(input(">"))
            if o_option==-1: 
                operate_on_existing_corpus()
                break

            if o_option==1: 
                try:
                    no_of_pages_between_quit_prompt = int(input("Enter no of pages after which you are prompted to stop crawling (min:1, max:500)> "))
                    no_of_pages_between_quit_prompt = max(no_of_pages_between_quit_prompt,1)
                    no_of_pages_between_quit_prompt = min(no_of_pages_between_quit_prompt,500)
                except Exception as e:
                    pass

                print("\nAfter visiting " + str(no_of_pages_between_quit_prompt)+" pages, you will be asked if you want to stop crawling\n")
                print("Continuing crawl on "+ items[c_option-1]+" corpus")

                Crawler("", items[c_option-1], "", no_of_pages_between_quit_prompt)
                break
            if o_option==2:
                make_graph(items[c_option-1])
                break
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    print("Starting crawler...")

    options = ["A", "Q", "a", "q"]
    while True:
        items = [x for x in os.listdir() if "seed" in x]

        print("\nMenu")
        print("A. Create new corpus")
        if len(items) != 0:
            print("B. Operate on pre-existing corpus")
            options.extend(["B","b"])
        print("Q. Quit")
        
        option = ''
        while option not in options:
            option = input("Select option from menu> ")
        
        if option in ["A", "a"]: create_new_corpus()
        elif option in ["B", "b"]: operate_on_existing_corpus()
        else:
            print("\nGoodbye!")
            break