# solution to lab 2
# this is a reduction from hamiltonian cycle to the casting problem


# The input will be graph G = (V,E)

# The OUTPUT will be The first three lines of input consists of three integers, 
# one per line: n, s and k (number of roles, number of scenes and number of actors, n ≥ 2, s ≥ 1, k ≥ 2).
# The following n lines represent the constraints of type 1 and begin with an integer indicating the number of 
# subsequent integers on the line, followed by the numbers of the possible actors (between 1 and k, 
# in boldface in the examples below).
# The last s lines represent constraints of type 2. Each line begins with an integer indicating the number of subsequent 
# integers on the line, followed by integers representing the different roles playing in that scene. Each role appears 
# at most once in each row, so the number of roles is between 2 and n (1 is not possible since monologues are not allowed).  Every role plays in at least one of the s scenes.

# Question: Can the roles be cast using some or all of the given k actors so that p1 and p2 participate but not in the same scenes as each other?

# Input for graph coloring: 
# Row 1: Integer |V|<300 numb vertices
# Row 2: Integer |E|< 25000 numb edges
# Row 3: Integer 1<m <2^30 numb colors
# Followed by |E| rows of edge pairs (v,u)

# Input for casting problem:
# Row 1: Integer n number of roles
# Row 2: Integer s number of scenes
# Row 3: Integer k number of actors
# Followed by n rows of type 1 constraints (number of actors followed by actor numbers)
# Followed by s rows of type 2 constraints (number of roles followed by role numbers)

# ------------------------------------------------
# YES INSTANCE CONDITIONS
# p1 and p2 each have at least one role 1<=
# EVERY role has exactly 1 actor
# EVERY scene has at least 2 roles 
# EVERY scene has x roles then it has exactly x actors 
# EVERY scene can NOT have BOTH p1 and p2 playing 
# 
# ------------------------------------------------

def reduction():
    
    V = int(input()) 
    E = int(input()) 
    m = int(input())
    edge_list = []

    for _ in range(E):
        edge = input() # read in the edges, but we don't need to do anything with them
        edge = set([int(x) for x in edge.split()])
        edge_list.append(edge)
    
    # At MOST m colors... what is this concept related to in the casting problem
    # k actors are related to the vertices
    # n roles are related to the edges
    n = V+3
    s = E+2
    k = m+3
    # first 3 integers input n, s, k
    print(f"{n}\n{s}\n{k}")
    # type I constraint
    for i, v in enumerate(1, V+1):
        print(f"{m} ")
        # print all numbers 1 to m. Carbon copies of the entire actor set
        for j in range(1, m+1):
            print(f"{j}", end=" ")
    print(f"1 {m+1})") # p1 for role V+1
    print(f"1 {m+2}") # p2 for role V+2
    print(f"1 {m+3}") # dummy actor for role V+3

    # type II constraint each role is in at least one scene, and each scene has at least 2 roles.
    for i, e in enumerate(edge_list):
        print(f"{len(e)} {e[0]} {e[1]}")
    print(f"2 {V+1} {V+3}") # p1 and dummy actor in same scene
    print(f"2 {V+2} {V+3}") # p2 and dummy actor in same scene

def validate_casting_problem(Instance, Certificate):
    # certificate is a mapping of roles to actors
    # instance is the input to the casting problem
    n = Instance[0] # number of roles
    s = Instance[1] # number of scenes
    k = Instance[2] # number of actors
    type1_constraints = Instance[3:3+n] # type 1 constraints
    type2_constraints = Instance[3+n:3+n+s] # type 2 constraints



def reduction():
    V = int(input())
    E = int(input())
    m = int(input())

    edge_list = []
    isolated_vertices = {i for i in range(1, V + 1)} 
    for _ in range(E):
        edge = input() 
        edge = [int(x) for x in edge.split()]
        u, v = edge[0], edge[1]
        isolated_vertices.discard(u)
        isolated_vertices.discard(v)
        edge_list.append(edge)
    m = min(m, V)
    # add 3 extra dummy roles for p1,p2, and dummy actor "p3"
    n = V + 3
    # add 2 extra dummy scenes for p1 and p2 to be in seperate scenes and have p3 step in to that they are not monologues
    s = E + 2 + len(isolated_vertices)
    # add 2 extra dummy actors to substitute for divas p1, p2
    k = m + 3
    
    print(f"{n}")
    print(f"{s}")
    print(f"{k}")

    connected_actor_str = f"{m}"
    for j in range(3, m + 3):
        connected_actor_str += f" {j}"
    
    for i in range(1, V + 1):
        # print(f"{m} ", end="")
        # print entire actor list except the divas for each role. Matches the set up of the coloring problem since each vertex can be colored with any m of the colors
        print(connected_actor_str)

    print("1 1") # V+1 role gets actor p1
    print("1 2") # V+2 role gets actor p2
    print("1 3") # V+3 role gets dummy actor (p3)
    
    for edge in edge_list:
        u, v = edge[0], edge[1]
        print(f"2 {u} {v}")
    
    # the setup for the dummy scenes
    print(f"2 {V+1} {V+3}")
    print(f"2 {V+2} {V+3}")
    
    # just pair all the isolated vertices (i.e roles in scenes that are monologues) with dummy actor p3
    for v in isolated_vertices:
        print(f"2 {v} {V+1}")

if __name__ == "__main__":
    reduction()
