"""
FastAPI Backend for Psychological Test Application
Handles test data processing, AI analysis, and result generation
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import json
import logging
from datetime import datetime
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Psychological Test API",
    description="AI-powered psychological test analysis backend",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve CSS, JS, and assets
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

# Add individual file routes
@app.get("/style.css")
async def get_css():
    return FileResponse("style.css", media_type="text/css")

@app.get("/app.js")
async def get_js():
    return FileResponse("app.js", media_type="application/javascript")

# Serve HTML files directly
from fastapi.responses import FileResponse

@app.get("/developers.html")
async def get_developers_page():
    """Serve developers page"""
    return FileResponse("developers.html")

@app.get("/test.html") 
async def get_test_page():
    """Serve test page"""
    return FileResponse("test.html")

@app.get("/results.html")
async def get_results_page():
    """Serve results page"""
    return FileResponse("results.html")

@app.get("/index.html")
async def get_index_page():
    """Serve index page"""
    return FileResponse("index.html")

@app.get("/how-it-works.html")
async def get_how_it_works_page():
    """Serve how it works page"""
    return FileResponse("how-it-works.html")

# OpenAI API configuration
openai_api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/analyze-test")
async def analyze_test(test_data: dict):
    """
    Analyze psychological test results using AI
    
    Args:
        test_data: Dictionary containing test answers and metadata
        
    Returns:
        Dictionary with analysis results and recommendations
    """
    try:
        logger.info(f"Received test data for analysis: {len(test_data.get('answers', []))} answers")
        
        # Validate test data
        if not test_data.get('answers'):
            raise HTTPException(status_code=400, detail="No test answers provided")
        
        # Calculate basic statistics
        total_score = test_data.get('totalScore', 0)
        max_score = test_data.get('maxScore', 50)
        score_percentage = test_data.get('scorePercentage', 0)
        
        # Generate AI analysis
        ai_analysis = await generate_ai_analysis(test_data)
        
        # Generate category-specific insights
        category_analysis = analyze_by_category(test_data['answers'])
        
        # Generate personalized recommendations
        recommendations = generate_recommendations(score_percentage, category_analysis)
        
        # Prepare response
        analysis_result = {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "total_score": total_score,
            "max_score": max_score,
            "score_percentage": score_percentage,
            "ai_analysis": ai_analysis,
            "category_analysis": category_analysis,
            "recommendations": recommendations,
            "risk_level": determine_risk_level(score_percentage),
            "professional_help_needed": score_percentage < 40
        }
        
        logger.info("Analysis completed successfully")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

async def generate_ai_analysis(test_data: dict) -> str:
    """
    Generate AI-powered analysis of test results
    
    Args:
        test_data: Dictionary containing test answers and metadata
        
    Returns:
        String containing AI analysis
    """
    try:
        # Prepare prompt for AI analysis
        answers_summary = []
        for answer in test_data['answers']:
            answers_summary.append({
                "category": answer['category'],
                "question": answer['question'],
                "answer": answer['answer'],
                "score": answer['value']
            })
        
        prompt = f"""
        Bir psikolojik test sonucunu analiz etmeniz gerekiyor. Aşağıdaki bilgileri kullanarak 
        kişiye özel, anlayışlı ve yapıcı bir analiz yapın:

        Test Sonuçları:
        - Toplam Puan: {test_data.get('totalScore', 0)}/{test_data.get('maxScore', 50)}
        - Yüzde Skoru: {test_data.get('scorePercentage', 0):.1f}%
        
        Soru ve Cevaplar:
        {json.dumps(answers_summary, ensure_ascii=False, indent=2)}
        
        Lütfen aşağıdaki kriterlere göre analiz yapın:
        1. Kişinin genel ruhsal durumunu değerlendirin
        2. Güçlü yönlerini belirtin
        3. Geliştirilmesi gereken alanları nazik bir şekilde işaret edin
        4. Umut verici ve motivasyon artırıcı bir ton kullanın
        5. Profesyonel yardım gerekip gerekmediğini belirtin
        
        Türkçe olarak, yaklaşık 200-300 kelime ile yanıt verin.
        """
        
        # Use OpenAI API if available, otherwise use fallback analysis
        if openai_api_key and openai_api_key != "your-openai-api-key-here":
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen deneyimli bir psikoloji uzmanısın. Anlayışlı, empatik ve yapıcı tavsiyelerde bulunursun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content or generate_fallback_analysis(test_data)
        else:
            # Fallback analysis
            return generate_fallback_analysis(test_data)
            
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}")
        return generate_fallback_analysis(test_data)

def generate_fallback_analysis(test_data: dict) -> str:
    """
    Generate fallback analysis when AI is not available
    
    Args:
        test_data: Dictionary containing test answers and metadata
        
    Returns:
        String containing fallback analysis
    """
    score_percentage = test_data.get('scorePercentage', 0)
    
    if score_percentage >= 80:
        return """
        Test sonuçlarınız, ruhsal sağlığınızın oldukça iyi durumda olduğunu gösteriyor. 
        Genel olarak pozitif bir bakış açısına sahip olduğunuz ve yaşam zorluklarıyla 
        etkili bir şekilde başa çıkabildiğiniz görülüyor. Mevcut sağlıklı alışkanlıklarınızı 
        sürdürmeye devam edin ve kendinize zaman ayırmayı ihmal etmeyin.
        """
    elif score_percentage >= 60:
        return """
        Test sonuçlarınız genel olarak olumlu bir tablo çiziyor. Ruhsal sağlığınız 
        makul seviyelerde olmakla birlikte, bazı alanlarda iyileştirmeler yapabilirsiniz. 
        Düzenli egzersiz, kaliteli uyku ve sosyal aktivitelere katılım gibi sağlıklı 
        yaşam alışkanlıklarını güçlendirerek daha da iyi hissedebilirsiniz.
        """
    elif score_percentage >= 40:
        return """
        Test sonuçlarınız, ruhsal sağlığınızda dikkat edilmesi gereken bazı alanlar 
        olduğunu gösteriyor. Bu durum oldukça yaygın ve üstesinden gelinebilir. 
        Kendinize karşı sabırlı olmak, stres yönetimi teknikleri öğrenmek ve 
        sevdiklerinizle vakit geçirmek faydalı olacaktır. Gerektiğinde profesyonel 
        destek almaktan çekinmeyin.
        """
    else:
        return """
        Test sonuçlarınız, ruhsal sağlığınız konusunda dikkatli olmak gerektiğini 
        gösteriyor. Bu sonuçlar geçici zorluklardan kaynaklanabilir. Kendinize 
        karşı şefkatli olmak çok önemli. Bir ruh sağlığı uzmanı ile görüşmenizi 
        öneriyoruz. Unutmayın ki yardım almak cesaret gerektirir ve iyileşmek 
        mümkündür.
        """

def analyze_by_category(answers: List[dict]) -> Dict[str, Dict]:
    """
    Analyze test results by category
    
    Args:
        answers: List of answer dictionaries
        
    Returns:
        Dictionary with category-specific analysis
    """
    categories = {}
    
    for answer in answers:
        category = answer['category']
        if category not in categories:
            categories[category] = {
                'total_score': 0,
                'question_count': 0,
                'answers': []
            }
        
        categories[category]['total_score'] += answer['value']
        categories[category]['question_count'] += 1
        categories[category]['answers'].append(answer)
    
    # Calculate averages and interpretations
    for category, data in categories.items():
        avg_score = data['total_score'] / data['question_count']
        data['average_score'] = avg_score
        data['percentage'] = (avg_score / 5) * 100
        data['interpretation'] = get_category_interpretation(category, data['percentage'])
    
    return categories

def get_category_interpretation(category: str, percentage: float) -> str:
    """
    Get interpretation for a specific category
    
    Args:
        category: Category name
        percentage: Score percentage for the category
        
    Returns:
        String interpretation of the category score
    """
    if percentage >= 80:
        return "Mükemmel"
    elif percentage >= 60:
        return "İyi"
    elif percentage >= 40:
        return "Orta"
    elif percentage >= 20:
        return "Düşük"
    else:
        return "Çok Düşük"

def generate_recommendations(score_percentage: float, category_analysis: Dict) -> List[str]:
    """
    Generate personalized recommendations based on test results
    
    Args:
        score_percentage: Overall score percentage
        category_analysis: Category-specific analysis
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Base recommendations for everyone
    base_recommendations = [
        "Düzenli egzersiz yapın (haftada en az 3 gün, 30 dakika)",
        "Kaliteli uyku alın (günde 7-9 saat)",
        "Dengeli beslenin ve yeterli su tüketin",
        "Meditasyon veya derin nefes egzersizleri yapın"
    ]
    
    recommendations.extend(base_recommendations)
    
    # Score-based recommendations
    if score_percentage < 40:
        recommendations.extend([
            "Bir ruh sağlığı uzmanı ile görüşmeyi düşünün",
            "Stres yönetimi teknikleri öğrenin",
            "Sevdiğiniz insanlarla vakit geçirin",
            "Hobiler ve ilgi alanlarınıza zaman ayırın"
        ])
    elif score_percentage < 60:
        recommendations.extend([
            "Sosyal aktivitelere katılım artırın",
            "Günlük tutma alışkanlığı edinin",
            "Doğada zaman geçirin",
            "Yeni beceriler öğrenin"
        ])
    else:
        recommendations.extend([
            "Mevcut pozitif alışkanlıklarınızı sürdürün",
            "Başkalarına yardım ederek sosyal bağlarınızı güçlendirin",
            "Kişisel gelişim kitapları okuyun"
        ])
    
    # Category-specific recommendations
    for category, data in category_analysis.items():
        if data['percentage'] < 50:
            if category == "Sleep":
                recommendations.append("Uyku hijyeni kurallarını uygulayın")
            elif category == "Anxiety":
                recommendations.append("Rahatlama tekniklerini öğrenin")
            elif category == "Social":
                recommendations.append("Sosyal aktivitelere katılımınızı artırın")
            elif category == "Stress":
                recommendations.append("Stres yönetimi konusunda destek alın")
    
    return recommendations

def determine_risk_level(score_percentage: float) -> str:
    """
    Determine risk level based on score percentage
    
    Args:
        score_percentage: Overall score percentage
        
    Returns:
        String indicating risk level
    """
    if score_percentage >= 80:
        return "Düşük Risk"
    elif score_percentage >= 60:
        return "Düşük-Orta Risk"
    elif score_percentage >= 40:
        return "Orta Risk"
    elif score_percentage >= 20:
        return "Yüksek Risk"
    else:
        return "Çok Yüksek Risk"

# Additional endpoints for future expansion
@app.get("/api/test-questions")
async def get_test_questions():
    """Get the list of test questions"""
    # This could be expanded to return questions from a database
    return {"message": "Test questions are loaded from frontend"}

@app.post("/api/save-results")
async def save_results(results: dict):
    """Save test results (for future implementation)"""
    # This could be expanded to save results to a database
    return {"message": "Results saved successfully", "id": "saved_result_id"}

@app.get("/api/statistics")
async def get_statistics():
    """Get anonymized statistics (for future implementation)"""
    return {
        "total_tests": 1000,
        "average_score": 65.5,
        "most_common_category": "Mood"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
