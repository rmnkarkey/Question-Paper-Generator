# Generated by Django 2.1.7 on 2019-03-29 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionGenerator', '0004_auto_20190315_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('question_id', models.IntegerField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=200)),
                ('difficulty', models.CharField(max_length=200)),
                ('marks', models.IntegerField(max_length=200)),
                ('unit_no', models.IntegerField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('semester', models.IntegerField(max_length=200)),
                ('year', models.IntegerField(max_length=200)),
                ('subject_code', models.CharField(max_length=200)),
            ],
        ),
    ]