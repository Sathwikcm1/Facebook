# Generated by Django 5.0.6 on 2024-06-25 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='followerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
