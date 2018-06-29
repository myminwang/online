# Generated by Django 2.0.6 on 2018-06-29 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20180610_1336'),
        ('courses', '0004_auto_20180608_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursebanner',
            name='courseinfo_ptr',
        ),
        migrations.DeleteModel(
            name='CourseBanner',
        ),
        migrations.CreateModel(
            name='CourseBanner',
            fields=[
            ],
            options={
                'verbose_name': '轮播课程',
                'verbose_name_plural': '轮播课程',
                'proxy': True,
                'indexes': [],
            },
            bases=('courses.courseinfo',),
        ),
    ]