# Generated by Django 4.0.5 on 2022-06-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0007_alter_stock_category_alter_stockhistory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='last_updated',
            field=models.DateField(null=True),
        ),
    ]
