import os
import json
from dotenv import load_dotenv
from ingest import get_vectorstore

load_dotenv()

def generate_quiz(topic: str) -> list:
    """Generate 5 MCQs from course material."""
    
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(topic, k=4)
    
    if not docs:
        return []
    
    questions = []
    
    # Question 1
    content1 = " ".join(docs[0].page_content.split())[:300]
    questions.append({
        "question": f"What does the course material say about {topic}?",
        "options": [
            f"A. {content1[:80]}...",
            "B. It is not covered in this course",
            "C. It is only mentioned briefly",
            "D. None of the above"
        ],
        "answer": "A",
        "explanation": f"This is directly mentioned on page {docs[0].metadata.get('page', 'unknown')} of your course material."
    })
    
    # Question 2
    if len(docs) > 1:
        content2 = " ".join(docs[1].page_content.split())[:200]
        questions.append({
            "question": f"Which of the following is related to {topic}?",
            "options": [
                f"A. {content2[:80]}...",
                "B. Quantum computing",
                "C. Network security",
                "D. Database management"
            ],
            "answer": "A",
            "explanation": f"Found on page {docs[1].metadata.get('page', 'unknown')} of your course material."
        })
    
    # Question 3
    questions.append({
        "question": f"What is the primary focus of {topic} in this course?",
        "options": [
            "A. Theoretical concepts only",
            "B. Practical implementation only",
            "C. Both theory and practical applications",
            "D. Historical background only"
        ],
        "answer": "C",
        "explanation": "Engineering courses typically cover both theory and practical aspects."
    })
    
    # Question 4
    questions.append({
        "question": f"Which technique is commonly used in {topic}?",
        "options": [
            "A. Convolution",
            "B. Fourier Transform",
            "C. Histogram Processing",
            "D. All of the above"
        ],
        "answer": "D",
        "explanation": "All these techniques are commonly used in image processing applications."
    })
    
    # Question 5
    questions.append({
        "question": f"What is the importance of studying {topic}?",
        "options": [
            "A. Only for academic purposes",
            "B. For real-world applications",
            "C. Not important in modern technology",
            "D. Only for research purposes"
        ],
        "answer": "B",
        "explanation": "The subject has many real-world applications in industry."
    })
    
    return questions[:5]