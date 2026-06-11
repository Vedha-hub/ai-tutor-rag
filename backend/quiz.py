import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from ingest import get_vectorstore

load_dotenv()

QUIZ_PROMPT = """
You are a quiz generator for an academic course.
Generate EXACTLY 5 multiple choice questions about: {topic}
Base questions ONLY on this context: {context}

Return ONLY valid JSON in this exact format, no other text:
[
  {{
    "question": "Question text here?",
    "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
    "answer": "A",
    "explanation": "Brief explanation why A is correct"
  }}
]
"""

def generate_quiz(topic: str) -> list:
    """Generate 5 MCQs using Gemini."""
    
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(topic, k=4)
    
    if not docs:
        return []
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )
    
    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template=QUIZ_PROMPT
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "topic": topic,
        "context": context
    })
    
    raw = response.content.strip()
    
    # Remove markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    
    try:
        questions = json.loads(raw)
        return questions[:5]
    except json.JSONDecodeError:
        # Return fallback questions if JSON parsing fails
        return [
            {
                "question": f"What is {topic}?",
                "options": [
                    "A. A fundamental concept",
                    "B. An advanced technique",
                    "C. A practical application",
                    "D. All of the above"
                ],
                "answer": "D",
                "explanation": "All options describe aspects of this topic."
            }
        ] * 5