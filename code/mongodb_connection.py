from mongoengine import *
import datetime


def setup_database_connection():
    """The function sets up the MongoDB database connection. Due to the public Github page, at the moment the
    connection information is read from the file, not included in the repository"""

    with open('DB_Connection_Data.txt') as db_connection_data:  # reads the file saved in the current dir
        input_data = db_connection_data.readlines()
        output_db_data = []
        for line in input_data:  # cleaning of the read file
            split_line = line.split(' = ')[1]
            cleaned_line = split_line.replace("\n", "")
            output_db_data.append(cleaned_line)
    # sets up the connection: http: // docs.mongoengine.org / guide / connecting.html
    connect(output_db_data[3], host=('mongodb://' + output_db_data[0] + ':' + output_db_data[1] +
                                     output_db_data[2] + '/' + output_db_data[3]))


class Conversation(EmbeddedDocument):
    """Template for what a conversation looks like in the database.
    Its going to be a list of lists of spoken lines, containing also some additional data
    The conversations list is always embedded in the Player document"""
    who_said_it = BooleanField(required=True)  # 0 bot, 1 human
    message_content = StringField(required=True)  # what message has been sent
    message_timestamp = DateTimeField(required=False)  # when a specific date was recorded
    message_intent = StringField()  # feelings and what not


class Player(Document):
    """Template for what a player document looks like in the database.
    Conversations are embedded to it"""
    facebook_id = StringField(primary_key=True, required=True)  # UNIQUE INDEX OF THE DB
    first_name = StringField()
    last_name = StringField()
    sex = StringField(choices=('Female', 'Male'))
    times_played = IntField(default=0)
    times_won = IntField(default=0)
    conversations = ListField(EmbeddedDocumentField(Conversation))  # a list of embeded conversations
    date_of_joining = DateTimeField(required=True, default=datetime.datetime.now)


def create_player(facebook_id, first_name=None, last_name=None, sex=None):
    """A function used to create a player, given a new, unique facebook_id is provided.
    Sidenote: if the provided facebook_id is already present in the DB, the record is going to be updated"""
    player = Player(
        facebook_id=facebook_id,
        first_name=first_name,
        last_name=last_name,
        sex=sex
    )
    player.save()


def update_player(facebook_id, first_name=None, last_name=None, sex=None, times_played=None,
                  times_won=None):
    """A function used to update player data."""
    query = Player.objects(facebook_id=facebook_id)  # finds the specific record via facebook_id
    if first_name is not None:
        query.update_one(set__first_name=first_name)
    if last_name is not None:
        query.update_one(set__last_name=last_name)
    if sex is not None:
        query.update_one(set__sex=sex)
    if times_played is not None:
        query.update_one(set__times_played=query[0].times_played + times_played)
    # if you want to increment by one, provide 1 as the times_played function argument value
    if times_won is not None:
        query.update_one(set__times_won=query[0].times_won + times_won)

def update_player_results(facebook_id, times_won=None):
    """A function used to update player results.
    Content is similar to update_player function, but it's a bit quicker."""
    query = Player.objects(facebook_id=facebook_id)  # finds the specific record via facebook_id
    query.update_one(set__times_played=query[0].times_played + 1)
    if times_won == 1:
        query.update_one(set__times_won=query[0].times_won + 1)


def add_conversation(facebook_id, who_said_it, message_content, message_timestamp=None, message_intent=None):
    """A function used to add a conversation to the specific player """
    conversation = Conversation(
        who_said_it=who_said_it,
        message_content=message_content,
        message_timestamp=message_timestamp,
        message_intent=message_intent
    )
    query = Player.objects(facebook_id=facebook_id)  # finds the specific record via facebook_id
    query.update_one(push__conversations=conversation)
    # adds the conversation to the player record (to the end of conversations list)


def find_player(facebook_id):
    """A function used to find the specific player and it returns the instance of Player object. """
    query = Player.objects(facebook_id=facebook_id)
    return (query.first())


setup_database_connection()
