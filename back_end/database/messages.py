from .database import db_connect


def insert_message(user_id, title, text):
    with db_connect().cursor() as cursor:
        cursor.execute("INSERT INTO `messages`(`user_id`, `title`, `text`) VALUES (%s, %s, %s)", (user_id, title, text))
        cursor.connection.commit()
        cursor.connection.close()
        return cursor.lastrowid

def get_all_user_messages(user_id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM messages WHERE user_id=%s", user_id)
        messages = cursor.fetchall()
        cursor.connection.close()
        return messages