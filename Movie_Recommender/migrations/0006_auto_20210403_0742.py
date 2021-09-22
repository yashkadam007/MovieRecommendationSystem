# Generated by Django 3.1.1 on 2021-04-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movie_Recommender', '0005_myrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myrating',
            name='rating',
            field=models.FloatField(blank=True, choices=[(1, '1-Trash'), (1.5, '1.5-Terrible'), (2, '2-Bad'), (2.5, '2.5-Ok'), (3, '3-Watchable'), (3.5, '3.5-Good'), (4, '4-Very Good'), (4.5, '4.5-Perfect'), (5, '5-Master Piece')]),
        ),
    ]
