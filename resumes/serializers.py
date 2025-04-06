from rest_framework import serializers
from .models import Resume, ResumeAnalysis

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'title', 'file', 'content', 'skills', 'experience', 'education', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ('id', 'resume', 'ats_score', 'skills_match', 'missing_skills', 'improvement_suggestions', 'created_at')
        read_only_fields = ('id', 'created_at') 