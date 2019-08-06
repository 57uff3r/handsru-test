import peewee
from .db_connection import database


class BasicModel(peewee.Model):

    class Meta:
        database = database
