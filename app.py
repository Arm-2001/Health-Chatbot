from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import datetime
import os
import re
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)

class HealthAssistantChatbot:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', 'your_openrouter_api_key_here')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1"
        
        self.doctors = self._load_doctor_data()
        self.conversations = {}
        self.system_prompt = self._create_system_prompt()
        
    def _load_doctor_data(self) -> List[Dict]:
        doctors = [
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
        
        return doctors
    
    def _create_system_prompt(self) -> str:
        doctor_catalog = "COMPLETE DOCTOR DATABASE:\n\n"
        
        for doctor in self.doctors:
            doctor_catalog += f"• {doctor['name']}\n"
            doctor_catalog += f"  Category: {doctor['category']}\n"
            doctor_catalog += f"  Experience: {doctor['experience']}\n"
            doctor_catalog += f"  Expertise: {doctor['expertise']}\n"
            doctor_catalog += f"  Phone: {doctor['phone']}\n"
            doctor_catalog += f"  Address: {doctor['address']}\n"
            doctor_catalog += f"  Start Time: {doctor['start_time']}\n"
            doctor_catalog += f"  Off Time: {doctor['off_time']}\n\n"
        
        return f"""You are a professional health assistant chatbot that helps patients find the right doctor based on their symptoms and health concerns.

{doctor_catalog}

YOUR ROLE:
1. When a patient first contacts you, greet them warmly and ask about their health concerns
2. Ask 3-4 relevant health questions to understand their condition:
   - What are your main symptoms?
   - How long have you been experiencing these symptoms?
   - What part of your body is affected?
   - Any specific concerns or previous medical history?
3. Based on their answers, recommend the MOST SUITABLE doctor from the database
4. Always be empathetic, professional, and helpful

IMPORTANT RESPONSE FORMAT for doctor recommendations:
When recommending a doctor, use this EXACT format:

**RECOMMENDED DOCTOR:**
• Name: [Doctor Name]
  Specialty: [Category]
  Experience: [Experience]
  Expertise: [Expertise]
  Phone: [Phone Number]
  Address: [Address]
  Available: [Start Time] to [Off Time]

DOCTOR SPECIALTIES GUIDE:
- Cardiologist: Heart problems, chest pain, blood pressure
- Neurologist: Brain, nervous system, headaches, seizures
- Gastroenterologist: Stomach, digestive issues, abdominal pain
- Pediatrician: Children's health (under 18 years)
- Gynecologist: Women's reproductive health
- Oncologist: Cancer-related concerns
- Radiologist: Imaging, scans, X-rays
- Surgeon: Surgical procedures, injuries
- Pulmonologist: Lung problems, breathing issues
- Nephrologist: Kidney problems

RULES:
- Always ask health questions before recommending
- Be empathetic and professional
- Only recommend ONE doctor per consultation
- Consider location preferences if mentioned
- Ask follow-up questions if symptoms are unclear
- Never provide medical diagnosis - only doctor recommendations

Remember: You are helping connect patients with the right healthcare professional based on their symptoms and needs."""

    def _analyze_symptoms_and_recommend(self, symptoms: str, conversation_history: List) -> Dict:
        """Analyze symptoms and recommend the best doctor"""
        symptoms_lower = symptoms.lower()
        
        # Define symptom-to-specialty mapping
        specialty_keywords = {
            'cardiologist': ['heart', 'chest pain', 'blood pressure', 'cardiac', 'heart attack', 'palpitations', 'hypertension'],
            'neurologist': ['headache', 'migraine', 'brain', 'seizure', 'memory', 'nervous', 'neurological', 'stroke', 'epilepsy'],
            'gastroenterologist': ['stomach', 'abdomen', 'digestive', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'gastric'],
            'pediatrician': ['child', 'baby', 'infant', 'kid', 'toddler', 'under 18', 'pediatric'],
            'gynecologist': ['pregnancy', 'menstrual', 'reproductive', 'gynecological', 'uterus', 'ovarian', 'period'],
            'oncologist': ['cancer', 'tumor', 'chemotherapy', 'oncology', 'malignant', 'benign', 'biopsy'],
            'radiologist': ['scan', 'x-ray', 'mri', 'ct scan', 'imaging', 'radiology'],
            'surgeon': ['surgery', 'operation', 'surgical', 'trauma', 'accident', 'injury', 'wound'],
            'pulmonologist': ['lung', 'breathing', 'cough', 'asthma', 'pneumonia', 'respiratory', 'shortness of breath'],
            'nephrologist': ['kidney', 'urine', 'dialysis', 'renal', 'urinary', 'nephrology']
        }
        
        # Find matching specialty
        best_specialty = None
        max_matches = 0
        
        for specialty, keywords in specialty_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in symptoms_lower)
            if matches > max_matches:
                max_matches = matches
                best_specialty = specialty
        
        # If no clear match, look at conversation history for more context
        if not best_specialty:
            full_conversation = " ".join([msg.get('user', '') + " " + msg.get('assistant', '') for msg in conversation_history])
            for specialty, keywords in specialty_keywords.items():
                matches = sum(1 for keyword in keywords if keyword in full_conversation.lower())
                if matches > max_matches:
                    max_matches = matches
                    best_specialty = specialty
        
        # Find doctors with matching specialty
        if best_specialty:
            matching_doctors = [doc for doc in self.doctors if doc['category'].lower() == best_specialty]
            if matching_doctors:
                # Prefer doctors with more experience
                best_doctor = max(matching_doctors, key=lambda x: int(x['experience'].split()[0]))
                return best_doctor
        
        # Fallback to general practitioner or most experienced doctor
        return max(self.doctors, key=lambda x: int(x['experience'].split()[0]))

    def _format_doctor_response(self, doctor: Dict, context: str = "") -> str:
        """Format doctor recommendation in the exact format expected"""
        response = context
        if context and not context.endswith('\n'):
            response += "\n\n"
        
        response += "**RECOMMENDED DOCTOR:**\n"
        response += f"• Name: {doctor['name']}\n"
        response += f"  Specialty: {doctor['category']}\n"
        response += f"  Experience: {doctor['experience']}\n"
        response += f"  Expertise: {doctor['expertise']}\n"
        response += f"  Phone: {doctor['phone']}\n"
        response += f"  Address: {doctor['address']}\n"
        response += f"  Available: {doctor['start_time']} to {doctor['off_time']}\n\n"
        response += "Please call to schedule an appointment. Take care of your health!"
        
        return response

    def process_query(self, user_input: str, session_id: str = "default") -> str:
        """Process user query with health assessment and doctor recommendation"""
        
        if session_id not in self.conversations:
            self.conversations[session_id] = {'messages': [], 'questions_asked': 0, 'symptoms_collected': False}
        
        conversation = self.conversations[session_id]
        user_input_lower = user_input.lower().strip()
        
        # Handle greetings
        greetings = ['hi', 'hello', 'hey', 'sup', 'hii', 'helo']
        if user_input_lower in greetings:
            response = "Hello! I'm your health assistant. I'm here to help you find the right doctor based on your symptoms and health concerns. How are you feeling today? What brings you here?"
            conversation['messages'].append({'user': user_input, 'assistant': response})
            return response
        
        # Handle very short inputs
        if len(user_input.strip()) < 2:
            response = "I'm here to help you find the right doctor for your health concerns. Please tell me about your symptoms or what's bothering you."
            conversation['messages'].append({'user': user_input, 'assistant': response})
            return response

        # If this is the first health-related query, start assessment
        if conversation['questions_asked'] == 0:
            response = f"I understand you're experiencing: {user_input}\n\nTo help you find the best doctor, I need to ask you a few questions:\n\n1. How long have you been experiencing these symptoms?\n2. Can you describe the severity (mild, moderate, severe)?\n3. What part of your body is most affected?\n\nPlease answer these questions so I can recommend the most suitable doctor for you."
            conversation['questions_asked'] = 1
            conversation['messages'].append({'user': user_input, 'assistant': response})
            return response
        
        # If we've asked initial questions but need more info
        elif conversation['questions_asked'] < 3 and not conversation['symptoms_collected']:
            follow_up_questions = [
                "Thank you for that information. Are there any other symptoms you're experiencing? Any pain, discomfort, or changes you've noticed?",
                "That's helpful. Do you have any previous medical history related to this condition? Any medications you're currently taking?",
                "Based on what you've told me, I have enough information to recommend a suitable doctor."
            ]
            
            if conversation['questions_asked'] < len(follow_up_questions):
                response = follow_up_questions[conversation['questions_asked'] - 1]
                conversation['questions_asked'] += 1
                conversation['messages'].append({'user': user_input, 'assistant': response})
                
                # If we've asked enough questions, prepare for recommendation
                if conversation['questions_asked'] >= 3:
                    conversation['symptoms_collected'] = True
                
                return response
        
        # Now recommend a doctor based on collected information
        if conversation['symptoms_collected'] or conversation['questions_asked'] >= 3:
            # Collect all user inputs to analyze symptoms
            all_symptoms = " ".join([msg['user'] for msg in conversation['messages']] + [user_input])
            
            # Find the best doctor
            recommended_doctor = self._analyze_symptoms_and_recommend(all_symptoms, conversation['messages'])
            
            context = "Based on your symptoms and health concerns, here's my recommendation:"
            response = self._format_doctor_response(recommended_doctor, context)
            
            conversation['messages'].append({'user': user_input, 'assistant': response})
            
            # Reset for new consultation
            conversation['questions_asked'] = 0
            conversation['symptoms_collected'] = False
            
            return response

        # Try AI API for more natural conversation
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            recent_history = conversation['messages'][-4:] if len(conversation['messages']) > 4 else conversation['messages']
            for msg in recent_history:
                messages.append({"role": "user", "content": msg['user']})
                messages.append({"role": "assistant", "content": msg['assistant']})
            
            messages.append({"role": "user", "content": user_input})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 500,
                "top_p": 0.9
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and result['choices'] and result['choices'][0]['message']['content'].strip():
                ai_response = result['choices'][0]['message']['content'].strip()
                
                conversation['messages'].append({'user': user_input, 'assistant': ai_response})
                
                # Clean up conversation history
                if len(conversation['messages']) > 10:
                    conversation['messages'] = conversation['messages'][-8:]
                
                return ai_response
                
        except Exception as e:
            print(f"AI API error: {str(e)}")
            # Fall through to fallback response

        # Fallback response
        response = "I understand your concern. To provide you with the best doctor recommendation, could you please tell me more about your symptoms? What specific health issues are you experiencing?"
        conversation['messages'].append({'user': user_input, 'assistant': response})
        return response

# Initialize chatbot
chatbot = HealthAssistantChatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'response': 'Please send a valid message!',
                'session_id': 'error',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
            
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', f'health_session_{datetime.datetime.now().timestamp()}')
        
        if not user_message:
            return jsonify({
                'response': 'Hi! I\'m your health assistant. Please tell me about your symptoms or health concerns so I can help you find the right doctor.',
                'session_id': session_id,
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        print(f"Processing health query: '{user_message}' for session: {session_id}")
        
        # Process the query
        response_text = chatbot.process_query(user_message, session_id)
        
        print(f"Generated response: {response_text[:100]}...")
        
        return jsonify({
            'response': response_text,
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'I\'m here to help you find the right doctor for your health concerns. Please tell me about your symptoms.',
            'session_id': 'error_session',
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'Health Assistant AI',
        'timestamp': datetime.datetime.now().isoformat(),
        'doctors_loaded': len(chatbot.doctors)
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Health Assistant Chatbot API',
        'status': 'online',
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/health (GET)'
        },
        'usage': 'Send POST request to /api/chat with {"message": "your health concern", "session_id": "optional_session_id"}',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🏥 Starting Health Assistant Chatbot on port {port}")
    print(f"👨‍⚕️ Loaded {len(chatbot.doctors)} doctors")
    print("Available specialties:", set([doc['category'] for doc in chatbot.doctors]))
    app.run(host='0.0.0.0', port=port, debug=False)
