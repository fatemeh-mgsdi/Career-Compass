# Generated by Django 5.0.2 on 2025-04-06 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeanalysis',
            name='ats_details',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='resumeanalysis',
            name='format_analysis',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='resumes/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='skills',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='resume',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='resumeanalysis',
            name='ats_score',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='resumeanalysis',
            name='improvement_suggestions',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='resumeanalysis',
            name='missing_skills',
            field=models.JSONField(default=dict),
        ),
    ]
