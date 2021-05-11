from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logincode',
            options={'ordering': ['-id']},
        ),
    ]
