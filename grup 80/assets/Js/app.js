// App.js - Main JavaScript functionality for the psychological test application

// Header scroll behavior
let lastScrollTop = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > lastScrollTop && scrollTop > 100) {
        // Scrolling down
        header.classList.add('hidden');
    } else {
        // Scrolling up
        header.classList.remove('hidden');
    }
    
    lastScrollTop = scrollTop;
});

// Global variables
let currentQuestion = 0;
let testAnswers = [];
let testQuestions = [];
let testStartTime = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the test page
    if (window.location.pathname.includes('test.html')) {
        initializeTest();
    }
    
    // Check if we're on the results page
    if (window.location.pathname.includes('results.html')) {
        displayResults();
    }
});

// Test questions data
const psychologicalTestQuestions = [
    {
        id: 1,
        category: "Mood",
        question: "Son iki hafta içinde kendinizi nasıl hissettiniz?",
        options: [
            { text: "Çok iyi ve enerjik", value: 5 },
            { text: "Genel olarak iyi", value: 4 },
            { text: "Normal/kararsız", value: 3 },
            { text: "Biraz kötü", value: 2 },
            { text: "Çok kötü ve umutsuz", value: 1 }
        ]
    },
    {
        id: 2,
        category: "Sleep",
        question: "Uyku kaliteniz nasıl?",
        options: [
            { text: "Çok iyi, dinlendirici", value: 5 },
            { text: "Genellikle iyi", value: 4 },
            { text: "Bazen iyi bazen kötü", value: 3 },
            { text: "Genellikle kötü", value: 2 },
            { text: "Çok kötü, uykusuzluk", value: 1 }
        ]
    },
    {
        id: 3,
        category: "Anxiety",
        question: "Ne sıklıkla endişe veya kaygı hissediyorsunuz?",
        options: [
            { text: "Hiçbir zaman", value: 5 },
            { text: "Nadiren", value: 4 },
            { text: "Bazen", value: 3 },
            { text: "Sık sık", value: 2 },
            { text: "Sürekli", value: 1 }
        ]
    },
    {
        id: 4,
        category: "Social",
        question: "Sosyal aktivitelere katılma isteğiniz nasıl?",
        options: [
            { text: "Çok istekliyim", value: 5 },
            { text: "Genellikle istekliyim", value: 4 },
            { text: "Bazen istekliyim", value: 3 },
            { text: "Genellikle istemiyorum", value: 2 },
            { text: "Hiç istemiyorum", value: 1 }
        ]
    },
    {
        id: 5,
        category: "Concentration",
        question: "Konsantrasyon beceriniz nasıl?",
        options: [
            { text: "Çok iyi", value: 5 },
            { text: "Genellikle iyi", value: 4 },
            { text: "Orta seviye", value: 3 },
            { text: "Zayıf", value: 2 },
            { text: "Çok zayıf", value: 1 }
        ]
    },
    {
        id: 6,
        category: "Energy",
        question: "Enerji seviyeniz nasıl?",
        options: [
            { text: "Çok yüksek", value: 5 },
            { text: "Yüksek", value: 4 },
            { text: "Normal", value: 3 },
            { text: "Düşük", value: 2 },
            { text: "Çok düşük", value: 1 }
        ]
    },
    {
        id: 7,
        category: "Stress",
        question: "Stres düzeyiniz nasıl?",
        options: [
            { text: "Çok düşük", value: 5 },
            { text: "Düşük", value: 4 },
            { text: "Orta", value: 3 },
            { text: "Yüksek", value: 2 },
            { text: "Çok yüksek", value: 1 }
        ]
    },
    {
        id: 8,
        category: "Relationships",
        question: "İlişkilerinizden ne kadar memnunsunuz?",
        options: [
            { text: "Çok memnunum", value: 5 },
            { text: "Memnunum", value: 4 },
            { text: "Orta seviye", value: 3 },
            { text: "Memnun değilim", value: 2 },
            { text: "Hiç memnun değilim", value: 1 }
        ]
    },
    {
        id: 9,
        category: "Self-esteem",
        question: "Kendinizi nasıl değerlendiriyorsunuz?",
        options: [
            { text: "Çok olumlu", value: 5 },
            { text: "Olumlu", value: 4 },
            { text: "Nötr", value: 3 },
            { text: "Olumsuz", value: 2 },
            { text: "Çok olumsuz", value: 1 }
        ]
    },
    {
        id: 10,
        category: "Future",
        question: "Geleceğe bakış açınız nasıl?",
        options: [
            { text: "Çok iyimser", value: 5 },
            { text: "İyimser", value: 4 },
            { text: "Kararsız", value: 3 },
            { text: "Karamsar", value: 2 },
            { text: "Çok karamsar", value: 1 }
        ]
    }
];

// Start the test
function startTest() {
    testStartTime = new Date();
    window.location.href = 'test.html';
}

// Show info modal
function showInfo() {
    alert(`Bu Test Hakkında:

✅ Bilimsel olarak doğrulanmış sorular
✅ AI destekli detaylı analiz
✅ Kişiselleştirilmiş öneriler
✅ Tamamen gizli ve güvenli

Test yaklaşık 5-7 dakika sürer ve ruhsal durumunuz hakkında detaylı bilgi verir.

NOT: Bu test tıbbi tanı yerine geçmez. Ciddi durumlar için profesyonel yardım alın.`);
}

// Initialize test page
function initializeTest() {
    testQuestions = [...psychologicalTestQuestions];
    currentQuestion = 0;
    testAnswers = [];
    
    displayQuestion();
}

// Display current question
function displayQuestion() {
    const question = testQuestions[currentQuestion];
    const progressPercent = ((currentQuestion + 1) / testQuestions.length) * 100;
    
    // Update progress bar
    const progressBar = document.querySelector('.test-progress-bar');
    if (progressBar) {
        progressBar.style.width = progressPercent + '%';
    }
    
    // Update question counter
    const questionCounter = document.querySelector('.question-counter');
    if (questionCounter) {
        questionCounter.textContent = `Soru ${currentQuestion + 1} / ${testQuestions.length}`;
    }
    
    // Update question content
    const questionTitle = document.querySelector('.question-title');
    const questionText = document.querySelector('.question-text');
    const answerOptions = document.querySelector('.answer-options');
    
    if (questionTitle) questionTitle.textContent = `${question.category} - Soru ${currentQuestion + 1}`;
    if (questionText) questionText.textContent = question.question;
    
    if (answerOptions) {
        answerOptions.innerHTML = '';
        question.options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.className = 'answer-option';
            optionElement.textContent = option.text;
            optionElement.addEventListener('click', () => selectAnswer(index, option.value));
            answerOptions.appendChild(optionElement);
        });
    }
    
    // Update navigation buttons
    updateNavigationButtons();
}

// Select an answer
function selectAnswer(optionIndex, value) {
    // Remove previous selection
    document.querySelectorAll('.answer-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Add selection to clicked option
    document.querySelectorAll('.answer-option')[optionIndex].classList.add('selected');
    
    // Store answer
    testAnswers[currentQuestion] = {
        questionId: testQuestions[currentQuestion].id,
        category: testQuestions[currentQuestion].category,
        question: testQuestions[currentQuestion].question,
        answer: testQuestions[currentQuestion].options[optionIndex].text,
        value: value
    };
    
    // Enable next button
    const nextButton = document.querySelector('.btn-next');
    if (nextButton) {
        nextButton.disabled = false;
        nextButton.style.opacity = '1';
    }
}

// Navigate to next question
function nextQuestion() {
    if (currentQuestion < testQuestions.length - 1) {
        currentQuestion++;
        displayQuestion();
    } else {
        finishTest();
    }
}

// Navigate to previous question
function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        displayQuestion();
        
        // Restore previous answer if exists
        if (testAnswers[currentQuestion]) {
            const selectedValue = testAnswers[currentQuestion].value;
            const question = testQuestions[currentQuestion];
            const optionIndex = question.options.findIndex(opt => opt.value === selectedValue);
            
            if (optionIndex !== -1) {
                document.querySelectorAll('.answer-option')[optionIndex].classList.add('selected');
                const nextButton = document.querySelector('.btn-next');
                if (nextButton) {
                    nextButton.disabled = false;
                    nextButton.style.opacity = '1';
                }
            }
        }
    }
}

// Update navigation buttons
function updateNavigationButtons() {
    const prevButton = document.querySelector('.btn-prev');
    const nextButton = document.querySelector('.btn-next');
    
    if (prevButton) {
        prevButton.style.display = currentQuestion > 0 ? 'inline-flex' : 'none';
    }
    
    if (nextButton) {
        nextButton.disabled = !testAnswers[currentQuestion];
        nextButton.style.opacity = testAnswers[currentQuestion] ? '1' : '0.5';
        nextButton.textContent = currentQuestion === testQuestions.length - 1 ? 'Testi Bitir' : 'Sonraki Soru';
    }
}

// Finish test and calculate results
async function finishTest() {
    const testEndTime = new Date();
    const testDuration = (testEndTime - testStartTime) / 1000; // in seconds
    
    // Calculate total score
    const totalScore = testAnswers.reduce((sum, answer) => sum + answer.value, 0);
    const maxScore = testQuestions.length * 5;
    const scorePercentage = (totalScore / maxScore) * 100;
    
    // Prepare test results
    const testResults = {
        answers: testAnswers,
        totalScore: totalScore,
        maxScore: maxScore,
        scorePercentage: scorePercentage,
        duration: testDuration,
        completedAt: testEndTime.toISOString()
    };
    
    // Store results in localStorage
    localStorage.setItem('testResults', JSON.stringify(testResults));
    
    // Send results to backend for AI analysis
    try {
        const response = await fetch('/api/analyze-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testResults)
        });
        
        if (response.ok) {
            const analysisResult = await response.json();
            localStorage.setItem('analysisResult', JSON.stringify(analysisResult));
        }
    } catch (error) {
        console.error('Error sending results to backend:', error);
    }
    
    // Redirect to results page
    window.location.href = 'results.html';
}

// Display results on results page
function displayResults() {
    const testResults = JSON.parse(localStorage.getItem('testResults'));
    const analysisResult = JSON.parse(localStorage.getItem('analysisResult'));
    
    if (!testResults) {
        window.location.href = 'index.html';
        return;
    }
    
    // Display score
    const scoreDisplay = document.querySelector('.score-display');
    if (scoreDisplay) {
        const scoreCircle = document.createElement('div');
        scoreCircle.className = 'score-circle';
        scoreCircle.innerHTML = `<span>${Math.round(testResults.scorePercentage)}%</span>`;
        scoreDisplay.appendChild(scoreCircle);
        
        const scoreText = document.createElement('p');
        scoreText.textContent = `Toplam Skor: ${testResults.totalScore}/${testResults.maxScore}`;
        scoreDisplay.appendChild(scoreText);
    }
    
    // Display interpretation
    const interpretation = getScoreInterpretation(testResults.scorePercentage);
    const interpretationElement = document.querySelector('.score-interpretation');
    if (interpretationElement) {
        interpretationElement.innerHTML = `
            <h3>${interpretation.title}</h3>
            <p>${interpretation.description}</p>
        `;
    }
    
    // Display recommendations
    const recommendationsElement = document.querySelector('.recommendations ul');
    if (recommendationsElement) {
        const recommendations = getRecommendations(testResults.scorePercentage);
        recommendationsElement.innerHTML = recommendations.map(rec => `<li>${rec}</li>`).join('');
    }
    
    // Display AI analysis if available
    if (analysisResult && analysisResult.ai_analysis) {
        const aiAnalysisElement = document.querySelector('.ai-analysis');
        if (aiAnalysisElement) {
            aiAnalysisElement.innerHTML = `
                <h3>AI Destekli Analiz</h3>
                <p>${analysisResult.ai_analysis}</p>
            `;
        }
    }
}

// Get score interpretation
function getScoreInterpretation(scorePercentage) {
    if (scorePercentage >= 80) {
        return {
            title: "Mükemmel Ruhsal Durum",
            description: "Test sonuçlarınız, ruhsal sağlığınızın çok iyi durumda olduğunu gösteriyor. Mevcut pozitif yaklaşımınızı sürdürün."
        };
    } else if (scorePercentage >= 60) {
        return {
            title: "İyi Ruhsal Durum",
            description: "Genel olarak iyi bir ruhsal durumdasınız. Bazı alanlarda iyileştirmeler yapabilirsiniz."
        };
    } else if (scorePercentage >= 40) {
        return {
            title: "Orta Seviye Ruhsal Durum",
            description: "Bazı alanlarda zorluklar yaşıyorsunuz. Önerilerimizi takip ederek iyileşme sağlayabilirsiniz."
        };
    } else if (scorePercentage >= 20) {
        return {
            title: "Düşük Ruhsal Durum",
            description: "Ruhsal sağlığınız konusunda dikkat edilmesi gereken alanlar var. Profesyonel destek almanızı öneririz."
        };
    } else {
        return {
            title: "Kritik Ruhsal Durum",
            description: "Test sonuçlarınız ciddi sorunlara işaret ediyor. Lütfen en kısa sürede bir uzmana başvurun."
        };
    }
}

// Get personalized recommendations
function getRecommendations(scorePercentage) {
    const baseRecommendations = [
        "Düzenli egzersiz yapın (haftada en az 3 gün)",
        "Yeterli uyku alın (günde 7-9 saat)",
        "Sağlıklı beslenin ve su tüketimini artırın",
        "Sosyal aktivitelere katılın",
        "Meditasyon veya nefes egzersizleri yapın"
    ];
    
    if (scorePercentage < 40) {
        return [
            ...baseRecommendations,
            "Bir psikoloji uzmanı ile görüşün",
            "Stres yönetimi teknikleri öğrenin",
            "Sevdiğiniz hobiler ile vakit geçirin",
            "Güvendiğiniz kişiler ile konuşun"
        ];
    } else if (scorePercentage < 60) {
        return [
            ...baseRecommendations,
            "Günlük tutma alışkanlığı edinin",
            "Doğada zaman geçirin",
            "Yeni beceriler öğrenin"
        ];
    } else {
        return [
            ...baseRecommendations,
            "Mevcut pozitif alışkanlıklarınızı sürdürün",
            "Başkalarına yardım ederek sosyal bağlarınızı güçlendirin"
        ];
    }
}

// Restart test
function restartTest() {
    if (confirm('Testi yeniden başlatmak istediğinizden emin misiniz? Mevcut sonuçlarınız silinecektir.')) {
        localStorage.removeItem('testResults');
        localStorage.removeItem('analysisResult');
        window.location.href = 'test.html';
    }
}

// Share results
function shareResults() {
    const testResults = JSON.parse(localStorage.getItem('testResults'));
    if (testResults) {
        const shareText = `Psikolojik Test Sonucum: ${Math.round(testResults.scorePercentage)}% - Ruhsal sağlığınızı test etmek için: ${window.location.origin}`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Psikolojik Test Sonucum',
                text: shareText,
                url: window.location.origin
            });
        } else {
            // Fallback for browsers that don't support Web Share API
            navigator.clipboard.writeText(shareText).then(() => {
                alert('Sonuçlar panoya kopyalandı!');
            });
        }
    }
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading animation
function showLoading() {
    const loadingElement = document.createElement('div');
    loadingElement.className = 'loading-overlay';
    loadingElement.innerHTML = `
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Sonuçlarınız analiz ediliyor...</p>
        </div>
    `;
    document.body.appendChild(loadingElement);
}

function hideLoading() {
    const loadingElement = document.querySelector('.loading-overlay');
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Add CSS for loading animation
const loadingStyles = `
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(102, 126, 234, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    color: white;
}

.loading-spinner {
    text-align: center;
}

.loading-spinner i {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.loading-spinner p {
    font-size: 1.2rem;
}
`;

// Add loading styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = loadingStyles;
document.head.appendChild(styleSheet);
