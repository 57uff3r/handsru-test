import peewee
import datetime

from .basic_model import BasicModel


class UserModel(BasicModel):
    id = peewee.IntegerField()
    company_name = peewee.CharField(max_length=512)
    created = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        db_table = 'companies'

