from urllib.request import urlopen
import file_handler
from html_parser import Parser
import keyboard
import time
import os

class Crawler:
    CRAWLED_NAME, QUEUE_NAME = r"\crawled.txt", r"\queue.txt"
    project_name = ''
    seed_url = ''
    crawled, queue = set(), set()

    def __init__(self, path, project_name, seed_url, no_of_pages_between_quit_prompt):
        self.project_name = path + project_name
        self.seed_url = seed_url
        self.stop_crawling = False
        self.no_of_pages_between_quit_prompt = no_of_pages_between_quit_prompt

        print("Initializing corpus...")
        file_handler.make_dir(self.project_name)
        file_handler.create_and_or_write(self.project_name, self.CRAWLED_NAME, "a", [])
        file_handler.create_and_or_write(self.project_name, self.QUEUE_NAME, "a", [])

        self.queue = file_handler.file_to_list(self.project_name, self.QUEUE_NAME, True)
        self.crawled = file_handler.file_to_list(self.project_name, self.CRAWLED_NAME, True)
        if len(self.queue) == 0: self.queue.add(seed_url)
        
        self.crawl(len(self.crawled))

    def crawl(self, start_file_num):
        count=0
        while len(self.queue)!=0 and not self.stop_crawling:
            html_string = ''
            url = self.queue.pop()
            try:
                print("\nVisiting "+ url)
                response = urlopen(url, timeout=10)
                
                if 'text/html' in response.getheader('Content-Type'):
                    html_string = response.read().decode("utf-8")
                    
                    parser = Parser(url)
                    parser.feed(html_string)

                    data = [url]
                    data.extend(parser.page_links())
                    file_handler.create_and_or_write(self.project_name, r"\\" + str(start_file_num)+".txt", "w", data)

                    self.crawled.add(url)
                    self.queue = self.queue.union(parser.page_links().difference(self.crawled))

                    start_file_num+=1
                    count+=1
                    if start_file_num!=0:
                        print("Queue size: "+ str(len(self.queue)))
                        print("Pages visited: "+ str(len(self.crawled)))

                    if count % self.no_of_pages_between_quit_prompt == 0:
                        self.prompt_stop_crawling()

            except Exception as e:
                print("\n"+str(e))
                print("Error: Cannot visit page\n")
    
    def prompt_stop_crawling(self):
        print("\nPress 'q' to stop crawling")
        print("Press 'c' to keep crawling")
        opt = input(">")
        
        if opt in ["q", "Q"]:
            self.stop_crawling = True
            file_handler.set_to_file(self.project_name, self.CRAWLED_NAME, self.crawled)
            file_handler.set_to_file(self.project_name, self.QUEUE_NAME, self.queue)
        if opt in ["c", "C"]:
            self.stop_crawling = False
        print()