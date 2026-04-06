"""
PS-09 | CSE AI
AI Resume Screener & Career Roadmap Advisor for Students
"""

import PyPDF2
import docx
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Set
import pandas as pd
import streamlit as st

class ResumeScreener:
    def __init__(self):
        # Industry skill benchmarks for different roles
        self.skill_benchmarks = {
            "Data Scientist": {
                "required": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
                "preferred": ["TensorFlow", "PyTorch", "Cloud Computing", "Big Data", "Deep Learning"],
                "certifications": ["IBM Data Science", "Google Data Analytics", "AWS Certified Data Analytics"]
            },
            "Software Engineer": {
                "required": ["Python", "Java", "Data Structures", "Algorithms", "Git", "SQL"],
                "preferred": ["React", "Node.js", "Docker", "Kubernetes", "Microservices", "AWS"],
                "certifications": ["AWS Developer", "Microsoft Azure Developer", "Google Associate Engineer"]
            },
            "AI Engineer": {
                "required": ["Python", "Machine Learning", "Deep Learning", "NLP", "PyTorch/TensorFlow", "SQL"],
                "preferred": ["Computer Vision", "Transformers", "MLOps", "LangChain", "Cloud AI Services"],
                "certifications": ["NVIDIA DLI", "TensorFlow Developer", "AWS AI/ML Specialty"]
            },
            "Frontend Developer": {
                "required": ["HTML", "CSS", "JavaScript", "React", "Git"],
                "preferred": ["TypeScript", "Next.js", "Tailwind CSS", "Vue.js", "Webpack"],
                "certifications": ["Meta Frontend Developer", "freeCodeCamp Frontend", "Google UX Design"]
            },
            "Backend Developer": {
                "required": ["Python/Java", "SQL", "REST APIs", "Git", "Linux"],
                "preferred": ["Django/Spring Boot", "Node.js", "MongoDB", "Redis", "Docker", "Kafka"],
                "certifications": ["Oracle Java Cert", "Python Institute PCEP", "MongoDB Developer"]
            },
            "DevOps Engineer": {
                "required": ["Linux", "Docker", "CI/CD", "Git", "Scripting (Python/Bash)"],
                "preferred": ["Kubernetes", "Jenkins", "Terraform", "Prometheus", "AWS/Azure/GCP"],
                "certifications": ["AWS DevOps", "CKA", "Docker Certified", "Terraform Associate"]
            },
            "Data Analyst": {
                "required": ["SQL", "Excel", "Python/R", "Data Visualization", "Statistics"],
                "preferred": ["Tableau", "Power BI", "Pandas", "NumPy", "Business Intelligence"],
                "certifications": ["Google Data Analytics", "Microsoft Power BI", "Tableau Desktop Specialist"]
            },
            "ML Engineer": {
                "required": ["Python", "Machine Learning", "SQL", "Data Processing", "Model Deployment"],
                "preferred": ["MLflow", "Kubeflow", "TensorFlow Extended", "Feature Stores", "Vector Databases"],
                "certifications": ["MLOps Engineering", "TensorFlow Developer", "AWS ML Specialty"]
            }
        }
        
        # Career roadmap templates
        self.roadmap_templates = {
            "Data Scientist": {
                "0-3 months": ["Learn Python basics", "Complete SQL course", "Statistics fundamentals"],
                "3-6 months": ["Machine Learning basics (Scikit-learn)", "Data Visualization (Matplotlib/Seaborn)", "Kaggle beginner competitions"],
                "6-12 months": ["Deep Learning basics (TensorFlow/PyTorch)", "Big Data tools (Spark)", "Build portfolio projects"],
                "12-18 months": ["Cloud platforms (AWS/GCP)", "MLOps basics", "Advanced certifications"]
            },
            "Software Engineer": {
                "0-3 months": ["Master Data Structures & Algorithms", "Learn version control (Git)", "Complete Python/Java basics"],
                "3-6 months": ["Database design & SQL", "Build REST APIs", "Learn testing frameworks"],
                "6-12 months": ["System design basics", "Learn framework (Django/Spring)", "Open source contributions"],
                "12-18 months": ["Cloud services", "Microservices architecture", "Advanced system design"]
            },
            "AI Engineer": {
                "0-3 months": ["Python advanced", "Math refresher (Linear Algebra, Calculus)", "ML fundamentals"],
                "3-6 months": ["Deep Learning specialization", "NLP/Computer Vision basics", "PyTorch/TensorFlow mastery"],
                "6-12 months": ["LLM fundamentals (Transformers, RAG)", "MLOps and deployment", "AI portfolio projects"],
                "12-18 months": ["Multi-modal AI", "Production AI systems", "AI safety and ethics"]
            }
        }
    
    def extract_text_from_pdf(self, file_source) -> str:
        """Extract text from PDF file or buffer"""
        text = ""
        try:
            if isinstance(file_source, str):
                with open(file_source, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
            else:
                pdf_reader = PyPDF2.PdfReader(file_source)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            text = f"Error reading PDF: {e}"
        return text
    
    def extract_text_from_docx(self, file_source) -> str:
        """Extract text from DOCX file or buffer"""
        text = ""
        try:
            doc = docx.Document(file_source)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            text = f"Error reading DOCX: {e}"
        return text
    
    def extract_skills_from_resume(self, resume_text: str) -> Set[str]:
        """Extract skills from resume text using pattern matching"""
        tech_skills = {
            "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Swift", "Kotlin",
            "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring Boot", "Express.js",
            "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn",
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Elasticsearch",
            "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "CI/CD", "Terraform", "Ansible",
            "AWS", "Azure", "GCP", "Cloud Computing", "Serverless", "Lambda", "S3", "EC2",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Science", "Data Analysis",
            "HTML", "CSS", "SASS", "Tailwind CSS", "Bootstrap", "TypeScript", "Next.js", "Nuxt.js",
            "GraphQL", "REST API", "Microservices", "System Design", "Algorithms", "Data Structures",
            "Linux", "Unix", "Bash", "PowerShell", "Excel", "Tableau", "Power BI", "Looker"
        }
        resume_lower = resume_text.lower()
        found_skills = set()
        for skill in tech_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, resume_lower):
                found_skills.add(skill)
        return found_skills
    
    def extract_experience_years(self, resume_text: str) -> float:
        """Extract years of experience from resume"""
        patterns = [
            r'(\d+)\+?\s*years?\s+of\s+experience',
            r'experience\s+of\s+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+experience',
        ]
        for pattern in patterns:
            match = re.search(pattern, resume_text.lower())
            if match:
                return float(match.group(1))
        date_pattern = r'(20\d{2})\s*[-–]\s*(?:present|current|20\d{2})'
        dates = re.findall(date_pattern, resume_text.lower())
        if len(dates) >= 2:
            return float(max(2026 - int(dates[0]), 0))
        return 0.0
    
    def evaluate_resume(self, resume_text: str, target_role: str) -> Dict:
        """Evaluate resume against target role benchmarks"""
        if target_role not in self.skill_benchmarks:
            return {"error": f"Role '{target_role}' not found."}
        
        resume_skills = self.extract_skills_from_resume(resume_text)
        experience_years = self.extract_experience_years(resume_text)
        benchmark = self.skill_benchmarks[target_role]
        required_skills = set(benchmark["required"])
        preferred_skills = set(benchmark["preferred"])
        
        matched_required = resume_skills & required_skills
        missing_required = required_skills - resume_skills
        matched_preferred = resume_skills & preferred_skills
        
        required_score = len(matched_required) / len(required_skills) * 60 if required_skills else 0
        preferred_score = len(matched_preferred) / len(preferred_skills) * 20 if preferred_skills else 0
        experience_score = min(experience_years / 2 * 20, 20)
        
        total_score = required_score + preferred_score + experience_score
        
        suggestions = []
        if missing_required:
            suggestions.append(f"Learn these required skills: {', '.join(missing_required)}")
        if len(matched_preferred) < len(preferred_skills) / 2:
            suggestions.append(f"Enhance your profile with preferred skills: {', '.join(preferred_skills - resume_skills)}")
        if experience_years < 1:
            suggestions.append("Gain practical experience through internships or personal projects")
        if total_score < 70:
            suggestions.append("Consider certification courses to strengthen your profile")
        
        roadmap = self.generate_roadmap(target_role, missing_required, preferred_skills - resume_skills)
        
        return {
            "resume_score": round(total_score, 2),
            "matched_required_skills": list(matched_required),
            "missing_required_skills": list(missing_required),
            "matched_preferred_skills": list(matched_preferred),
            "missing_preferred_skills": list(preferred_skills - resume_skills),
            "experience_years": experience_years,
            "suggestions": suggestions,
            "recommended_certifications": benchmark["certifications"],
            "career_roadmap": roadmap
        }
    
    def generate_roadmap(self, role: str, missing_skills: Set[str], preferred_skills: Set[str]) -> Dict:
        """Generate personalized career roadmap"""
        if role in self.roadmap_templates:
            roadmap = self.roadmap_templates[role].copy()
            if missing_skills:
                roadmap["0-3 months"].insert(0, f"Focus on: {', '.join(list(missing_skills)[:3])}")
            if preferred_skills:
                roadmap["3-6 months"].append(f"Add advantage: {', '.join(list(preferred_skills)[:2])}")
            return roadmap
        else:
            return {
                "0-3 months": ["Learn fundamentals", "Build foundational skills", "Start online courses"],
                "3-6 months": ["Practice with projects", "Learn industry tools", "Earn entry-level certification"],
                "6-12 months": ["Build portfolio", "Contribute to open source", "Network with professionals"],
                "12-18 months": ["Advanced certifications", "Specialize in domain", "Apply for roles"]
            }
    
    def process_resume(self, file_source, target_role: str, filename: str = "") -> Dict:
        """Main function to process resume and return evaluation"""
        resume_text = ""
        if filename.endswith('.pdf'):
            resume_text = self.extract_text_from_pdf(file_source)
        elif filename.endswith('.docx'):
            resume_text = self.extract_text_from_docx(file_source)
        else:
            try:
                if isinstance(file_source, str):
                    with open(file_source, 'r', encoding='utf-8') as f:
                        resume_text = f.read()
                else:
                    resume_text = file_source.read().decode('utf-8')
            except:
                return {"error": "Unsupported file format. Please upload PDF, DOCX or TXT"}
        
        if not resume_text.strip() or resume_text.startswith("Error"):
            return {"error": f"Could not extract text: {resume_text}"}
        
        return self.evaluate_resume(resume_text, target_role)

def create_sample_resume():
    """Create a sample resume text for testing"""
    sample_resume = """
    JOHN DOE
    Computer Science Graduate | Class of 2025
    
    EDUCATION:
    Bachelor of Technology in Computer Science
    XYZ University, GPA: 3.7/4.0
    
    TECHNICAL SKILLS:
    - Programming: Python, Java, SQL
    - Web: HTML, CSS, JavaScript, React
    - Data: Pandas, NumPy, Matplotlib
    - Tools: Git, VS Code, Linux
    
    PROJECTS:
    - E-commerce Website: Built full-stack application using React and Node.js
    - Data Analysis Dashboard: Created interactive dashboard using Python and Plotly
    - Machine Learning Model: Implemented classification model using Scikit-learn
    
    INTERNSHIP:
    Software Development Intern | ABC Tech | Summer 2024
    - Developed REST APIs using Python Flask
    - Worked with PostgreSQL database
    - Participated in code reviews and agile ceremonies
    
    CERTIFICATIONS:
    - Python for Everybody (Coursera)
    - SQL Fundamentals (HackerRank)
    """
    with open("sample_resume.txt", "w") as f:
        f.write(sample_resume)

def streamlit_ui():
    """Streamlit interface for AI Resume Screener"""
    st.set_page_config(
        page_title="ResumeAI - Premium Resume Screener",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        .stMetric {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .skill-card {
            background: rgba(45, 212, 191, 0.1);
            color: #2dd4bf;
            padding: 5px 12px;
            border-radius: 20px;
            display: inline-block;
            margin: 4px;
            font-size: 0.85rem;
            border: 1px solid rgba(45, 212, 191, 0.3);
        }
        .missing-skill-card {
            background: rgba(248, 113, 113, 0.1);
            color: #f87171;
            padding: 5px 12px;
            border-radius: 20px;
            display: inline-block;
            margin: 4px;
            font-size: 0.85rem;
            border: 1px solid rgba(248, 113, 113, 0.3);
        }
        .roadmap-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-left: 4px solid #3b82f6;
            margin-bottom: 10px;
            border-radius: 0 10px 10px 0;
        }
        .category-header {
            color: #3b82f6;
            font-weight: 700;
            margin-top: 20px;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("💼 Hackit")
        st.write("---")
        uploaded_file = st.file_uploader("📂 Upload Resume", type=['pdf', 'docx', 'txt'])
        available_roles = [
            "Data Scientist", "Software Engineer", "AI Engineer", 
            "Frontend Developer", "Backend Developer", "DevOps Engineer", 
            "Data Analyst", "ML Engineer"
        ]
        target_role = st.selectbox("🎯 Target Role", available_roles)
        analyze_button = st.button("🚀 Analyze Resume", use_container_width=True, type="primary")
        st.write("---")
        st.info("💡 Tip: Upload a detailed resume for better analysis.")
        
        # Developer Credits
        st.markdown("""
            <div style="margin-top: 50px; font-size: 0.8rem; color: rgba(255,255,255,0.5);">
                👨‍💻 Code written and deployed by<br>
                <b>Anshu Sharma 25BAI11353</b>
            </div>
        """, unsafe_allow_html=True)

    st.title("🤖 AI Resume Screener & Career Roadmap Advisor for Students")
    st.markdown("### Elevate your career \n with \n AI-driven resume insights and personalized growth paths.")
    st.write("---")

    if analyze_button and uploaded_file is not None:
        with st.spinner("🧠 Analyzing your resume..."):
            screener = ResumeScreener()
            results = screener.process_resume(uploaded_file, target_role, uploaded_file.name)
            
            if "error" in results:
                st.error(f"❌ Error: {results['error']}")
            else:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    score = results['resume_score']
                    st.metric("🏆 Resume Score", f"{score}/100")
                    st.progress(score / 100)
                with col2:
                    st.metric("💼 Experience", f"{results['experience_years']} Years")
                with col3:
                    match_count = len(results['matched_required_skills'])
                    total_req = match_count + len(results['missing_required_skills'])
                    st.metric("✅ Core Skills", f"{match_count}/{total_req}")

                st.write("---")
                layout_col1, layout_col2 = st.columns([1, 1])
                with layout_col1:
                    st.subheader("🛠️ Technical Skill Assessment")
                    st.markdown("<div class='category-header'>✓ Matched Required Skills</div>", unsafe_allow_html=True)
                    if results['matched_required_skills']:
                        st.markdown(" ".join([f"<span class='skill-card'>{skill}</span>" for skill in results['matched_required_skills']]), unsafe_allow_html=True)
                    else:
                        st.write("No required skills matched.")
                        
                    st.markdown("<div class='category-header'>✗ Missing Required Skills</div>", unsafe_allow_html=True)
                    if results['missing_required_skills']:
                        st.markdown(" ".join([f"<span class='missing-skill-card'>{skill}</span>" for skill in results['missing_required_skills']]), unsafe_allow_html=True)
                    else:
                        st.write("✨ You've got all core required skills!")
                        
                    st.markdown("<div class='category-header'>🔥 Preferred Skills Found</div>", unsafe_allow_html=True)
                    if results['matched_preferred_skills']:
                        st.markdown(" ".join([f"<span class='skill-card'>{skill}</span>" for skill in results['matched_preferred_skills']]), unsafe_allow_html=True)
                    else:
                        st.write("No preferred skills matched yet.")

                with layout_col2:
                    st.subheader("💡 Strategic Insights")
                    for suggestion in results['suggestions']:
                        st.info(suggestion)
                    st.markdown("<div class='category-header'>🎓 Recommended Certifications</div>", unsafe_allow_html=True)
                    for cert in results['recommended_certifications']:
                        st.write(f"- 📜 {cert}")

                st.write("---")
                st.subheader("🗺️ Personalized Career Roadmap")
                st.markdown("Your optimized path to master this role over the next 18 months.")
                roadmap_tabs = st.tabs(list(results['career_roadmap'].keys()))
                for i, (period, tasks) in enumerate(results['career_roadmap'].items()):
                    with roadmap_tabs[i]:
                        for task in tasks:
                            st.markdown(f"<div class='roadmap-card'>🔹 {task}</div>", unsafe_allow_html=True)
                
                st.sidebar.download_button(
                    label="💾 Download Full Report",
                    data=json.dumps(results, indent=2),
                    file_name=f"resume_analysis_{target_role.replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    elif not analyze_button and uploaded_file is None:
        st.write("### 👈 To get started, upload your resume in the sidebar!")
        st.info("Ready to take the next step in your career? Our AI will analyze your skills and build a roadmap for your dream role.")

def main():
    """Entry point to run Streamlit UI"""
    streamlit_ui()

if __name__ == "__main__":
    main()