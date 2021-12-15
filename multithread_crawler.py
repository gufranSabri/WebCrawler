from urllib.request import urlopen
from html_parser import Parser
import file_handler
import threading
import keyboard
import time

class Crawler:
    CRAWLED_NAME, QUEUE_NAME = r"\crawled.txt", r"\queue.txt"
    MAX_NO_OF_THREADS = 8
    project_name, seed_url = '', ''
    crawled, queue = set(), set()
    page_count, file_name = 0, 0
    prompted = False
    print_error_messages = False

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
        
        self.file_name = len(self.crawled)

        self.work()
    
    def work(self):
        threads = []
        lock = threading.Lock()
        while not self.stop_crawling and len(self.queue)!=0:
            no_of_threads = min(self.no_of_pages_between_quit_prompt - (self.page_count%self.no_of_pages_between_quit_prompt), 
                self.MAX_NO_OF_THREADS) 
            no_of_threads = max(1, min(no_of_threads, len(self.queue)))
            
            for i in range(1,no_of_threads+1):
                t = threading.Thread(target=self.crawl, name="Thread "+str(i), args=(lock,))
                threads.append(t)
                t.start()
                
            for t in threads:t.join()

            print("\n------------------------------------------------------------------")
            print("Pages visited: "+ str(len(self.crawled)))
            print("Queue size: "+ str(len(self.queue)))
            print("------------------------------------------------------------------\n")

            if self.page_count % self.no_of_pages_between_quit_prompt == 0 and self.page_count!=0 and not self.prompted:
                self.prompt_stop_crawling()
            
            self.prompted = False
        
        if len(self.queue) == 0:
            print("Crawl Frontier empty")

    def crawl(self, lock):
        if len(self.queue)!=0 and not self.stop_crawling:
            html_string = ''

            lock.acquire()
            url = self.queue.pop()
            self.crawled.add(url)
            lock.release()
            try:
                print(threading.current_thread().name + " visiting "+ url)
                self.page_count+=1

                response = urlopen(url, timeout=10)
                if 'text/html' in response.getheader('Content-Type'):
                    html_string = response.read().decode("utf-8")
                    
                    parser = Parser(url)
                    parser.feed(html_string)

                    data = [url]
                    links = parser.page_links()
                    parser.page_links().remove(url)
                    data.extend(links)

                    lock.acquire()
                    self.file_name+=1
                    lock.release()
                    file_handler.create_and_or_write(self.project_name, r"\\" + str(self.file_name)+".txt", "w", data)

                    self.queue = self.queue.union(parser.page_links().difference(self.crawled))

            except Exception as e:
                if self.print_error_messages:
                    print("\n------------------------------------------------------------------")
                    print(str(e))
                    print("------------------------------------------------------------------\n")
    
    def prompt_stop_crawling(self):
        self.prompted = True

        print("\nPress 'q' to stop crawling")
        print("Press 'c' to keep crawling")
        opt = input(">")
        if opt in ["q", "Q"]:
            self.stop_crawling = True
            file_handler.set_to_file(self.project_name, self.CRAWLED_NAME, self.crawled)
            file_handler.set_to_file(self.project_name, self.QUEUE_NAME, self.queue)
        if opt in ["c", "C"]:self.prompted = self.stop_crawling = False