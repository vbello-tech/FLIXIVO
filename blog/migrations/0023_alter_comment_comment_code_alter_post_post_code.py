# Generated by Django 4.1.3 on 2023-02-28 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_alter_comment_comment_code_alter_post_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_code',
            field=models.CharField(default='a8atuufrhh5u870d56rg', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_code',
            field=models.CharField(default='tkx8m3ot08ly28euavby', max_length=20),
        ),
    ]