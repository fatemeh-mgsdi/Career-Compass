from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Interview, Question, Answer, InterviewFeedback
from .serializers import InterviewSerializer, QuestionSerializer, AnswerSerializer, InterviewFeedbackSerializer
from .services import InterviewService

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Interview.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_questions(self, request, pk=None):
        interview = self.get_object()
        
        # Get resume content
        resume = interview.resume
        if not resume.content:
            return Response(
                {'error': 'Resume content is empty. Please analyze the resume first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use AI to generate questions
        interview_service = InterviewService()
        questions_data = interview_service.generate_questions(
            resume_content=resume.content,
            job_description=interview.job_description,
            interview_type=interview.interview_type
        )
        
        # Create questions in the database
        created_questions = []
        for question_data in questions_data:
            question = Question.objects.create(
                interview=interview,
                text=question_data['text'],
                category=question_data['category'],
                suggested_answer=question_data['suggested_answer'],
                key_points=question_data['key_points']
            )
            created_questions.append(question)
        
        # Return the created questions
        serializer = QuestionSerializer(created_questions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        interview = self.get_object()
        question_id = request.data.get('question_id')
        answer_text = request.data.get('answer')
        
        if not question_id or not answer_text:
            return Response(
                {'error': 'Both question_id and answer are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            question = Question.objects.get(id=question_id, interview=interview)
        except Question.DoesNotExist:
            return Response(
                {'error': 'Question not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create the answer
        answer = Answer.objects.create(
            question=question,
            user=request.user,
            text=answer_text
        )
        
        # Use AI to evaluate the answer
        interview_service = InterviewService()
        evaluation = interview_service.evaluate_answer(
            question=question.text,
            answer=answer_text,
            suggested_answer=question.suggested_answer,
            key_points=question.key_points
        )
        
        # Create feedback
        feedback = InterviewFeedback.objects.create(
            answer=answer,
            clarity_score=evaluation['clarity_score'],
            technical_score=evaluation['technical_score'],
            confidence_score=evaluation['confidence_score'],
            feedback_text=evaluation['feedback_text'],
            improvement_suggestions=evaluation['improvement_suggestions']
        )
        
        # Return the answer and feedback
        answer_serializer = AnswerSerializer(answer)
        feedback_serializer = InterviewFeedbackSerializer(feedback)
        
        return Response({
            'answer': answer_serializer.data,
            'feedback': feedback_serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        interview = self.get_object()
        questions = Question.objects.filter(interview=interview)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        interview = self.get_object()
        questions = Question.objects.filter(interview=interview)
        answers = Answer.objects.filter(question__in=questions, user=request.user)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def feedback(self, request, pk=None):
        interview = self.get_object()
        questions = Question.objects.filter(interview=interview)
        answers = Answer.objects.filter(question__in=questions, user=request.user)
        feedback = InterviewFeedback.objects.filter(answer__in=answers)
        serializer = InterviewFeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
