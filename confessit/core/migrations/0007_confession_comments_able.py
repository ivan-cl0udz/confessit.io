from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_comment_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='confession',
            name='comments_able',
            field=models.BooleanField(default=True),
        ),
    ]
