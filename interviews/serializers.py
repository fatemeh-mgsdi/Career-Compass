from rest_framework import serializers
from .models import Interview, Question, Answer, InterviewFeedback

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'interview', 'text', 'category', 'suggested_answer', 'key_points', 'created_at')
        read_only_fields = ('id', 'interview', 'created_at')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'user', 'text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = ('id', 'answer', 'clarity_score', 'technical_score', 'confidence_score', 'feedback_text', 'improvement_suggestions', 'created_at')
        read_only_fields = ('id', 'created_at')

class InterviewSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Interview
        fields = ('id', 'user', 'resume', 'title', 'interview_type', 'job_description', 'created_at', 'questions')
        read_only_fields = ('id', 'user', 'created_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 