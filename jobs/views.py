from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Job, JobApplication, JobMatch
from .serializers import JobSerializer, JobApplicationSerializer, JobMatchSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(requirements__icontains=search)
            )
        return queryset
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        job = self.get_object()
        resume_id = request.data.get('resume_id')
        cover_letter = request.data.get('cover_letter', '')
        
        if not resume_id:
            return Response(
                {'error': 'resume_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create job application
        application = JobApplication.objects.create(
            job=job,
            user=request.user,
            resume_id=resume_id,
            cover_letter=cover_letter,
            status='submitted'
        )
        
        # TODO: Implement job matching logic
        match = JobMatch.objects.create(
            job=job,
            user=request.user,
            resume_id=resume_id,
            match_score=0.75,  # Dummy score
            skills_matched=['python', 'django'],  # Dummy matches
            missing_skills=['react', 'aws']  # Dummy missing skills
        )
        
        application_serializer = JobApplicationSerializer(application)
        match_serializer = JobMatchSerializer(match)
        
        return Response({
            'application': application_serializer.data,
            'match': match_serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        job = self.get_object()
        matches = JobMatch.objects.filter(job=job, user=request.user)
        serializer = JobMatchSerializer(matches, many=True)
        return Response(serializer.data)

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        application = self.get_object()
        application.status = 'withdrawn'
        application.save()
        return Response({'status': 'application withdrawn'})
