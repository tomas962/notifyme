from .database import db_connect

def get_user(user_id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT id, email, user_group, email_notifications FROM users WHERE id=%s", user_id)
        user = cursor.fetchone()
        cursor.connection.close()
        return user

def get_users():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT id, email, user_group, email_notifications, banned FROM users")
        users = cursor.fetchall()
        cursor.connection.close()
        return users