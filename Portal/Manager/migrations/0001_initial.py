# Generated by Django 2.2 on 2022-02-04 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='user first name', max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, help_text='user last name', max_length=100, null=True)),
                ('email', models.CharField(help_text='user email', max_length=100, null=True)),
                ('address', models.CharField(blank=True, help_text='user address', max_length=400, null=True)),
                ('dob', models.DateField(blank=True, help_text='date of birth format YYYY-MM-DD', null=True, verbose_name='date of birth')),
                ('company', models.CharField(help_text='user company name', max_length=100, null=True, unique=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='activate/deactivate user')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Managers',
                'db_table': 'manager',
                'unique_together': {('user', 'email')},
            },
        ),
    ]
