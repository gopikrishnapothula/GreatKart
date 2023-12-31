# Generated by Django 4.2.7 on 2023-12-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
        ('order', '0002_alter_order_payment_alter_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
