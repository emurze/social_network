from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0007_rename_contract_followcontract_and_more'),
    ]

    operations = [
        TrigramExtension(),
    ]