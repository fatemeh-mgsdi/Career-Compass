import PyPDF2
import json
import os
from openai import OpenAI
from typing import Dict

class ResumeAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                

    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        return text


    def analyze_with_ai(self, text: str) -> Dict:
        """Use AI to analyze the resume content."""
        prompt = f"""Analyze the following resume and provide a detailed analysis in JSON format. Include:
        1. Extracted skills (both technical and soft skills)
        2. Education details
        3. Work experience details
        4. ATS score (0-1) with explanation
        5. Improvement suggestions
        6. Missing important skills for their field (ONLY suggest skills that are relevant to their current career path, DO NOT suggest learning completely different programming languages)
        7. Keyword analysis
        8. Format and presentation analysis

        Resume text:
        {text}

        Provide the analysis in the following JSON format:
        {{
            "skills": {{"technical": [], "soft": []}},
            "education": [{{"degree": "", "institution": "", "year": "", "field": ""}}],
            "experience": [{{
                "company": "",
                "position": "",
                "duration": "",
                "responsibilities": [],
                "achievements": []
            }}],
            "ats_analysis": {{
                "score": 0.0,
                "explanation": "",
                "keyword_density": 0.0,
                "format_score": 0.0
            }},
            "improvement_suggestions": [],
            "missing_skills": [],
            "keyword_analysis": {{
                "found_keywords": [],
                "missing_keywords": [],
                "industry_relevance": 0.0
            }},
            "format_analysis": {{
                "structure": "",
                "readability": "",
                "suggestions": []
            }}
        }}
        """

        try:
            models = self.client.models.list()
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert ATS system and resume analyzer. Provide detailed, professional analysis of resumes. When suggesting missing skills, ONLY suggest skills that are relevant to the person's current career path. DO NOT suggest learning completely different programming languages."},
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
            analysis = json.loads(content)
            return analysis
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return None

    def analyze_resume(self, pdf_file) -> Dict:
        """Analyze resume and return comprehensive results."""
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_file)
        
        # Get AI analysis
        analysis = self.analyze_with_ai(text)
        
        if not analysis:
            return {
                'error': 'Failed to analyze resume with AI'
            }
        
        # Filter out irrelevant missing skills (different programming languages)
        missing_skills = analysis.get('missing_skills', [])
        if isinstance(missing_skills, list):
            # Get the main programming language from the skills
            main_language = None
            for skill in analysis.get('skills', {}).get('technical', []):
                if skill.lower() in ['python', 'javascript', 'java', 'c#', 'c++', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin']:
                    main_language = skill.lower()
                    break
            
            # Filter out different programming languages
            if main_language:
                filtered_missing_skills = []
                for skill in missing_skills:
                    skill_lower = skill.lower()
                    # Skip if it's a different programming language
                    if skill_lower in ['python', 'javascript', 'java', 'c#', 'c++', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin'] and skill_lower != main_language:
                        continue
                    filtered_missing_skills.append(skill)
                missing_skills = filtered_missing_skills
        
        # Format the response
        return {
            'content': text,
            'skills': {
                'technical': analysis['skills']['technical'],
                'soft': analysis['skills']['soft']
            },
            'education': analysis['education'],
            'experience': analysis['experience'],
            'ats_score': analysis['ats_analysis']['score'],
            'ats_details': {
                'explanation': analysis['ats_analysis']['explanation'],
                'keyword_density': analysis['ats_analysis']['keyword_density'],
                'format_score': analysis['ats_analysis']['format_score']
            },
            'skills_match': {
                'found_keywords': analysis['keyword_analysis']['found_keywords'],
                'industry_relevance': analysis['keyword_analysis']['industry_relevance']
            },
            'missing_skills': missing_skills,
            'improvement_suggestions': (
                analysis['improvement_suggestions'] +
                analysis['format_analysis']['suggestions']
            ),
            'format_analysis': {
                'structure': analysis['format_analysis']['structure'],
                'readability': analysis['format_analysis']['readability']
            }
        } 