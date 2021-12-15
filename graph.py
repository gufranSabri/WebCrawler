
class Graph:
    adj_list = dict()
    nodes = list()

    def __init__(self, links):
        print("\nBuilding the graph...")
        for i in links:self.nodes.extend(i)
        
        self.nodes = list(set(self.nodes))
        self.nodes = dict(zip(self.nodes , range(len(self.nodes))))

        for i in links:
            neighbors = []
            l_neighbours = i[1:]

            for ln in l_neighbours:neighbors.append(self.nodes[ln])
            self.adj_list[self.nodes[i[0]]] = neighbors   
        print("Graph built\n")     
    
    def get_shortest_path(self, src, target):
        if src == target:
            print("Same urls!")
            return
        if src not in self.nodes:
            print("\n"+src+" doesn't exist in graph!")
            return
        if target not in self.nodes:
            print("\n"+target+" doesn't exist in graph!")
            return

        path_exists=False
        queue = []
        node_info = [{'visited':False, 'parent':None} for _ in range(len(self.nodes))]

        target_index = self.nodes[target]
        queue.append(self.nodes[src])
        node_info[self.nodes[src]]['visited']=True
        
        while len(queue)!=0:
            n = queue.pop(0)
            
            if n not in self.adj_list: continue
            for i in self.adj_list[n]:
                if not node_info[i]['visited']:
                    queue.append(i)
                    node_info[i]['visited']=True
                    node_info[i]['parent'] = n
                if i == target_index: 
                    path_exists=True
                    break
        
        if not path_exists: print("\nPath doesn't exist!")
        else:
            path=[target_index]
            print("\nShortest path:")
            while target_index != None:
                path.append(node_info[target_index]['parent'])
                target_index = node_info[target_index]['parent']
            
            path.pop()
            path.reverse()
            
            reversed_nodes = {value : key for (key, value) in self.nodes.items()}

            for i in path:print(reversed_nodes[i])