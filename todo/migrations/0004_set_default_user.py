from django.db import migrations, models
from django.conf import settings

def set_default_user(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Todo = apps.get_model('todo', 'Todo')
    default_user = User.objects.filter(username='admin').first()
    if default_user:
        Todo.objects.filter(user__isnull=True).update(user=default_user)

class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_make_category_optional'),
    ]

    operations = [
        migrations.RunPython(set_default_user),
        migrations.AlterField(
            model_name='todo',
            name='user',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='todos',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
