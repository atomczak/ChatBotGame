import mysql.connector
from mysql.connector import errorcode
from code import tokens
from signal import signal, SIGPIPE, SIG_DFL

"""Funtion definition"""

def create_database():
    cursor = cnx.cursor()
    DB_NAME = 'RockPaperScissor$Players'
    try:
        cursor.execute("CREATE DATABASE {} ".format(DB_NAME))
    except mysql.connector.Error as err:
        print("[LOG-DBSQL-ERROR] Failed creating database: {}".format(err))
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("[LOG-DBSQL-INFO] Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
            print("[LOG-DBSQL-INFO] Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print('LOG-DBSQL-ERROR ' + str(err))
    try:
        cursor.execute("""
        ALTER DATABASE
            RockPaperScissor$Players
            CHARACTER SET = utf8mb4
            COLLATE = utf8mb4_unicode_ci
        """)
        print ('[LOG-DBSQL-INFO] Changed UTF')
    except:
        print('[LOG-DBSQL-INFO] Failed to changed= UTF')


def connect_to_db(connection_config):
    global cursor
    try:
        cnx = mysql.connector.connect(**connection_config)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[LOG-DBSQL-ERROR] Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[LOG-DBSQL-ERROR] Database does not exist")
        else:
            print(err)
    else:
        return cnx

def create_tables():
    for table_name in db_tables:
        table_description = db_tables[table_name]
        try:
            print("[LOG-DBSQL-INFO] Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            try:
                cursor.execute("""
                ALTER TABLE %s
                CONVERT TO CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci""" % (table_name))
                print("[LOG-DBSQL-INFO] Table charset altering suceeded")
            except:
                print("[LOG-DBSQL-DEBUG] Table charset altering failed")
            try:
                cursor.execute("""
                ALTER TABLE conversations
                CHANGE message_content message_content
                VARCHAR(999)
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci;""")
                print("[LOG-DBSQL-INFO] Column charset altering suceeded")
            except:
                print("[LOG-DBSQL-DEBUG] Column charset altering failed")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print('[LOG-DBSQL-DEBUG] ' + str(err.msg))
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
        print ('[LOG-DBSQL-INFO] Added user {} using the following data: {}, {}, {}, {}, {}, {}, {}'.format(*data_player))
    except mysql.connector.IntegrityError as err:
        print("[LOG-DBSQL-ERROR] Error: {}".format(err))

def add_conversation(facebook_id, who_said_it, message_content, message_timestamp=None, message_intent=None):
    """A function used to add a conversation to the specific player. """
    try:
        add_conversation = ("INSERT INTO conversations "
                          "(facebook_id, message_content, who_said_it, message_timestamp, message_intent) "
                          "VALUES (%s, %s, %s, %s, %s)")
        data_conversation = (facebook_id, message_content, who_said_it, message_timestamp, message_intent)
        cursor.execute(add_conversation, data_conversation)
        cnx.commit()
        print('[LOG-DBSQL-INFO] Added conversation using the following data: {}, {}, {}, {}, {}'.format(*data_conversation))
    except:  #TODO -> FIX THIS EMOJI PROBLEM
        try:
            add_conversation = ("INSERT INTO conversations "
                              "(facebook_id, message_content, who_said_it, message_timestamp, message_intent) "
                              "VALUES (%s, %s, %s, %s, %s)")
            data_conversation = (facebook_id, 'unhandled emoji', who_said_it, message_timestamp, message_intent)
            cursor.execute(add_conversation, data_conversation)
            cnx.commit()
            print('[LOG-DBSQL-INFO] Added conversation emoji using the following data: {}, {}, {}, {}, {}'.format(*data_conversation))
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

def query(facebook_id, fields_to_query):
    str_facebook_id = "'" + facebook_id + "'"
    str_fields_to_query = ','.join(fields_to_query)
    query =  """SELECT %s
             FROM players
             WHERE facebook_id = %s""" % (str_fields_to_query, str_facebook_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def get_all(fields_to_get):
    query =  """SELECT %s
             FROM players
             """ % (fields_to_get)
    cursor.execute(query)
    result = cursor.fetchall()
    return [item[0] for item in result]

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

db_tables['conversations'] = (
    "CREATE TABLE `conversations` ("
    "  `conversation_no` int(1) NOT NULL AUTO_INCREMENT,"
    "  `facebook_id` char(25) NOT NULL,"
    "  `message_content` varchar(999),"
    "  `who_said_it` enum('Bot','User'),"
    "  `message_timestamp` date,"
    "  `message_intent` varchar(255),"
    "  PRIMARY KEY (`facebook_id`,`conversation_no`), KEY `conversation_no` (`conversation_no`),"
    "  CONSTRAINT `conversation_ibfk_1` FOREIGN KEY (`facebook_id`) "
    "     REFERENCES `players` (`facebook_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

local_config =  tokens.local_config

pythonanywhere_config = tokens.pythonanywhere_config

"""SETUP"""

signal(SIGPIPE, SIG_DFL)
cnx = connect_to_db(pythonanywhere_config)
create_database()
create_tables()
