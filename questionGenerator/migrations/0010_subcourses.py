# Generated by Django 2.1.7 on 2019-04-01 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionGenerator', '0009_courses_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='subCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapters', models.CharField(max_length=299)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionGenerator.courses')),
            ],
        ),
    ]