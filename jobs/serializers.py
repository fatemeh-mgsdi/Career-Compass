from rest_framework import serializers
from .models import Job, JobApplication, JobMatch

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title', 'company', 'description', 'requirements', 'skills_required', 'location', 'job_type', 'experience_level', 'salary_range', 'created_at', 'is_active')
        read_only_fields = ('id', 'created_at')

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('id', 'job', 'user', 'resume', 'cover_letter', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class JobMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMatch
        fields = ('id', 'job', 'user', 'resume', 'match_score', 'skills_matched', 'missing_skills', 'created_at')
        read_only_fields = ('id', 'user', 'created_at') 