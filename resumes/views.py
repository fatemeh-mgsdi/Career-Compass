from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from .services import ResumeAnalyzer

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        resume = self.get_object()
        
        # Check if file exists
        if not resume.file:
            return Response(
                {'error': 'No resume file found. Please upload a file first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Analyze resume
            analyzer = ResumeAnalyzer()
            analysis_results = analyzer.analyze_resume(resume.file)
            
            if 'error' in analysis_results:
                return Response(
                    {'error': analysis_results['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Update resume with extracted information
            resume.content = analysis_results['content']
            resume.skills = analysis_results['skills']
            resume.experience = analysis_results['experience']
            resume.education = analysis_results['education']
            resume.save()
            
            # Create analysis record
            analysis = ResumeAnalysis.objects.create(
                resume=resume,
                ats_score=analysis_results['ats_score'],
                ats_details=analysis_results['ats_details'],
                skills_match=analysis_results['skills_match'],
                missing_skills=analysis_results['missing_skills'],
                improvement_suggestions=analysis_results['improvement_suggestions'],
                format_analysis=analysis_results['format_analysis']
            )
            
            serializer = ResumeAnalysisSerializer(analysis)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to analyze resume: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        resume = self.get_object()
        analysis = ResumeAnalysis.objects.filter(resume=resume).first()
        if not analysis:
            return Response({'error': 'No analysis found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeAnalysisSerializer(analysis)
        return Response(serializer.data)
