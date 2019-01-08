import mysql.connector
from mysql.connector import errorcode
from code import tokens

"""Funtion definition"""

def create_database():
    cursor = cnx.cursor()
    DB_NAME = 'RockPaperScissor$Players'
    try:
        cursor.execute("CREATE DATABASE {} ".format(DB_NAME))
    except mysql.connector.Error as err:
        print("[LOG-DB] Failed creating database: {}".format(err))
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("[LOG-DB] Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
            print("[LOG-DB] Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)

def connect_to_db(connection_config):
    global cursor
    try:
        cnx = mysql.connector.connect(**connection_config)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[LOG-DB] Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[LOG-DB] Database does not exist")
        else:
            print(err)
    else:
        return cnx

def create_tables():
    for table_name in db_tables:
        table_description = db_tables[table_name]
        try:
            print("[LOG-DB] Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

def create_player(facebook_id, first_name=None, last_name=None, gender=None):
    try:
        add_player = ("INSERT INTO players "
                        "(facebook_id, first_name, last_name, gender, times_played, times_won, times_drew, times_lost) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        times_played = 0
        times_won = 0
        times_drew = 0
        times_lost = 0
        data_player = (facebook_id, first_name, last_name, gender,times_played, times_won, times_drew, times_lost)
        cursor.execute(add_player, data_player)
        cnx.commit()
        print ('[LOG-DB] Added user {} using the following data: {}, {}, {}, {}, {}, {}, {}'.format(*data_player))
    except mysql.connector.IntegrityError as err:
        print("[LOG-DB] Error: {}".format(err))

def add_conversation(facebook_id, who_said_it, message_content, message_timestamp=None, message_intent=None):
    """A function used to add a conversation to the specific player. """
    try:
        if who_said_it == 'Bot':
            bot_said = message_content
            user_said = None
        elif who_said_it == 'User':
            bot_said = None
            user_said = message_content
        add_conversation = ("INSERT INTO conversations "
                      "(facebook_id, bot_said, user_said, message_timestamp, message_intent) "
                      "VALUES (%s, %s, %s, %s, %s)")
        data_conversation = (facebook_id, bot_said, user_said, message_timestamp, message_intent)
        cursor.execute(add_conversation, data_conversation)
        cnx.commit()
        print('[LOG-DB] Added conversation using the following data: {}, {}, {}, {}, {}'.format(*data_conversation))
    except mysql.connector.IntegrityError as err:
        print("[LOG-DB] Error: {}".format(err))
    except:
        raise Exception("""[LOG-DB] Function input data does not fit the assumptions. Please specify who_said_it field properly. Options are: 'Bot' or 'User'""")

def update_player_results(facebook_id, times_won=None):
    """A function used to update player results."""
    if times_won == 1:  # winner player -> 1
        cursor.execute("""
           UPDATE players
           SET times_played=times_played+1, times_won=times_won+1
           WHERE facebook_id=%s
        """, (facebook_id,))
    elif times_won == 0: # winner bot -> 0
        cursor.execute("""
           UPDATE players
           SET times_played=times_played+1, times_lost=times_lost+1
           WHERE facebook_id=%s
        """, (facebook_id,))
    elif times_won == -1:  # draw -> -1
        cursor.execute("""
               UPDATE players
               SET times_played=times_played+1, times_drew=times_drew+1
               WHERE facebook_id=%s
            """, (facebook_id,))
    cnx.commit()

def update_player(facebook_id, first_name=None, last_name=None, gender=None):
    """A function used to update player data."""
    if first_name is not None:
        cursor.execute("""
           UPDATE players
           SET first_name=%s
           WHERE facebook_id=%s
        """, (first_name,facebook_id))
    elif last_name is not None:
        cursor.execute("""
           UPDATE players
           SET last_name=%s
           WHERE facebook_id=%s
        """, (last_name,facebook_id))
    elif gender is not None:
        cursor.execute("""
           UPDATE players
           SET gender=%s
           WHERE facebook_id=%s
        """, (gender,facebook_id))
    cnx.commit()

def db_query(facebook_id, fields_to_query):
    str_facebook_id = "'" + facebook_id + "'"
    str_fields_to_query = ','.join(fields_to_query)
    query =  """SELECT %s
             FROM players 
             WHERE facebook_id = %s""" % (str_fields_to_query, str_facebook_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

"""DATA"""

DB_NAME = 'players'
db_tables = {}
db_tables['players'] = (
    "CREATE TABLE `players` ("
    "  `facebook_id` char(25) NOT NULL,"
    "  `first_name` varchar(25),"
    "  `last_name` varchar(25),"
    "  `gender` enum('Female','Male'),"
    "  `times_played` smallint(1) NOT NULL,"
    "  `times_won` smallint(1) NOT NULL,"
    "  `times_drew` smallint(1) NOT NULL,"
    "  `times_lost` smallint(1) NOT NULL,"
    "  `creation_time` datetime default current_timestamp,"
    "  `modification_time` datetime on update current_timestamp,"
    "  PRIMARY KEY (`facebook_id`)"
    ") ENGINE=InnoDB")

db_tables['conversation'] = (
    "CREATE TABLE `conversations` ("
    "  `conversation_no` int(1) NOT NULL AUTO_INCREMENT,"
    "  `facebook_id` char(25) NOT NULL,"
    "  `bot_said` varchar(999),"
    "  `user_said` varchar(999),"
    "  `message_timestamp` date,"
    "  `message_intent` varchar(255),"
    "  PRIMARY KEY (`facebook_id`,`conversation_no`), KEY `conversation_no` (`conversation_no`),"
    "  CONSTRAINT `conversation_ibfk_1` FOREIGN KEY (`facebook_id`) "
    "     REFERENCES `players` (`facebook_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

local_config =  tokens.local_config

pythonanywhere_config = tokens.pythonanywhere_config

"""SETUP"""

cnx = connect_to_db(local_config)
create_database()
create_tables()
