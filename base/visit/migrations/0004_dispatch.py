# Generated by Django 5.1.1 on 2024-09-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '0003_rpmsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(help_text='Fullname', max_length=60)),
                ('username', models.CharField(help_text='Username', max_length=60)),
                ('telegramusername', models.CharField(blank=True, max_length=50, null=True)),
                ('phonenum', models.CharField(blank=True, max_length=9, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]