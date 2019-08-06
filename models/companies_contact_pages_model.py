import peewee
import datetime

from .basic_model import BasicModel


class CompaniesContactPageModel(BasicModel):
    id = peewee.IntegerField()
    company_id = peewee.IntegerField()
    url = peewee.CharField(max_length=512)

    created = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        db_table = 'companies_contact_pages'

