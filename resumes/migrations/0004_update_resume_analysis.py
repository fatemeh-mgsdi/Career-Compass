from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0003_resumeanalysis_ats_details_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='analysis',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='analysis_status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('processing', 'Processing'),
                    ('completed', 'Completed'),
                    ('failed', 'Failed')
                ],
                default='pending',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='resume',
            name='last_analyzed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ] 