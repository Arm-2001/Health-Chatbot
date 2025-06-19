from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import re
from typing import Dict, List, Any, Optional

app = Flask(__name__)
CORS(app)

class FastHealthAssistant:
    def __init__(self):
        self.doctors = self._load_doctor_data()
        self.conversations = {}
        self.symptom_keywords = self._load_symptom_keywords()
        
    def _load_doctor_data(self) -> List[Dict]:
        return [
            {
                "name": "Malik m Yaseen",
                "category": "Surgeon",
                "experience": "20 years",
                "expertise": "MBBS",
                "phone": "03117031884",
                "address": "KOREA",
                "start_time": "15:52",
                "off_time": "10:52"
            },
            {
                "name": "Alex",
                "category": "Pediatrician",
                "experience": "5 years",
                "expertise": "PEDIATRICIAN",
                "phone": "37383833",
                "address": "ISLAMABAD",
                "start_time": "06:30",
                "off_time": "10:30"
            },
            {
                "name": "Jack",
                "category": "Gastroenterologist",
                "experience": "6 years",
                "expertise": "MBBS",
                "phone": "03125869232",
                "address": "LAHORE",
                "start_time": "12:00",
                "off_time": "08:00"
            },
            {
                "name": "Stephen",
                "category": "Radiologist",
                "experience": "5 years",
                "expertise": "MBBS",
                "phone": "155348990",
                "address": "DothaN",
                "start_time": "03:20",
                "off_time": "11:00"
            },
            {
                "name": "Haris",
                "category": "Oncologist",
                "experience": "20 years",
                "expertise": "MBBS",
                "phone": "03151167096",
                "address": "ISB",
                "start_time": "04:10",
                "off_time": "12:10"
            },
            {
                "name": "Shenza Kaszmi",
                "category": "Oncologist",
                "experience": "8 years",
                "expertise": "FCPS",
                "phone": "0318362512",
                "address": "ISLAMABAD",
                "start_time": "01:00",
                "off_time": "09:00"
            },
            {
                "name": "Alex",
                "category": "Cardiologist",
                "experience": "10 years",
                "expertise": "MBBS FCPS CARDIOLOGIST",
                "phone": "274994268292",
                "address": "LAHORE",
                "start_time": "08:00",
                "off_time": "09:00"
            },
            {
                "name": "Mueen Hery",
                "category": "Cardiologist",
                "experience": "7 years",
                "expertise": "MBBS",
                "phone": "01236986989",
                "address": "DRIILS",
                "start_time": "02:00",
                "off_time": "08:00"
            },
            {
                "name": "Dr Emily Thompson",
                "category": "Neurologist",
                "experience": "3 years",
                "expertise": "FCPS",
                "phone": "61412345678",
                "address": "SYDNEY",
                "start_time": "03:00",
                "off_time": "11:00"
            },
            {
                "name": "Dr Iqra Hayat",
                "category": "Radiologist",
                "experience": "2 years",
                "expertise": "MBBS",
                "phone": "0312583687",
                "address": "ISLAMABAD",
                "start_time": "01:00",
                "off_time": "12:00"
            },
            {
                "name": "Dr Noor Hassan",
                "category": "Neurologist",
                "experience": "4 years",
                "expertise": "FCPS",
                "phone": "96650123",
                "address": "RIYADH",
                "start_time": "16:00",
                "off_time": "10:00"
            },
            {
                "name": "Mam Tayyaba",
                "category": "Nephrologist",
                "experience": "20 years",
                "expertise": "MBBS",
                "phone": "03151167096",
                "address": "ISB",
                "start_time": "12:00",
                "off_time": "08:00"
            },
            {
                "name": "Dr Fatima Zahra",
                "category": "Gynecologist",
                "experience": "5 years",
                "expertise": "MBBS",
                "phone": "97150123456",
                "address": "DUBAI",
                "start_time": "02:00",
                "off_time": "12:00"
            },
            {
                "name": "Dr Peter Andreson",
                "category": "Pulmonologist",
                "experience": "2 years",
                "expertise": "MBBS",
                "phone": "27111234567",
                "address": "NARIRO",
                "start_time": "12:00",
                "off_time": "05:00"
            },
            {
                "name": "Dr Sophie",
                "category": "Pulmonologist",
                "experience": "10 years",
                "expertise": "MBBS",
                "phone": "20100123456",
                "address": "CAIRO",
                "start_time": "05:00",
                "off_time": "10:00"
            },
            {
                "name": "Dr Ayesha Khan",
                "category": "Pediatrician",
                "experience": "7 years",
                "expertise": "MBBS",
                "phone": "03001234567",
                "address": "LAHORE",
                "start_time": "01:00",
                "off_time": "11:00"
            },
            {
                "name": "Dr Maria Rossi",
                "category": "Gynecologist",
                "experience": "5 years",
                "expertise": "MBBS",
                "phone": "3906123456",
                "address": "ROME",
                "start_time": "03:00",
                "off_time": "10:00"
            }
        ]
    
    def _load_symptom_keywords(self) -> Dict:
        return {
            'cardiologist': {
                'primary': ['chest pain', 'heart pain', 'cardiac', 'heart attack', 'heart problem'],
                'secondary': ['chest', 'heart', 'palpitation', 'blood pressure', 'bp', 'hypertension', 'pressure', 'tight chest', 'chest pressure', 'heart beat', 'heart rate'],
                'questions': [
                    "How long have you been experiencing this chest pain?",
                    "Is the pain sharp, dull, or like pressure?",
                    "Does it happen during physical activity or at rest?",
                    "Do you have any history of heart problems?"
                ]
            },
            'gastroenterologist': {
                'primary': ['stomach pain', 'abdominal pain', 'stomach ache', 'belly pain', 'stomach problem'],
                'secondary': ['stomach', 'abdomen', 'belly', 'nausea', 'vomit', 'diarrhea', 'constipation', 'digestive', 'gut', 'bowel', 'gastric'],
                'questions': [
                    "What type of stomach problem are you experiencing?",
                    "How long have you had these stomach issues?",
                    "Is it mainly pain, nausea, or digestive problems?",
                    "Does eating make it better or worse?"
                ]
            },
            'neurologist': {
                'primary': ['headache', 'migraine', 'head pain', 'brain problem', 'neurological problem'],
                'secondary': ['head', 'dizzy', 'dizziness', 'memory', 'confusion', 'seizure', 'nervous', 'brain', 'concentration'],
                'questions': [
                    "How severe is your headache on a scale of 1-10?",
                    "How often do you get these headaches?",
                    "Do you experience any dizziness or nausea with the headache?",
                    "Is this a new type of headache for you?"
                ]
            },
            'pulmonologist': {
                'primary': ['breathing problem', 'lung problem', 'respiratory problem', 'shortness of breath'],
                'secondary': ['breath', 'breathing', 'cough', 'lung', 'respiratory', 'asthma', 'pneumonia', 'chest congestion'],
                'questions': [
                    "What kind of breathing difficulties are you having?",
                    "Do you have a persistent cough?",
                    "How long have you been experiencing breathing problems?",
                    "Do you have any history of asthma or lung problems?"
                ]
            },
            'pediatrician': {
                'primary': ['child sick', 'baby sick', 'kid problem', 'child problem', 'infant problem'],
                'secondary': ['child', 'baby', 'kid', 'infant', 'toddler', 'son', 'daughter', 'children', 'pediatric'],
                'questions': [
                    "How old is your child?",
                    "What symptoms is your child showing?",
                    "How long has your child been unwell?",
                    "Does your child have a fever?"
                ]
            },
            'gynecologist': {
                'primary': ['pregnancy problem', 'menstrual problem', 'period problem', 'women health problem'],
                'secondary': ['pregnant', 'pregnancy', 'period', 'menstrual', 'reproductive', 'women', 'female', 'uterus', 'ovarian'],
                'questions': [
                    "What specific women's health concern do you have?",
                    "Are you currently pregnant or trying to conceive?",
                    "How are your menstrual cycles?",
                    "Is this related to pregnancy or general women's health?"
                ]
            },
            'nephrologist': {
                'primary': ['kidney problem', 'urinary problem', 'kidney pain', 'urine problem'],
                'secondary': ['kidney', 'urine', 'urinary', 'bladder', 'renal', 'dialysis'],
                'questions': [
                    "What kind of kidney or urinary problems are you experiencing?",
                    "Do you have pain while urinating?",
                    "How often do you need to urinate?",
                    "Have you noticed changes in your urine color or amount?"
                ]
            }
        }
    
    def _extract_age_info(self, text: str) -> Optional[int]:
        """Extract age information from text"""
        age_patterns = [
            r'(\d+)\s*(?:years?\s*old|yrs?\s*old|year|yr)',
            r'age\s*(\d+)',
            r'(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        return None
    
    def _extract_duration(self, text: str) -> str:
        """Extract duration information from text"""
        duration_patterns = [
            r'(\d+)\s*(?:days?|weeks?|months?|years?)',
            r'(yesterday|today|last night|this morning)',
            r'(few days|several days|long time|while now)',
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)
        return "not specified"
    
    def _extract_severity(self, text: str) -> str:
        """Extract severity information from text"""
        if any(word in text.lower() for word in ['severe', 'terrible', 'unbearable', '9', '10']):
            return "severe"
        elif any(word in text.lower() for word in ['moderate', 'medium', '5', '6', '7']):
            return "moderate"
        elif any(word in text.lower() for word in ['mild', 'light', 'little', '1', '2', '3']):
            return "mild"
        return "not specified"
    
    def _analyze_symptoms(self, text: str) -> List[str]:
        """Analyze text and return matching medical specialties"""
        text_lower = text.lower()
        matches = []
        
        for specialty, keywords in self.symptom_keywords.items():
            score = 0
            
            # Check primary keywords (higher weight)
            for keyword in keywords['primary']:
                if keyword in text_lower:
                    score += 3
            
            # Check secondary keywords (lower weight)
            for keyword in keywords['secondary']:
                if keyword in text_lower:
                    score += 1
            
            if score > 0:
                matches.append((specialty, score))
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x[1], reverse=True)
        return [match[0] for match in matches[:3]]
    
    def _get_next_question(self, specialty: str, answered_questions: List[str]) -> Optional[str]:
        """Get the next question to ask for a specialty"""
        if specialty not in self.symptom_keywords:
            return None
        
        questions = self.symptom_keywords[specialty]['questions']
        for question in questions:
            if question not in answered_questions:
                return question
        return None
    
    def _recommend_doctors(self, specialties: List[str], user_preferences: Dict = None) -> List[Dict]:
        """Recommend doctors based on specialties"""
        recommended = []
        
        for specialty in specialties:
            specialty_doctors = [doc for doc in self.doctors if doc['category'].lower() == specialty.lower()]
            if specialty_doctors:
                # Sort by experience
                specialty_doctors.sort(key=lambda x: int(x['experience'].split()[0]), reverse=True)
                recommended.extend(specialty_doctors[:2])  # Top 2 doctors per specialty
        
        # Remove duplicates
        seen = set()
        unique_doctors = []
        for doc in recommended:
            if doc['name'] not in seen:
                seen.add(doc['name'])
                unique_doctors.append(doc)
        
        return unique_doctors[:3]  # Return top 3 overall
    
    def _format_doctor_recommendation(self, doctors: List[Dict], context: str = "") -> str:
        """Format doctor recommendations"""
        if not doctors:
            return "I apologize, but I couldn't find suitable doctors for your condition. Please try contacting a general practitioner."
        
        response = f"{context}\n\n" if context else ""
        response += "**RECOMMENDED DOCTORS:**\n\n"
        
        for i, doctor in enumerate(doctors, 1):
            response += f"**{i}. Dr. {doctor['name']}** - {doctor['category']}\n"
            response += f"• Experience: {doctor['experience']} | Expertise: {doctor['expertise']}\n"
            response += f"• Phone: {doctor['phone']} | Location: {doctor['address']}\n"
            response += f"• Available: {doctor['start_time']} to {doctor['off_time']}\n\n"
        
        response += "I recommend calling to schedule an appointment. Take care of your health!"
        return response
    
    def process_message(self, user_input: str, session_id: str) -> str:
        """Process user message and return appropriate response"""
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'stage': 'greeting',
                'symptoms': [],
                'specialties': [],
                'answered_questions': [],
                'user_info': {
                    'age': None,
                    'duration': None,
                    'severity': None,
                    'location': None
                },
                'messages': []
            }
        
        conversation = self.conversations[session_id]
        user_input_clean = user_input.strip()
        
        # Store message
        conversation['messages'].append({'user': user_input, 'timestamp': datetime.datetime.now()})
        
        # Handle greetings
        if conversation['stage'] == 'greeting' or user_input.lower().strip() in ['hi', 'hello', 'hey', 'sup']:
            conversation['stage'] = 'initial_assessment'
            return "Hello! I'm your health assistant. I'm here to help you find the right doctor. How are you feeling today? What's bothering you?"
        
        # Extract information from user input
        age = self._extract_age_info(user_input_clean)
        duration = self._extract_duration(user_input_clean)
        severity = self._extract_severity(user_input_clean)
        
        if age:
            conversation['user_info']['age'] = age
        if duration != "not specified":
            conversation['user_info']['duration'] = duration
        if severity != "not specified":
            conversation['user_info']['severity'] = severity
        
        # Analyze symptoms
        detected_specialties = self._analyze_symptoms(user_input_clean)
        if detected_specialties:
            conversation['specialties'].extend(detected_specialties)
            conversation['specialties'] = list(set(conversation['specialties']))  # Remove duplicates
        
        # Determine response based on stage
        if conversation['stage'] == 'initial_assessment':
            if detected_specialties:
                conversation['stage'] = 'gathering_details'
                primary_specialty = detected_specialties[0]
                
                # Get first question for the primary specialty
                next_question = self._get_next_question(primary_specialty, conversation['answered_questions'])
                
                if next_question:
                    conversation['answered_questions'].append(next_question)
                    return f"I understand you're dealing with {user_input_clean}. That sounds concerning. {next_question}"
                else:
                    # No more questions, recommend doctors
                    conversation['stage'] = 'recommendation'
                    doctors = self._recommend_doctors(conversation['specialties'])
                    return self._format_doctor_recommendation(doctors, "Based on what you've told me, here are some doctors who can help:")
            else:
                return "Could you tell me more specifically what symptoms you're experiencing? For example, are you having pain anywhere, feeling nauseous, having trouble breathing, or experiencing something else?"
        
        elif conversation['stage'] == 'gathering_details':
            # Check if we have enough information or should ask more questions
            primary_specialty = conversation['specialties'][0] if conversation['specialties'] else None
            
            if primary_specialty and len(conversation['answered_questions']) < 3:
                next_question = self._get_next_question(primary_specialty, conversation['answered_questions'])
                
                if next_question:
                    conversation['answered_questions'].append(next_question)
                    return f"Thank you for that information. {next_question}"
            
            # We have enough information, recommend doctors
            conversation['stage'] = 'recommendation'
            doctors = self._recommend_doctors(conversation['specialties'])
            
            # Create context based on gathered information
            context_parts = []
            if conversation['user_info']['severity'] and conversation['user_info']['severity'] != "not specified":
                context_parts.append(f"severity: {conversation['user_info']['severity']}")
            if conversation['user_info']['duration'] and conversation['user_info']['duration'] != "not specified":
                context_parts.append(f"duration: {conversation['user_info']['duration']}")
            
            context = "Based on your symptoms"
            if context_parts:
                context += f" ({', '.join(context_parts)})"
            context += ", here are some doctors I recommend:"
            
            return self._format_doctor_recommendation(doctors, context)
        
        elif conversation['stage'] == 'recommendation':
            # Post-recommendation stage
            if any(word in user_input.lower() for word in ['thank', 'thanks', 'appreciate']):
                return "You're very welcome! I hope you feel better soon. Don't hesitate to reach out if you need help finding other doctors or have any health concerns."
            elif any(word in user_input.lower() for word in ['more', 'other', 'different', 'alternative']):
                # User wants more options
                all_doctors = self._recommend_doctors(conversation['specialties'])
                if len(all_doctors) > 3:
                    return self._format_doctor_recommendation(all_doctors[3:6], "Here are some additional doctors you might consider:")
                else:
                    return "Those were the top recommendations for your condition. You might also want to check with your local hospital or clinic for more options in your area."
            elif any(word in user_input.lower() for word in ['new', 'different', 'another']) and any(word in user_input.lower() for word in ['problem', 'issue', 'symptom']):
                # New health issue
                conversation['stage'] = 'initial_assessment'
                conversation['symptoms'] = []
                conversation['specialties'] = []
                conversation['answered_questions'] = []
                return "I understand you have a different health concern. What new symptoms or problems are you experiencing?"
            else:
                return "Is there anything specific you'd like to know about these doctors, or do you have any other health concerns I can help you with?"
        
        # Default fallback
        return "I'm here to help you find the right doctor for your health concerns. Could you tell me what symptoms you're experiencing?"

# Initialize the fast health assistant
health_assistant = FastHealthAssistant()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'response': 'Hello! I\'m your health assistant. How can I help you today?',
                'session_id': 'error',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', f'session_{datetime.datetime.now().timestamp()}')
        
        if not user_message:
            return jsonify({
                'response': 'Hi! I\'m here to help you find the right doctor. How are you feeling today?',
                'session_id': session_id,
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        print(f"Fast processing: '{user_message}' for session: {session_id}")
        
        response_text = health_assistant.process_message(user_message, session_id)
        
        return jsonify({
            'response': response_text,
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'Hi! I\'m here to help you find the right doctor for your health concerns. What\'s bothering you today?',
            'session_id': 'error_session',
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Fast Rule-Based Health Assistant',
        'timestamp': datetime.datetime.now().isoformat(),
        'doctors_loaded': len(health_assistant.doctors),
        'specialties': list(health_assistant.symptom_keywords.keys())
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Fast Rule-Based Health Assistant Chatbot',
        'status': 'online',
        'type': 'rule-based (no external APIs)',
        'features': [
            'Lightning fast responses',
            'Interactive symptom assessment',
            'Smart data extraction',
            'Contextual doctor recommendations',
            'No timeouts or delays'
        ],
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/health (GET)'
        },
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"⚡ Starting Fast Health Assistant Chatbot on port {port}")
    print(f"👨‍⚕️ Loaded {len(health_assistant.doctors)} doctors")
    print(f"🧠 Loaded {len(health_assistant.symptom_keywords)} medical specialties")
    print("🚀 Ready for lightning-fast conversations!")
    app.run(host='0.0.0.0', port=port, debug=False)
