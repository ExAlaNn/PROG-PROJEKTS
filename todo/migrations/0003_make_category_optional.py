from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_add_user_to_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='category',
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to='todo.category',
                related_name='todos',
            ),
        ),
    ]
