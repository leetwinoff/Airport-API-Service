# Generated by Django 4.2.3 on 2023-07-24 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0006_alter_order_order_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterField(
            model_name="ticket",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="airport.order",
            ),
        ),
        migrations.AlterModelTable(
            name="order",
            table="order",
        ),
    ]
