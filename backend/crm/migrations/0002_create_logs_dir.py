# В файле migrations/0002_create_logs_dir.py
from django.db import migrations
import os

def create_logs_dir(apps, schema_editor):
    os.makedirs('logs', exist_ok=True)

class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_logs_dir),
    ]