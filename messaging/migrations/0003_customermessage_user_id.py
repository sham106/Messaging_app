# Generated by Django 4.2.7 on 2023-12-03 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_customermessage_agent_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermessage',
            name='user_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
