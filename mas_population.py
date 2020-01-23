#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

import mas_utils as u
import mas_environment as e
import mas as m
import mas_agent as a
import random
import copy

#==================================================
#  POPULATION
#==================================================

# --- Constants ---

LIST_AGENT_PRESENT_IDX = 0
ENV_IDX = 1
MAX_AGENT_CAPACITY_IDX = 2
MAX_IDX = 2

# --- Tools functions ---

def get_property(POP, idx):
    if not (0 <= idx <= MAX_IDX):
        raise Exception("Invalid AGENT property index.")
    return POP[idx]

def set_property ( POP, idx, value ) :
    if not (0 <= idx <= MAX_IDX):
        raise Exception("Invalid AGENT property index.")    
    POP[idx] = value

def empty_list():
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---



def get_agents(pop):
    """ Renvoie la liste d'agent """
    return get_property(pop, LIST_AGENT_PRESENT_IDX)    

def set_agents(pop, liste):
    set_property(pop, LIST_AGENT_PRESENT_IDX, liste)

def get_env(pop):
    """ Renvoie l'environnement de la population """
    return get_property(pop, ENV_IDX)

def set_env(pop, env):
    set_property(pop, ENV_IDX, env)

def get_max_agent_capacity(pop):
    return get_property(pop, MAX_AGENT_CAPACITY_IDX)

def set_max_agent_capacity (pop, cfg):                   
    set_property(pop,MAX_AGENT_CAPACITY_IDX, cfg)

def get_position_agent(pop, agent):
    res = 0
    liste = get_agents(pop)
    for i in range(len(liste)):
        if liste[i] == agent:
            res = i
        else:
            raise Exception("Invalid AGENT property position in the list of agent.")
    return res




# -----------------------------------------------------------

def new_instance(mas, size,cfg):
    pop = empty_list()
    set_agents(pop, [])                                           
    set_env(pop, m.get_env(mas))
    set_max_agent_capacity(pop, cfg["MAX_AGENT_CAPACITY"])
    MAX_AGENT_CAPACITY = cfg["MAX_AGENT_CAPACITY"]
    AGENT_PRESENT = int(cfg["INITIAL_AGENT"])
    init_agents(pop, AGENT_PRESENT,cfg)
    return pop

def init_agents(pop, nombre,cfg):
    liste = get_agents(pop)
    for i in range(nombre):
        new_agent = a.new_instance(cfg)
        while occupied_cell_agent(pop, new_agent):
            new_agent = a.new_instance(cfg)
        liste.append(new_agent)
        
        
"""def apply_rule(pop, cfg):
     Applique une agent_rule à toute la population 
    for agent in get_agents(pop):
        agent_rules(agent, mas, cfg)
"""


def apply_population_rules(mas,pop,cfg,matrix):
    liste = get_agents(pop)
    if cfg["RULE_POPULATION"] == 'default':
        for agent in liste:
            Default_move (agent,mas,cfg,matrix)
    if cfg["RULE_POPULATION"] == 'OA1':
        ls = copy.deepcopy(get_agents(m.get_pop(mas)))
        while not ls == [] :
            x = random.randint(0,len(ls)-1)
            agent = ls[x]
            del ls[x] 
            Default_move(agent, mas, cfg, matrix)
                  
    if cfg["RULE_POPULATION"] == 'OA2':
        ls = copy.deepcopy(get_agents(m.get_pop(mas)))
        while not ls == [] :
            res = 0
            agent1 = 0
            for i in range(len(ls)):
                if res<ls[i][2]:
                    res = ls[i][2]
                    agent1 = ls[i]
                    position = Default_move(agent1,mas,cfg,matrix)
                    a.set_pos(agent1,position)
            del ls[i]

def Default_move (agent,mas,cfg,matrix):           
    position = a.move_agent(agent, mas, cfg,matrix)                        
    if a.get_sugar_level == 0.0:
        kill_agent(pop,agent)
    return position

"""
            reproduction_asexual(pop, agent )                                             
            if occupied_cell_agent(pop,agent) == True :
                res = rule_rencontre(pop,cfg)
            else:
                res = False
"""                    
def occupied_cell_agent(pop, agent):
    """ booléen, pour savoir si il y a déjà un agent sur la cellule convoitée par l'agent """
    liste = get_agents(pop)
    res = False
    for i in range(len(liste)):
        if a.get_pos(liste[i]) == a.get_pos(agent):     
            res = True
    return res


def occupied_cell_position(pop,agent):
    """ donne quel positio de l'agent ( dans la liste ) est dejà sur la cellule  """
    liste = get_agents(POP)
    res = 0
    for i in range(len(liste)):
        if a.get_pos(liste[i]) == a.get_pos(agent):     
            res = i
    return res
      
    
def kill_agent(pop,agent) :
    ls = get_agents(pop)
    for i in range(len(ls)):
        if ls[i] == agent:
            res = i
    ls = get_agents(pop)
    del ls[i]
"""
def agent_combat(pop,agent1,agent2):
    x = random.randint(1,7)
    y = random.randint(1,7)
    position1 = get_position_agent(pop,agent1)
    position2 = get_position_agent (pop,agent2)
    if x == y:
        agent_combat(agent1,agent2)
    if x > y:
        kill_agent(pop, agent2)
    else:
        kill_agent(pop, agent1)


def rule_rencontre(pop, agent): 
    cfg = u.config_read_file("test.cfg")
    liste = get_agents(pop)
    matrix_copy = copy.deepcopy(e.get_cell_matrix(get_env(pop))
    if cfg["RULE_RENCONTRE"] == 'combat':
        position1 = occupied_cell_position(pop,agent)
        agent1 = liste[position1]
        agent_combat(agent1,agent)
        res = False
    if cfg["RULE_RENCONTRE"] == ' reproduction_sexuee ':
        position1 = occupied_cell_position(POP,agent)
        agent1 = liste[position1]
        reproduction_sexual (pop, agent1, agent)
        res = False
    else:
        agent1 = liste[occupied_cell_position(pop,agent)]                               
        position_matrix = agent1[get_position_agent(pop, agent)]
        lig, col = position1[0], position1[1]
        matrix_copy[lig][col] = 0
        a.move_agent(agent,matrix_copy)                            
        res = True
    return res  
        
"""

'''

def reproduction_asexual (pop, agent):
    x = random.randrange(20)
    if x == 10 : ## On crée une condition arbitraire
        liste = get_agents(pop)
        baby = agent
        i = 0
        while occupied_cell_agent(pop, baby ):
            baby_position = vector_sum((i,i ),( a.get_position(agent)))
            i += 1
        a.set_position(baby, baby_position)
        liste.append(baby)

def reproduction_sexual (pop, agent1, agent2 ):
    liste = get_agents(pop)
    x = random.randrange(2)
    y = (-1,-1)
    z = (1,1)
    if x == 0:
        baby = agent1 ## On prend les caractéristiques d'un des 2
    else :
        baby = agent2
    liste.append(baby)
    a.set_position(agent1, vector_sum(x, a.get_position(agent1)))
    a.set_position(agent2, vector_sum(y, a.get_position(agent2)))    
        
'''








    




