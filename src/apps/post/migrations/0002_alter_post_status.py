# Generated by Django 4.2.4 on 2023-08-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('PB', 'Published'), ('DF', 'Draft')], default='PB', max_length=2),
        ),
    ]
