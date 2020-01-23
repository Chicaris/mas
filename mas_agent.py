#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

import mas_population as p
import mas_environment as e
import mas as m
import mas_cell as c
import mas_utils as u
import random
import copy

#==================================================
#  AGENT
#==================================================

# --- Constants ---

VISION_IDX = 0
MAX_SUGAR_CAPACITY_IDX = 1
SUGAR_LEVEL_IDX = 2
POSITION_IDX = 3
MEMORY_IDX = 4
METABOLISM_IDX = 5
MAX_IDX = 5

# --- Tools functions ---

def get_property ( agent, idx ) :
    if not (0 <= idx <= MAX_IDX):
        raise Exception("Invalid AGENT property index.")
    return agent[idx]

def set_property ( agent, idx, value ) :
    if not (0 <= idx <= MAX_IDX):
        raise Exception("Invalid AGENT property index.")    
    agent[idx] = value

def empty_list():
    return [None]*(MAX_IDX+1) ## longueur de la liste

# --- Getters and setters ---

def get_vision(agent):
    return get_property(agent,VISION_IDX)

def set_vision(agent, vision ):
    set_property(agent, VISION_IDX, vision) ## change avec la nouvelle vision donnée en paramètre

def get_max_sugar_capacity ( agent ) :
    return get_property(agent, MAX_SUGAR_CAPACITY_IDX )

def set_max_sugar_capacity ( agent, max_sugar_capacity ) :
    set_property(agent, MAX_SUGAR_CAPACITY_IDX, max_sugar_capacity )

def get_sugar_level ( agent ) :
    return get_property ( agent, SUGAR_LEVEL_IDX )

def set_sugar_level ( agent, sugar_level ) :
    set_property(agent, SUGAR_LEVEL_IDX, sugar_level )
    
def get_memory(agent):
    return get_property(agent, MEMORY_IDX)

def set_memory(agent, memory):
    set_property(agent, MEMORY_IDX, memory)
    
def set_pos( agent, position ) :
    set_property(agent, POSITION_IDX, position )

def get_pos(agent):
    """ Renvoie la position de l'agent """
    return get_property(agent, POSITION_IDX)

def get_metabolism(agent):
    return get_property(agent,METABOLISM_IDX)

def set_metabolism(agent, metabolism):
    set_property(agent, METABOLISM_IDX,metabolism)
    
def get_is_living(agent):
    return True    

# --- Initialisation ---

def new_instance(cfg):
    agent = empty_list()
    size = cfg["ENV_SIZE"]
    #Vision
    vision =  random.randint(1, int(cfg["AGENT_VISION"]))
    set_vision(agent,vision)
    #Sucre maximal
    max_sugar_capacity = int(cfg["MAX_SUGAR_CAPACITY_AGENT"])
    set_max_sugar_capacity(agent,max_sugar_capacity )
    #Initial sugar   
    sugar_level = int(cfg["INITIAL_SUGAR_LEVEL"])
    set_sugar_level(agent, sugar_level )
    #Initial position
    initial_position =(random.randint(0,int(size)-1),random.randint(0,int(size)-1))
    set_pos(agent, initial_position)
    #Memory
    memory = (0,0)
    set_memory(agent, memory)
    #Métabolism
    set_metabolism(agent, float(cfg["METABOLISM"]))
    return agent


# --- Rules ---

def move_agent (agent,mas,cfg,matrix) :
    pop = m.get_pop(mas)
    matrix = e.get_cell_matrix(m.get_env(mas))
    size = len(matrix)
    if cfg["RULE_AGENT"] == 'default':
        new_position = agent_move_to_random_position(mas,agent,size, cfg)
        (col,lig) = new_position
        set_pos(agent, new_position)
        set_sugar_level(agent, float(get_sugar_level(agent))-float(get_metabolism(agent)))
        new_sugar_agent,new_sugar_cell = eat_sugar(agent,mas)
        set_sugar_level(agent,new_sugar_agent)
        matrix[lig][col][1] = new_sugar_cell
    if cfg["RULE_AGENT"] == 'RA1':
        new_position = RA1(mas,agent,matrix)        
    if cfg["RULE_AGENT"] == 'RA2':        
        new_position = RA2(mas, agent,matrix)        
    if cfg["RULE_AGENT"] == 'RA3':
        new_position = RA3(mas, agent )
    if cfg["RULE_AGENT"] == None:
        raise Exception('Invalid syntax for the moving rules')   
    return new_position

def agent_move_to_random_position(mas,agent,size,cfg):
    pop = m.get_pop(mas)
    return (random.randint(1,int(size)-1),random.randint(1,int(size)-1))
    
    
def eat_sugar(agent,mas):
    matrix = e.get_cell_matrix(m.get_env(mas))
    pop = m.get_pop(mas)
    (col,lig) = get_pos(agent)
    vision = get_vision(agent)
    sugar_agent = get_sugar_level(agent)
    max_sugar_agent = get_max_sugar_capacity(agent)
    sugar_cell = c.get_sugar_level(matrix[lig][col])
    new_sugar_agent = 0.0
    new_sugar_cell = 0.0

    if sugar_agent == max_sugar_agent:
        new_sugar_agent = max_sugar_agent
        new_sugar_cell = sugar_cell

    if sugar_agent < max_sugar_agent:
        if sugar_agent+sugar_cell < max_sugar_agent:
            new_sugar_agent = sugar_agent+sugar_cell
            new_sugar_cell = 0.0
                        
        if sugar_agent+sugar_cell>max_sugar_agent:
            new_sugar_agent = max_sugar_agent
            new_sugar_cell = sugar_cell + (sugar_agent - max_sugar_agent)
            
    c.set_sugar_level(matrix[lig][col],new_sugar_cell)
    return new_sugar_agent,new_sugar_cell


def RA1(mas,agent,matrix):
    pop = m.get_pop(mas)
    position = get_pos(agent)
    vision = get_vision(agent)
    idx_position = position
    res = 0
    while vision > 0:
        a,z = horizontal1(matrix,vision,res,idx_position,position)
        b,y = horizontal2(matrix,vision,res,idx_position,position)
        c,x = vertical1(matrix,vision,res,idx_position,position)
        d,w = vertical2(matrix,vision,res,idx_position,position)
        res = max(a,b,c,d)
        if res == a:
            idx_position = z
        elif res == b:
            idx_position = y
        elif res == c:
            idx_position = x
        elif res == d:
            idx_position = w
        else:
            p.kill_agent(pop,agent)
        vision -=1
    (col,lig) = idx_position    
    set_pos(agent, idx_position)
    set_sugar_level(agent, float(get_sugar_level(agent))-float(get_metabolism(agent)))
    new_sugar_agent,new_sugar_cell = eat_sugar(agent,mas)
    set_sugar_level(agent,new_sugar_agent)
    matrix[lig][col][1] = new_sugar_cell
    return idx_position

        
def horizontal1(matrix,i,res,idx_position,position):
    size = len(matrix)
    lig,col = int(position[0]),int(position[1])
    if res < matrix[lig][((col+i)%size)][1]:
            res = matrix[lig][int((col+i)%size)][1]            
            idx_position = (lig,(col+i)%size)
    return res,idx_position
            
def horizontal2(matrix,i,res,idx_position,position):
    size = len(matrix)
    lig,col = int(position[0]),int(position[1])
    if res < matrix[int((lig+i)%size)][col][1]:
            res = matrix[int((lig+i)%size)][col][1]
            idx_position = ((lig+i)%size,col)
    return res,idx_position

def vertical1(matrix,i,res,idx_position,position):
    size = len(matrix)
    lig,col = int(position[0]),int(position[1])
    if res < matrix[lig][int(((col-i)%size))][1]:
            res = matrix[lig][int(((col-i)%size))][1]
            idx_position = (lig,((col-i)%size))
    return res,idx_position

def vertical2(matrix,i,res,idx_position,position):
    size = len(matrix)
    lig,col = int(position[0]),int(position[1])
    if res < matrix[int(((lig-i)%size))][col][1]:
            res = matrix[int(((lig-i)%size))][col][1]
            idx_position = (((lig-i)%size),col)
    return res,idx_position



def RA2(mas, agent,matrix):
    memory = RA1(mas, agent,matrix )
    set_memory(agent, memory)
    position_actuelle = get_pos(agent)
    deplacement = (position[0]-memory[0],position[1]-memory[1])
    if deplacement == (0,0):
        agent_kill(mas,agent_ref)
    else:
        if deplacement[0]==0:
            if deplacement[1]>0:
                new_position = (position[0],position[1]+1)
                deplacement[1]-=1
            else:
                new_position = (position[0], position[1]-1)
                deplacement[1]+=1
        if deplacement[1]==0:
            if deplacement[0]>0:
                new_position = (position[0]+1,position[1])
                deplacement[0]+=1
            else:
                new_position = (position[0]-1,position[1])
                deplacement[0]-=1        

def RA3(mas, agent):
    (lig, col ) = get_pos(agent)
    matrix = e.get_cell_matrix( m.get_env(mas) )
    vision = get_vision(agent)
    res = 0 
    size = len(matrix)-1
    idx_position = (lig,col)
    metabolism = get_metabolism(agent)
    for i in range(vision+1):
        distance = vision-i
        if col+i > size:
            for j in range (distance):
                if metabolism <= res < matrix[lig][j][1]:    ##cellule[1] = taux de sucres
                    res = matrix[lig][j][1]
                    idx_position = (lig, j)
                                
        if lig+i > size:
            for j in range(distance):
                if metabolism <= res < matrix[j][col][1]:
                    res = matrix[j][col][1]
                    idx_position = (j,col)
        if col-i<0:
            for j in range(distance):
                if metabolism <= res < matrix[lig][size-j][1]:
                    res = matrix[lig][size-j][1]
                    idx_position = (lig, size-j )
        if lig-i<0:
            for j in range(distance):
                if metabolism <= res < matrix[size-j][col][1]:
                    res = matrix[size-j][col][1]
                    idx_position = (size-j, col )
        else:    
            if metabolism <= res < matrix[lig][col+i][1]:
                res = matrix[lig][col+i][1]
                idx_position = ( lig, col+i )
            if metabolism <= res < matrix[lig][col-i][1]:
                res = matrix[lig][col-i][1]
                idx_position = ( lig, col-i)
            if metabolism <= res < matrix[lig+i][col][1]:
                res = matrix[lig+i][col]
                idx_position = (lig+i, col)
            elif metabolism <= res < matrix[lig-i][col]:
                res = matrix[lig-i][col]
                idx_position = ( lig-i, col)
        return idx_position

def RA4(mas, agent):
    pass




















    
