from peewee import *

db = SqliteDatabase('Users.db')


class User(Model):
    first_name = CharField(default="Mysterious")
    last_name = CharField(default="Stranger")
    chat_id = IntegerField(unique=True)
    real_time_check = BooleanField(default=False)

    class Meta:
        database = db


def create_tables():
    db.connect()
    db.create_tables([User])


if __name__ == "__main__":
    create_tables()
