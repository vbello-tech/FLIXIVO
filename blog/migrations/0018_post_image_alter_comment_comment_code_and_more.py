# Generated by Django 4.1.3 on 2023-01-29 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_comment_comment_code_alter_post_post_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='Post/'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_code',
            field=models.CharField(default='udj7hsihg909ioraricw', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_code',
            field=models.CharField(default='4jljtkqttn19egeirrcu', max_length=20),
        ),
    ]