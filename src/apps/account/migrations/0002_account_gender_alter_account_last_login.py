# Generated by Django 4.2.4 on 2023-08-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[('FL', 'Female'), ('ML', 'Male'), ('CM', 'Custom')], default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
