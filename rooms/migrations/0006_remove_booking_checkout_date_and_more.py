# Generated by Django 4.0.6 on 2022-07-25 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_email_remove_customuser_first_name_and_more'),
        ('rooms', '0005_alter_room_address_alter_room_area_of_room_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='checkout_date',
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_status',
            field=models.CharField(choices=[('booked', 'booked'), ('pending', 'pending'), ('cancel', 'cancel')], default='pending', max_length=15),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, max_length=3000)),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser')),
            ],
        ),
    ]