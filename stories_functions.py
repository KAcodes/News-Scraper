"""Functions and database needed for api"""
from os import environ
import psycopg2
from psycopg2 import extensions, extras



def get_db_connection() -> extensions.connection:
    """Gets connection from social_news database on local machine"""
    try:
        return psycopg2.connect(
            user=environ["DATABASE_USERNAME"],
            password=environ["DATABASE_PASSWORD"],
            host=environ["DATABASE_IP"],
            port=environ["DATABASE_PORT"],
            database=environ["DATABASE_NAME"]
            )
    except (psycopg2.OperationalError, psycopg2.DatabaseError) as err:
        print("Error connecting to database.", err)


def load_all_stories(connection: extensions.connection) -> list[dict[str]]:
    """Returns all the story data from the database"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)

    cursor.execute("""SELECT stories.*, SUM(CASE votes.direction WHEN 'up'
            THEN 1 WHEN 'down' THEN -1 ELSE 0 END) AS score FROM stories
            LEFT JOIN votes ON stories.id = votes.story_id
            GROUP BY stories.id;""")
    rows = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in rows]


def update_stories(connection: extensions.connection, url: str, title: str, story_id: int):
    """Edits the content of a story"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)

    query = """UPDATE stories
        SET title = %s, url = %s, updated_at = current_timestamp 
        WHERE id = %s;"""
    params = (title, url, story_id)
    cursor.execute(query, params)

    connection.commit()
    cursor.close()


def make_new_story(connection: extensions.connection, url: str, title: str):
    """Creates a new story and adds this to database"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)

    query = "INSERT INTO stories (title, url, created_at, updated_at)\
        VALUES (%s, %s, current_timestamp, current_timestamp);"
    params = (title, url)
    cursor.execute(query, params)

    connection.commit()
    cursor.close()


def find_story_with_id(connection: extensions.connection, story_id: int) -> list[dict]:
    """Finds a story with specific id"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)
    cursor.execute("SELECT * FROM stories WHERE id = %s;", (story_id, ))
    row = cursor.fetchone()
    cursor.close()
    return row


def add_votes(connection: extensions.connection, direction: str, story_id: int) -> None:
    """Adds a new vote to story, inserting row into votes database"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)
    query = """INSERT INTO votes(direction, created_at, updated_at, story_id)
            VALUES (%s, current_timestamp, current_timestamp, %s);"""
    params = (direction, story_id)
    cursor.execute(query, params)

    connection.commit()
    cursor.close()


def delete_story(connection: extensions.connection, story_id: int):
    """Deletes a story given an id"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)

    query = """DELETE FROM votes WHERE story_id = %s;
            DELETE FROM stories WHERE id = %s;"""
    params = (story_id, story_id)
    cursor.execute(query, params)

    connection.commit()
    cursor.close()


def sort_stories(connection: extensions.connection, sort_type: str, order: str) -> list[dict]:
    """Sorts stories based on input from user and returns it"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)
    sort_order = 'ASC' if order in (None, "ascending") else 'DESC'

    if sort_type == "created":
        sort_type += "_at"

    if sort_type == "modified":
        sort_type = "updated_at"

    capitalise = "INITCAP" if sort_type == "title" else ""

    cursor.execute(f"""
                SELECT stories.*, SUM(CASE votes.direction WHEN 'up'
            THEN 1 WHEN 'down' THEN -1 ELSE 0 END) AS score FROM stories
            LEFT JOIN votes ON stories.id = votes.story_id
            GROUP BY stories.id
            ORDER BY {capitalise}({sort_type}) {sort_order};""")

    rows = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in rows]


def find_specific_story(connection: extensions.connection, search: str) -> list[dict]:
    """Finds specific story based on user search"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)

    query = """SELECT stories.*, SUM(CASE votes.direction WHEN 'up'
            THEN 1 WHEN 'down' THEN -1 ELSE 0 END) AS score 
            FROM stories LEFT JOIN votes ON stories.id = votes.story_id
            WHERE LOWER(title) LIKE %s
            GROUP BY stories.id 
            ;"""
    params = (f'%{search.lower()}%',)
    cursor.execute(query, params)

    rows = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in rows]


def count_votes(connection: extensions.connection, story_id) -> list[dict]:
    """Counts the votes for a specific story"""
    cursor = connection.cursor(cursor_factory = extras.RealDictCursor)

    query = """SELECT SUM(CASE direction WHEN 'up' THEN 1 ELSE -1 END)
                AS score
                FROM votes WHERE story_id = %s;"""
    params = (story_id, )
    cursor.execute(query, params)

    row = cursor.fetchone()
    cursor.close()

    return row
