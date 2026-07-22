import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_alter_batch_courses_alter_batch_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
