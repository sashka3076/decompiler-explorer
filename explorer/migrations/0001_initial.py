# Generated by Django 3.2.12 on 2022-04-08 05:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import explorer.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Binary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=255, upload_to=explorer.models.binary_upload_path)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Compile Date')),
                ('hash', models.CharField(editable=False, max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Decompiler',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255, verbose_name='Version Major.minor.patch')),
                ('revision', models.CharField(blank=True, max_length=255, verbose_name='Specific revision label')),
            ],
        ),
        migrations.CreateModel(
            name='DecompilationRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('completed', models.BooleanField(default=False, editable=False)),
                ('binary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='decompilation_requests', to='explorer.binary')),
                ('decompiler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='decompilation_requests', to='explorer.decompiler')),
            ],
        ),
        migrations.CreateModel(
            name='Decompilation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('decompiled_file', models.FileField(max_length=255, null=True, upload_to=explorer.models.decompilation_upload_path)),
                ('error', models.TextField(null=True, verbose_name='Error Message')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Decompile Date')),
                ('analysis_time', models.FloatField(default=0)),
                ('binary', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='decompilations', to='explorer.binary')),
                ('decompiler', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='decompilations', to='explorer.decompiler')),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='decompilation', to='explorer.decompilationrequest')),
            ],
        ),
        migrations.AddConstraint(
            model_name='decompilationrequest',
            constraint=models.UniqueConstraint(fields=('binary', 'decompiler'), name='unique_binary_decompiler'),
        ),
        migrations.AddConstraint(
            model_name='decompilation',
            constraint=models.UniqueConstraint(fields=('binary', 'decompiler'), name='unique_binary_decompilation'),
        ),
        migrations.AddConstraint(
            model_name='decompilation',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('decompiled_file', ''), ('error__isnull', False)), models.Q(models.Q(('decompiled_file', ''), _negated=True), ('error__isnull', True)), _connector='OR'), name='decompiled_file_or_error'),
        ),
    ]
