# Generated by Django 4.2.7 on 2023-12-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_alter_customermessage_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
