# Generated by Django 5.1 on 2024-11-23 12:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_creditcard_cvv_alter_creditcard_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='my_integer',
            field=models.IntegerField(default=0, help_text='Enter a number up to 3 digits', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='cvv',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='year',
            field=models.IntegerField(),
        ),
    ]
