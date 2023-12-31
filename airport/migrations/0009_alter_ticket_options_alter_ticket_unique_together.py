# Generated by Django 4.2.3 on 2023-07-28 17:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0008_airplane_crew"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("flight", "row", "seat")},
        ),
    ]
