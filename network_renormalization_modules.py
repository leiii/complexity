#Code source: http://www-levich.engr.ccny.cuny.edu/~hmakse/modules.py
#Comments:
#
#If you have any questions or find a bug write Hernan Rozenfeld an email at
#hernanrozenfeld at domain gmail with the usual "dot com" at the end.
# 
#Code in Python (written by Hernan Rozenfeld):
# 
#For this code to run you'll need to install Python (http://www.python.org)
#and Networkx (http://networkx.lanl.gov/).
# 
#File "modules.py" contains algorithms MEMB, CBB, and random covering for
#network renormalization.

from math import *
from networkx import *
import random
from copy import deepcopy
import os, sys
import time

# 分形小世界生长模型
def fractal_model(generation,m,x,e):
    """
    Returns the fractal model introduced by 
    Song, Havlin, Makse in Nature Physics 2, 275.
    generation = number of generations
    m = number of offspring per node
    x = number of connections between offsprings
    e = probability that hubs stay connected
    1-e = probability that x offsprings connect.
    If e=1 we are in MODE 1 (pure small-world).
    If e=0 we are in MODE 2 (pure fractal).
    """
    G=Graph()
    G.add_edge(0,1) #This is the seed for the network (generation 0)
    node_index = 2
    for n in range(1,generation+1):
        all_links = G.edges()
        while all_links:
            link = all_links.pop()
            new_nodes_a = range(node_index,node_index + m)
            #random.shuffle(new_nodes_a)
            node_index += m
            new_nodes_b = range(node_index,node_index + m)
            #random.shuffle(new_nodes_b)
            node_index += m
            G.add_edges_from([(link[0],node) for node in new_nodes_a])
            G.add_edges_from([(link[1],node) for node in new_nodes_b])
            repulsive_links = zip(new_nodes_a,new_nodes_b)
            G.add_edges_from([repulsive_links.pop() for i in range(x-1)])
            if random.random() > e:
                G.delete_edge(link)
                G.add_edge(repulsive_links.pop())
    return G

#盒子覆盖法1 CBB
def CBB(G,lb): #This is the compact box burning algorithm.
    """
    It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
    The box_id is the center of the box.
    The subgraphs may be disconnected.
    """    
    uncovered_nodes=G.nodes()
    uncovered_nodes = set(uncovered_nodes)
    covered_nodes = set([])
    boxes_subgraphs = {}
    adj = G.adj
    while uncovered_nodes:
        center = random.choice(list(uncovered_nodes))
        nodes_visited = {center:0}
        search_queue = [center]
        d = 1
        while len(search_queue) > 0 and d <= lb-1:
            next_depth = []
            extend = next_depth.extend
            for n in search_queue:
                l = [ i for i in adj[n].iterkeys() if i not in nodes_visited ]
                extend(l)
                for j in l: 
                    nodes_visited[j] = d
            search_queue = next_depth
            d += 1
        new_covered_nodes = set(nodes_visited.keys())
        new_covered_nodes = new_covered_nodes.difference(covered_nodes)
        nodes_checked_as_centers = set([center])
        while len(nodes_checked_as_centers) < len(new_covered_nodes):
            secondary_center = random.choice(list(new_covered_nodes.difference(nodes_checked_as_centers)))
            nodes_checked_as_centers.add(secondary_center)
            nodes_visited = {secondary_center:0}
            search_queue = [secondary_center]
            d = 1
            while len(search_queue) > 0 and d <= lb-1:
                next_depth = []
                extend = next_depth.extend
                for n in search_queue:
                    l = [ i for i in adj[n].iterkeys() if i not in nodes_visited ] # faster than has_key? yep
                    extend(l)
                    for j in l:
                        nodes_visited[j] = d
                search_queue = next_depth
                d += 1
            nodes_covered_by_secondary = set(nodes_visited.keys())
            new_covered_nodes = new_covered_nodes.intersection(nodes_covered_by_secondary)
        boxes_subgraphs[center] = subgraph(G,list(new_covered_nodes))
        uncovered_nodes = uncovered_nodes.difference(new_covered_nodes)
        covered_nodes = covered_nodes.union(new_covered_nodes)
    return boxes_subgraphs


#盒子覆盖法1 RBC
def random_box_covering(G,rb):
    """
    It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
    The box_id is the center of the box.
    """
    H = deepcopy(G)
    burned_nodes = []
    unburned_nodes = G.nodes()
    boxes_subgraphs = {}
    adj = H.adj
    while unburned_nodes:
        center_node = random.choice(unburned_nodes) 
        nodes_visited = [center_node]
        search_queue = [center_node]
        d = 1
        while search_queue and d <= rb:
            next_depth = []
            extend = next_depth.extend
            for n in search_queue:
                l = [ i for i in adj[n].iterkeys() if i not in nodes_visited]
                extend(l)
                nodes_visited.extend(l)
            search_queue = next_depth
            d += 1
        new_burned_nodes = nodes_visited#.keys()
        H.delete_nodes_from(new_burned_nodes)
        boxes_subgraphs[center_node] = subgraph(G,new_burned_nodes)
        unburned_nodes = list(set(unburned_nodes)-set(new_burned_nodes))
    return boxes_subgraphs


#盒子覆盖法1 MEMB
def MEMB(G,rb,cycle=0):
    """
    It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
    The box_id is the center of the box.
    cycle: Ignore this parameter. Use the default cycle=0.
    """
    adj = G.adj
    number_of_nodes = G.number_of_nodes()
    covered_nodes = set()
    center_nodes = set()
    non_center_nodes = G.nodes()
    center_node_found = 0
    boxes={} #this will be "box_id:[nodes in box]"
    central_distance_of_node = {} #"node:central_distance"
    node_box_id = {} #"node:box_id"
    nodes_sorted_by_central_distance={} #Dict with {central_distance:[nodes]}
    excluded_mass_of_non_centers_rb = {} #This contains [(node:excluded_mass)] for rb
    excluded_mass_of_non_centers_rb2 = {} #This contains [(node:excluded_mass)] for rb+1
    rb2 = rb + 1
    for node in non_center_nodes:
        #if node in [5000,10000,20000,30000]: print "node", node
        level=0                  # the current level
        nextlevel={node:1}       # list of nodes to check at next level
        paths_rb=None
        paths_rb2={node:[node]} # paths dictionary  (paths to key from source)
        while nextlevel:
            paths_rb = deepcopy(paths_rb2)
            thislevel=nextlevel
            nextlevel={}
            for v in thislevel:
                for w in G.neighbors(v):
                    if not paths_rb2.has_key(w):
                        paths_rb2[w]=paths_rb2[v]+[w]
                        nextlevel[w]=1
            level=level+1
            if (rb2 <= level):  break
        excluded_mass_of_node = len(paths_rb2)
        try:
            excluded_mass_of_non_centers_rb2[excluded_mass_of_node].append(node)
        except KeyError:
            excluded_mass_of_non_centers_rb2[excluded_mass_of_node] = [node]
        excluded_mass_of_node = len(paths_rb)
        try:
            excluded_mass_of_non_centers_rb[excluded_mass_of_node].append(node)
        except KeyError:
            excluded_mass_of_non_centers_rb[excluded_mass_of_node] = [node]
    maximum_excluded_mass = 0
    nodes_with_maximum_excluded_mass=[]
    new_covered_nodes = {}
    center_node_and_mass = []
    cycle_index = 0
    while len(covered_nodes) < number_of_nodes:
        #print len(covered_nodes),number_of_nodes
        cycle_index += 1
        if cycle_index == cycle:
            rb2 = rb+1
            cycle_index = 0
        else:
            rb2 = rb
        while 1:
            if rb2 == rb+1:
                #t1=time.time()
                while 1:
                    maximum_key = max(excluded_mass_of_non_centers_rb2.keys())
                    node = random.choice(excluded_mass_of_non_centers_rb2[maximum_key])
                    if node in center_nodes:
                        excluded_mass_of_non_centers_rb2[maximum_key].remove(node)
                        if not excluded_mass_of_non_centers_rb2[maximum_key]: del excluded_mass_of_non_centers_rb2[maximum_key]
                    else:
                        break    
                nodes_visited = {}
                bfs = single_source_shortest_path(G,node,cutoff=rb2)
                for i in bfs:
                    nodes_visited[i] = len(bfs[i])-1
                excluded_mass_of_node = len(set(nodes_visited.keys()).difference(covered_nodes))
                if excluded_mass_of_node == maximum_key:
                    center_node_and_mass = (node,maximum_key)
                    excluded_mass_of_non_centers_rb2[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb2[maximum_key]: del excluded_mass_of_non_centers_rb2[maximum_key]
                    new_covered_nodes = nodes_visited
                    break
                else:
                    excluded_mass_of_non_centers_rb2[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb2[maximum_key]: del excluded_mass_of_non_centers_rb2[maximum_key]
                    try:
                        excluded_mass_of_non_centers_rb2[excluded_mass_of_node].append(node)
                    except KeyError:
                        excluded_mass_of_non_centers_rb2[excluded_mass_of_node] = [node]
                #print "time", time.time()-t1
            else:
                #t1=time.time()
                while 1:
                    maximum_key = max(excluded_mass_of_non_centers_rb.keys())
                    node = random.choice(excluded_mass_of_non_centers_rb[maximum_key])
                    if node in center_nodes:
                        excluded_mass_of_non_centers_rb[maximum_key].remove(node)
                        if not excluded_mass_of_non_centers_rb[maximum_key]: del excluded_mass_of_non_centers_rb[maximum_key]
                    else:
                        break    
                nodes_visited = {}
                bfs = single_source_shortest_path(G,node,cutoff=rb)
                for i in bfs:
                    nodes_visited[i] = len(bfs[i])-1
                excluded_mass_of_node = len(set(nodes_visited.keys()).difference(covered_nodes))
                if excluded_mass_of_node == maximum_key:
                    center_node_and_mass = (node,maximum_key)
                    excluded_mass_of_non_centers_rb[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb[maximum_key]: del excluded_mass_of_non_centers_rb[maximum_key]
                    new_covered_nodes = nodes_visited
                    break
                else:
                    excluded_mass_of_non_centers_rb[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb[maximum_key]: del excluded_mass_of_non_centers_rb[maximum_key]
                    try:
                        excluded_mass_of_non_centers_rb[excluded_mass_of_node].append(node)
                    except KeyError:
                        excluded_mass_of_non_centers_rb[excluded_mass_of_node] = [node]
                #print "time", time.time()-t1
                    
        center_node_found = center_node_and_mass[0]
        boxes[center_node_found] = [center_node_found]
        node_box_id[center_node_found] = center_node_found
        non_center_nodes.remove(center_node_found)
        center_nodes.add(center_node_found)
        
        covered_nodes = covered_nodes.union(set(new_covered_nodes.keys()))
        #print len(covered_nodes)
        for i in new_covered_nodes:
            
            try:
                if central_distance_of_node[i] > new_covered_nodes[i]:
                    nodes_sorted_by_central_distance[central_distance_of_node[i]].remove(i)
                    if not nodes_sorted_by_central_distance[central_distance_of_node[i]]:
                        del nodes_sorted_by_central_distance[central_distance_of_node[i]]
                    try:
                        nodes_sorted_by_central_distance[new_covered_nodes[i]].append(i)
                    except KeyError:
                        nodes_sorted_by_central_distance[new_covered_nodes[i]] = [i]
                    central_distance_of_node[i] = new_covered_nodes[i]
            except KeyError:
                central_distance_of_node[i] = new_covered_nodes[i]
                try:
                    nodes_sorted_by_central_distance[new_covered_nodes[i]].append(i)
                except:
                    nodes_sorted_by_central_distance[new_covered_nodes[i]] = [i]

    max_distance = max(nodes_sorted_by_central_distance.keys())
    for i in range(1,max_distance+1):
        for j in nodes_sorted_by_central_distance[i]:
            targets = list(set(adj[j].iterkeys()).intersection(set(nodes_sorted_by_central_distance[i-1])))
            node_box_id[j] = node_box_id[random.choice(targets)]
            boxes[node_box_id[j]].append(j)
    boxes_subgraphs={}
    for i in boxes:
        boxes_subgraphs[i] = subgraph(G,boxes[i])
    
    return boxes_subgraphs

if __name__ == '__main__':
    g=fractal_model(3,2,2,0)
    boxes_subgraphs = MEMB(g,2)
    print boxes_subgraphs
