# Generated by Django 4.2.5 on 2023-10-16 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author_name', models.CharField(max_length=50)),
                ('author_surname', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=50)),
                ('publication_year', models.CharField(max_length=50)),
                ('page_count', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BookRent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=50)),
                ('reader_surname', models.CharField(max_length=50)),
                ('rent_date', models.DateField()),
                ('return_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=250)),
            ],
        ),
    ]