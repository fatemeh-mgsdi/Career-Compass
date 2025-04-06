import os
import json
from openai import OpenAI
from typing import Dict, List

class InterviewService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_questions(self, resume_content: str, job_description: str, interview_type: str) -> List[Dict]:
        """Generate interview questions based on resume, job description, and interview type."""
        prompt = f"""Generate a list of interview questions for a {interview_type} interview based on the following resume and job description.
        
        Resume:
        {resume_content}
        
        Job Description:
        {job_description}
        
        Generate 5-7 relevant questions that would be asked in a {interview_type} interview for this position.
        For each question, provide:
        1. The question text
        2. The category (technical, behavioral, or system_design)
        3. A suggested answer based on the resume
        4. Key points that should be included in the answer
        
        Format the response as a JSON array of objects with the following structure:
        [
            {{
                "text": "Question text here",
                "category": "category here",
                "suggested_answer": "Suggested answer here",
                "key_points": ["point 1", "point 2", "point 3"]
            }},
            ...
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert interview coach specializing in technical, behavioral, and system design interviews."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Clean up the response - remove markdown code block formatting if present
            if content.startswith('```json'):
                content = content.replace('```json', '', 1)
            if content.endswith('```'):
                content = content.rsplit('```', 1)[0]
            
            # Strip any leading/trailing whitespace
            content = content.strip()
            
            # Parse the JSON
            questions = json.loads(content)
            return questions
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []
    
    def evaluate_answer(self, question: str, answer: str, suggested_answer: str, key_points: List[str]) -> Dict:
        """Evaluate a candidate's answer to an interview question."""
        prompt = f"""Evaluate the following interview answer:
        
        Question: {question}
        
        Candidate's Answer: {answer}
        
        Suggested Answer: {suggested_answer}
        
        Key Points to Include: {', '.join(key_points)}
        
        Provide a detailed evaluation with:
        1. A clarity score (0-1)
        2. A technical accuracy score (0-1)
        3. A confidence score (0-1)
        4. Feedback text
        5. Improvement suggestions
        
        Format the response as a JSON object with the following structure:
        {{
            "clarity_score": 0.0,
            "technical_score": 0.0,
            "confidence_score": 0.0,
            "feedback_text": "Feedback here",
            "improvement_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert interview evaluator specializing in technical, behavioral, and system design interviews."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Clean up the response - remove markdown code block formatting if present
            if content.startswith('```json'):
                content = content.replace('```json', '', 1)
            if content.endswith('```'):
                content = content.rsplit('```', 1)[0]
            
            # Strip any leading/trailing whitespace
            content = content.strip()
            
            # Parse the JSON
            evaluation = json.loads(content)
            return evaluation
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return {
                "clarity_score": 0.5,
                "technical_score": 0.5,
                "confidence_score": 0.5,
                "feedback_text": "Unable to evaluate answer due to an error.",
                "improvement_suggestions": ["Try again with a more detailed answer."]
            } 