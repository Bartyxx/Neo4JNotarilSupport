"""
-------------------------------------------------------------------------------
                                  main.py
-------------------------------------------------------------------------------
Notaril support project in python&neo4j.
Connect to a Neo4j database and execute a series of operations for control
the status of the ineritance of the famili's goods.
"""
from neo4j import GraphDatabase

class Connection:
    def __init__(self, neo4j_uri, neo4j_username, neo4j_password):
        """
        Parameters
        ----------
        neo4j_uri : STR
            Databse uri.
        neo4j_username : STR
            Username for access the database.
        neo4j_password : STR
            Password of the database.

        Returns
        -------
        Connection or disconnection to the database.
        """
        
        print(f"Connecting to the database {neo4j_uri}....")
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, \
                                                            neo4j_password))
        print(f"Connect to the database {neo4j_uri}.")

    def close(self):
        if self.driver:
            self.driver.close()
            print(f"Disconnect to the database {self.driver}.")

# ============================================================================
def menu(connection:Connection):
    """
        Parameters
    ----------
    connection : Connection
        Class connection with the connection instruction.

    Returns
    -------
    None.
    """
    
    driver = connection.driver
    isfromc = False
    while True:
        print("=" * 100 + "\n"
              'Menu\n\t'
              'Welcome to the notarial support. Please choose an option:\n\t'
              '- Show the property of a living person.                                 - a\n\t'
              '- Show the nearest living relative of a person.                         - b\n\t'
              '- Show the new property considering the departure of a person.          - c\n\t'
              '- Exit                                                                  - every other key\n'
              + "=" * 100)
        try:
            guess = str(input('Your choice: > '))
            break
        except Exception as e:
            print(f'Something went wrong:{e}')
    if guess.lower() == 'a':
        possessions(connection)
    elif guess.lower() == 'b':
        relatives("", isfromc)
    elif guess.lower() == 'c':
        departure()
    else:
        print('Thank for choosing us!')
        driver.close()

# ============================================================================
def possessions(connect:Connection):
    """
        Parameters
    ----------
    connection : Connection
        Class connection with the connection instruction.

    Returns
    -------
    None
    """
    
    driver = connect.driver
    session = driver.session()
    
    person, counter, iterable_result, i, result = initialize_id()
    control_id(person, counter)            

    query_string = 'MATCH(p:p{id:"' + i[0] + '"})-[r: Owns]->(a) return a.name, a.value, r.value'
    query = session.run(query_string)
    query_iterable = iter(query)
    
    printobj = list()
    for item in query_iterable:
        printobj.append(item)
        
    if len(printobj):
        print(f'\n Items possessed by {i[1]} {i[2]}:\n')
        print("=" * 100 + "\n")
        for item in printobj:
             print(f'--------------------------------------\n'
                   f'Item name: {item["a.name"]}\n'
                   f'--------------------------------------\n'
                   f'Value of the item: {item["a.value"]}€\n'
                   f'Percentage of item possession: {item["r.value"]}\n'
                   f'Calculated value:{item["a.value"]/100*item["r.value"]}\n')
    else:
        print(f'--------------------------------------\n'
              f"{i[1]} {i[2]} don't have any items\n"
              f'--------------------------------------\n')
    
    final_control()
        
        
# ============================================================================
def relatives(person_fromc, isfromc):
    """
        Parameters
    ----------
    person_fromc : STR
        Always ""
    isfromc : BOOLEAN
        FALSE : Function called in the menu.
        TRUE  : Function called in departure function.

    Returns
    -------
    list_heirs : LIST
        List of the heirs of person.

        
    Shows the nearest living relatives of the person. These relatives are the 
    ones who will inherit the goods if the person passes away.
    Used in the departure function to identify the nearest living heirs. 
           
    """
        
    if isfromc == False:
        person, counter, iterable_result, i, result = initialize_id()
        control_id(person, counter)
        printv = True
    else: 
        person = person_fromc
        counter, iterable_result, i, result = initialize_id_c(person)
        control_id(person, counter)
        printv = False
        
    # Returns the name and surname of the consort
    query_consort = "MATCH (p:p{id:'"+ str(person)+"'})-[:SposatoCon]-(a) RETURN a.name, a.surname, p.name"
    # Returns the name, surname, and ID of all the sons
    query_sons = "MATCH (p:p{id:'"+ str(person)+"'})-[:Generate]->(a) RETURN a.name, a.surname, a.id, p.name"
    # Returns the name, surname, and ID of the parents
    query_parbro = "MATCH(p:p{id:'" + str(person)+"'})<-[:Generate]-(a:p)-[:Generate]->(b:p) RETURN a.name, a.surname, a.id, p.name,b.name, b.surname, b.id"
    
    control = "consort"
    heirs = function_heirs(query_consort)
 
    if len(heirs):
        if printv == True:
            print(f"If {i[1]} where to be missing the good will go to "
                  f'{heirs[0][0]} {heirs[0][1]}, the consort.')
        list_heirs = to_list(heirs, control, i)
    else:
        if printv == True:
            print(f"{i[1]} don't have a consort!")
        control = "sons"
        heirs = function_heirs(query_sons)
        list_heirs = to_list(heirs, control, i)
            
        if len(heirs):
            if printv == True:
                print(f"If {i[1]} where to be missing is good will go to "
                      f"his son/s: ")
            try:
                for i in heirs:
                    if printv == True:
                        print(f"-----> {i['a.name']}")
            except KeyError:
                print("")
        else:
            if printv == True:
                print(f"{i[1]} don't have sons!")
            control = "parbro"
            heirs = function_heirs(query_parbro)
            list_heirs = to_list(heirs, control, i)
            if len(heirs):
                if printv == True:
                    print(f"If {i[1]} where to be missing is good will go to " 
                          f"parents and siblings: "
                          f'{"=" * 100}')
                prec_gen=None
                prec_sons=None   
                try:
                    for i in heirs:
                        if i['a.name']!=prec_gen:
                            if printv == True:
                                print(f"--parent--> {i['a.name']}")
                            prec_gen = i['a.name']
                        if i['b.name']!=prec_sons:
                            if printv == True:
                                print(f"--siblings--> {i['b.name']}")
                            prec_sons = i['b.name']
                except KeyError:
                    print("")
            else:
                if printv == True:
                    print(f"{i[1]} don't have parents or brothers so \
                          is good will pass to the State ")
    if printv == True:
        final_control()
    return list_heirs
    
# ============================================================================
def departure():
    """
    
    Calculates the heirs in case of the departure of a person.
    The succession rules are the same as in the parents function, so the 
    parents function is called to determine the heirs, and the variable isfromc
    is passed.
    The cypher query returns the name, code, and value of the goods 
    (a.name, a.code, 
    a.value), the value in percentage of the goods (r.value), and the name of 
    the interested person (p.name).
    
    If a person doesn't have any heirs, then the goods are assigned to 
    the State.

    
    """
    
    driver = connect.driver
    session = driver.session()

    person, counter, iterable_result, i, result = initialize_id()
    control_id(person, counter)
    
    query_string = f'MATCH(p:p {{id:"{i[0]}"}})-[r:Owns]->(a) RETURN a.name, a.code, a.value, r.value, p.name'
    result_possession = session.run(query_string)
    possessions = list(result_possession)

    if possessions:
        isfromc = True
        heirs = relatives(person, isfromc)
        if heirs:
            for items in possessions:
                percent_own_ereditors = round(items['r.value'] / len(heirs), 2)
                try:
                    for heir in heirs:
                        query = """
                        CREATE (a:p {id: $heirs_id})-[:Possiede {value: $percent_own_ereditors}]->(b:b {code: $items_code})
                        """
                        session.run(query, heirs_id=heir['id'], percent_own_ereditors=percent_own_ereditors, items_code=items['a.code'])
                        print(f"The goods {items['a.name']} will be inherited " 
                              f"by {heir['name']} {heir['surname']} for the " 
                              f"{round(percent_own_ereditors, 2)}% of "
                              f"its value, so {round(items['a.value'] * percent_own_ereditors / 100, 2)}€")
                except KeyError:
                    print("KeyError encountered.")
        else:
            print(f"{i['p.name']} did not have any heirs, the goods will go to the State")
            for items in possessions:
                query = """
                CREATE (s:country {name: 'Italy'})-[:Owns {value: $value}]->(b:b {code: $items_code})
                """
                session.run(query, value=items['r.value'], items_code=items['a.code'])
                print(
                    f"The goods {items['a.name']} will be inherited by the Italian "
                    f"State, for the {items['r.value']}% corresponding to, "
                    f"{items['a.value']}€")
    else:
        print(f"{i['p.name']} didn't have any goods")

# ============================================================================
def arrange_query_person(a: iter) -> dict:
    """
        Parameters
    ----------
    a : iter : NEO4J
        Result of a Neo4j query

    Returns
    -------
    l : DICTIONARY
     Transform the Neo4j object in a dictionary.  
    
    Given a Neo4j object, it returns a dict.
    """
    
    l = {}
    c = 0
    print(a)
    for line in a:
        l['p' + str(c)] = {'name': line['p.name'], 'surname': line['p.surname'], 'id': line['p.id'],'età':['p.age']}
        c += 1
    return l

# ============================================================================
def control_id(person, counter):
    """
        Parameters
    ----------
    person : STR
        Id of the person
    counter : BOOLEAN
        0 = No person with this id is alive.
        1 = A person with this id is alive.
        
    Returns
    -------
    ERROR
        If the id is wrong or the person is death returns error.

        
    In case of an error, it gives the user the option to exit the program or 
    return to the menu.   
    """
    
    if len(person) != 16:
        print("The id must be of length 16.")
        error = True
    elif counter == 0:
        print("There are no alive person with this id in our databases.")
        error = True
    elif counter > 1:
        print("There are more person with the same id in our databases!")
        print("There have been some mistake, the id should be unique!")
        error = True

    try:
        error
    except NameError:
        error = False
        
    if error == True:
        print('Press 1 if you want to go to the menu\nEvery other key to exit')
        try:
            guess=str(input('_'))
        except Exception as e:
            print(f'Something went wrong: {e}')
        if guess=='1':
            menu(connect)
        else:
            return 
    return 

# ============================================================================
def initialize_id():
    """
    
    This function is used in the three main functions for asking the ID.
    After the insertion of the ID, it is checked with the control_id function.
    
    Returns
    -------
        - id               -> ID inserted.
        - counter          -> In case there is more than one person with the 
                              same ID.
        - iterable_results -> The iteration of the query.
        - i                -> The last value in iterable_results; if the query
                              is empty, i is assigned to 0.
        - result           -> The cypher query.

    
    """
    
    driver = connect.driver
    session = driver.session()
    try:
        person = str(input('Insert the id\n> '))
    except Exception as e:
        print(f'Something went wrong: {e}')
    
    session = driver.session()
    result = session.run("match (p:p{id:'"+str(person)+"',status:'alive'})\
                         return p.id,p.name,p.surname,p.status,p.age")
    iterable_result = iter(result)
    counter = 0
    
    for i in iterable_result:
        counter += 1
    
    try:
        i
    except NameError:
        i = 0
        
    return person, counter, iterable_result, i, result
  
# ============================================================================      
def initialize_id_c(person):
    """
    Parameters
    ----------
    person : STR
        Id of the person.

    Returns
    -------
        - counter          -> In case there is more than one person with the 
                              same ID.
        - iterable_results -> The iteration of the query.
        - i                -> The last value in iterable_results; if the query
                              is empty, i is assigned to 0.
        - result           -> The cypher query.
        
    Similar to the initialize_id function but does not return the person.

    """
    
    driver = connect.driver
    session = driver.session()
    
    session = driver.session()
    result = session.run("match (p:p{id:'"+str(person)+"',status:'alive'})\
                         return p.id,p.name,p.surname,p.status,p.age")
    iterable_result = iter(result)
    counter = 0
    
    for i in iterable_result:
        counter+=1
    try:
        i
    except NameError:
        i = 0
        
    return counter, iterable_result, i, result

# ============================================================================
def function_heirs(query):
    """
    Parameters
    ----------
    query : QUERY
        Neo4J query.

    Returns
    -------
    listheirs : LIST
        List of heirs of the person.
    
    It is used in the relatives function to iterate through the list of heirs.



    """
    
    driver = connect.driver
    session = driver.session()
    
    heirs = session.run(query)
    iterable_heirs = iter(heirs)
    
    listheirs = list()
    for i in iterable_heirs:
        listheirs.append(i)
    return listheirs

# ============================================================================
def to_list(f_heirs, control, i):
    """
    Parameters
    ----------
    f_heirs : LIST
        The list containing the heirs, transformed from a Neo4j object to a 
        list in the function_heirs function.
    control : STR
        A string indicating the type of control being checked, which can be 
        consort, sons, or parbro.
    i : INT
        The current value of the iteration in iterable_result in the 
        initialize_id function.
    
    Returns
    -------
    list_heirs : LIST
        List with the heirs.
    """    

    if control == "consort":
        iterable_heirs = iter(f_heirs)
        consort = list()
        for i in iterable_heirs:
            consort.append(i)
    if control == "sons":
        iterable_heirs = iter(f_heirs)
        sons = []
        for i in iterable_heirs:
            sons.append(i)
    if control == "parbro":
        iterable_heirs = iter(f_heirs)
        parbro = list()
        for i in iterable_heirs:
            parbro.append(i)
        
    heirs = list()
    if control == "consort":
        for i in consort:
            heirs.append({'name': i[0], 'surname': i[1], 'relationship': 'spouse'})
    if control == "sons":
        for i in sons:
            heirs.append({'name': i[0], 'surname': i[1], 'id': i[2], 'relationship': 'son/daughter'})
    if control == "parbro":
        prec_gen = None
        prec_bro = None
        for i in parbro:
            if i['a.name'] != prec_gen:
                heirs.append({'name': i['a.name'], 'surname': i['a.surname'], 'id': i['a.id'], 'relationship': 'parent'})
                prec_gen = i['a.name']
            if i['b.name'] != prec_bro:
                heirs.append({'name': i['b.name'], 'surname': i['b.surname'], 'id': i['b.id'],'relationship': 'brother/sister'})
                prec_bro = i['b.name']
    list_heirs = list(heirs)
    return list_heirs

# ============================================================================
def final_control():
    """
    The final message of the program: if '0' the program returns to the menu; 
    if any other key is pressed, the program exits.
    """
    
    print("\t")
    print("=" * 100)
    print("Press 0 for exit or every other key to reach the menu")
    
    try:
        guess = str(input(' >'))
    except Exception as e:
        print(f'Something went wrong: {e}')
    if guess!= "0":
        menu(connect)
    


if __name__ == '__main__':
    neo4j_uri = "bolt://localhost:7687"
    neo4j_username = "neo4j"
    neo4j_password = "AlfaAlfa"
    connect=Connection(neo4j_uri,neo4j_username,neo4j_password)
    menu(connect)

    """
    Usefoul command for delete a database:
    // Cancella tutte le relazioni
    MATCH ()-[r]->()
    DELETE r;

    // Cancella tutti i nodi
    MATCH (n)
    DELETE n;
    """