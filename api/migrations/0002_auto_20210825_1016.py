# Generated by Django 3.2.6 on 2021-08-25 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessages',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='isRead',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Message_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Message_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=256),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='usermessages',
            name='messages',
            field=models.ManyToManyField(to='api.Message'),
        ),
    ]
