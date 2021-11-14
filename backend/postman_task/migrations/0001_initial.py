# Generated by Django 3.2.9 on 2021-11-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='images')),
                ('image_url', models.TextField(blank=True, null=True)),
                ('wight', models.IntegerField(blank=True)),
                ('height', models.IntegerField()),
            ],
            options={
                'db_table': 'images',
                'managed': True,
            },
        ),
    ]