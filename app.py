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
        self.model = "deepseek/deepseek-r1:free"  # Using DeepSeek R1 free tier
        
        self.doctors = self._load_doctor_data()
        self.conversations = {}
        
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
        """Create a dynamic system prompt for natural conversation"""
        
        doctor_catalog = "AVAILABLE DOCTORS DATABASE:\n\n"
        for doctor in self.doctors:
            doctor_catalog += f"• {doctor['name']} - {doctor['category']}\n"
            doctor_catalog += f"  Experience: {doctor['experience']}, Expertise: {doctor['expertise']}\n"
            doctor_catalog += f"  Phone: {doctor['phone']}, Address: {doctor['address']}\n"
            doctor_catalog += f"  Available: {doctor['start_time']} to {doctor['off_time']}\n\n"
        
        return f"""You are a friendly, professional health assistant chatbot that helps patients find suitable doctors. You should be conversational, empathetic, and natural - like talking to a helpful medical receptionist or nurse.

{doctor_catalog}

SPECIALTIES GUIDE:
- Cardiologist: Heart issues, chest pain, blood pressure, palpitations, heart conditions
- Neurologist: Brain/nervous system, headaches, migraines, seizures, memory problems, dizziness
- Gastroenterologist: Stomach, digestive issues, abdominal pain, nausea, liver problems, bowel issues
- Pediatrician: Children's health (under 18), baby/infant care, childhood diseases
- Gynecologist: Women's reproductive health, pregnancy, menstrual issues, female health concerns
- Oncologist: Cancer concerns, tumors, follow-up care, chemotherapy support
- Radiologist: Medical imaging, X-rays, MRI, CT scans, diagnostic imaging
- Surgeon: Surgical procedures, injuries, trauma, operations, wounds
- Pulmonologist: Lung problems, breathing issues, asthma, cough, respiratory conditions
- Nephrologist: Kidney problems, urinary issues, kidney stones, dialysis

YOUR APPROACH:
1. **Be naturally conversational** - respond to what the user actually says, don't force a rigid pattern
2. **Listen and adapt** - if they want to chat first, chat. If they have urgent symptoms, focus on that
3. **Ask clarifying questions naturally** - only when needed, like a human would
4. **Recommend multiple doctors when appropriate** - give options, not just one
5. **Be empathetic** - acknowledge their concerns and feelings
6. **Don't be robotic** - avoid overly structured responses unless they specifically want that

WHEN TO RECOMMEND DOCTORS:
- When user mentions specific symptoms or health concerns
- When they ask for doctor recommendations
- When you have enough information to make good suggestions
- If they seem ready for recommendations (don't force it)

RESPONSE STYLES:
- **Casual chat**: Be friendly and conversational
- **Health concerns**: Be more focused but still warm
- **Urgent symptoms**: Be direct but caring
- **Follow-up questions**: Ask naturally, not like a form

RECOMMENDATION FORMAT (use when appropriate):
**Here are some doctors who could help:**

**[Doctor Name]** - [Specialty]
• Experience: [Years] | Expertise: [Qualifications]  
• Phone: [Phone Number] | Location: [Address]
• Available: [Start Time] to [End Time]

**[Another Doctor]** - [Specialty]
• [similar format]

End with: "Would you like me to tell you more about any of these doctors, or do you have other questions?"

IMPORTANT RULES:
- Respond naturally to whatever the user says
- Don't force them through a rigid questionnaire 
- Be human-like in your responses
- Ask for clarification only when genuinely needed
- Recommend 2-3 doctors when you have enough info
- Handle casual conversation naturally
- Be empathetic about health concerns
- Don't be overly formal or robotic"""

    def _call_deepseek_api(self, messages: List[Dict], max_tokens: int = 500) -> str:
        """Call DeepSeek API with improved error handling"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",  # Required for free tier
                "X-Title": "Health Assistant Chatbot"      # Optional but helpful
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.6,  # Slightly higher for more natural responses
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
            
            print(f"Calling API with model: {self.model}")
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=15)  # Reduced timeout
            
            # Better error handling
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and result['choices'] and result['choices'][0]['message']['content'].strip():
                    return result['choices'][0]['message']['content'].strip()
                else:
                    print("API returned empty response")
                    return None
            elif response.status_code == 402:
                print("Payment required - free tier limit may be exceeded")
                return None
            elif response.status_code == 429:
                print("Rate limit exceeded - please wait before making more requests")
                return None
            else:
                print(f"API error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"DeepSeek API error: {str(e)}")
            return None

    def _analyze_symptoms_and_recommend_fallback(self, user_input: str, conversation_history: List) -> str:
        """Enhanced fallback system with intelligent doctor recommendations"""
        user_lower = user_input.lower()
        all_conversation = user_input.lower()
        
        # Include conversation history for better context
        if conversation_history:
            recent_messages = " ".join([msg.get('user', '') for msg in conversation_history[-3:]])
            all_conversation = (recent_messages + " " + user_input).lower()
        
        # Enhanced symptom-to-specialty mapping
        specialty_keywords = {
            'cardiologist': ['chest pain', 'heart', 'cardiac', 'blood pressure', 'palpitations', 'bp', 'hypertension', 'chest hurt', 'heart beat', 'chest pressure', 'chest tight'],
            'gastroenterologist': ['stomach', 'abdomen', 'belly', 'digestive', 'nausea', 'vomit', 'diarrhea', 'constipation', 'gastric', 'bowel', 'liver', 'gut', 'stomach pain', 'abdominal pain'],
            'neurologist': ['headache', 'migraine', 'brain', 'seizure', 'memory', 'nervous', 'dizzy', 'head hurt', 'head pain', 'confusion', 'dizziness'],
            'pediatrician': ['child', 'baby', 'infant', 'kid', 'toddler', 'pediatric', 'my son', 'my daughter', 'children'],
            'gynecologist': ['pregnancy', 'pregnant', 'menstrual', 'period', 'reproductive', 'uterus', 'ovarian', 'women health'],
            'oncologist': ['cancer', 'tumor', 'chemotherapy', 'oncology', 'malignant', 'biopsy', 'mass'],
            'pulmonologist': ['lung', 'breathing', 'cough', 'asthma', 'pneumonia', 'respiratory', 'shortness of breath', 'chest congestion', 'breath'],
            'nephrologist': ['kidney', 'urine', 'urinary', 'dialysis', 'renal', 'bladder'],
            'surgeon': ['surgery', 'operation', 'surgical', 'trauma', 'accident', 'injury', 'wound', 'cut', 'broken'],
            'radiologist': ['scan', 'x-ray', 'mri', 'ct scan', 'imaging', 'xray']
        }
        
        # Find matching specialties with better scoring
        specialty_scores = {}
        for specialty, keywords in specialty_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in all_conversation:
                    # Give higher score for exact phrase matches
                    if len(keyword.split()) > 1:
                        score += 3  # Multi-word phrases get higher score
                    else:
                        score += 1
            if score > 0:
                specialty_scores[specialty] = score
        
        # Sort by relevance (score)
        matching_specialties = sorted(specialty_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get recommended doctors
        recommended_doctors = []
        
        if matching_specialties:
            # Get doctors for top matching specialties
            for specialty, score in matching_specialties[:2]:
                specialty_doctors = [doc for doc in self.doctors if doc['category'].lower() == specialty]
                if specialty_doctors:
                    # Sort by experience and take top doctors
                    specialty_doctors.sort(key=lambda x: int(x['experience'].split()[0]), reverse=True)
                    recommended_doctors.extend(specialty_doctors[:2])
        
        # If no specific matches, recommend experienced general doctors
        if not recommended_doctors:
            all_doctors_sorted = sorted(self.doctors, key=lambda x: int(x['experience'].split()[0]), reverse=True)
            recommended_doctors = all_doctors_sorted[:3]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_doctors = []
        for doc in recommended_doctors:
            if doc['name'] not in seen:
                seen.add(doc['name'])
                unique_doctors.append(doc)
        
        # Create contextual response based on symptoms
        if 'chest pain' in all_conversation or ('chest' in all_conversation and 'pain' in all_conversation):
            intro = "Chest pain should definitely be evaluated by a medical professional. Based on your symptoms, here are some cardiologists I'd recommend:"
        elif 'stomach' in all_conversation:
            intro = "For stomach issues, I'd recommend seeing a gastroenterologist. Here are some excellent options:"
        elif 'headache' in all_conversation or 'head' in all_conversation:
            intro = "For persistent headaches, a neurologist would be the best choice. Here are some specialists:"
        else:
            intro = "Based on your symptoms, here are some doctors who could help:"
        
        response = f"{intro}\n\n**RECOMMENDED DOCTORS:**\n\n"
        
        for i, doctor in enumerate(unique_doctors[:3], 1):
            response += f"**{i}. Dr. {doctor['name']}** - {doctor['category']}\n"
            response += f"• Experience: {doctor['experience']} | Expertise: {doctor['expertise']}\n"
            response += f"• Phone: {doctor['phone']} | Location: {doctor['address']}\n"
            response += f"• Available: {doctor['start_time']} to {doctor['off_time']}\n\n"
        
        response += "I'd recommend calling to schedule an appointment. Is there anything specific you'd like to know about any of these doctors?"
        
        return response

    def _should_recommend_doctors(self, user_input: str, conversation_history: List) -> bool:
        """Intelligently decide if we should recommend doctors based on context"""
        user_lower = user_input.lower()
        
        # Direct requests for recommendations
        direct_requests = ['recommend', 'suggest', 'find doctor', 'need doctor', 'doctor for', 'who should i see']
        if any(phrase in user_lower for phrase in direct_requests):
            return True
        
        # Health symptoms mentioned
        health_indicators = [
            'pain', 'hurt', 'sick', 'symptoms', 'problem', 'issue', 'concern',
            'fever', 'headache', 'stomach', 'chest', 'breathing', 'cough',
            'dizzy', 'nausea', 'vomit', 'diarrhea', 'constipation', 'rash',
            'swelling', 'infection', 'injury', 'accident', 'broken', 'sprain',
            'heart', 'lung', 'kidney', 'liver', 'brain', 'nervous',
            'pregnant', 'pregnancy', 'menstrual', 'period',
            'child', 'baby', 'infant', 'kid', 'pediatric'
        ]
        
        # Check if user mentioned health issues
        health_mentioned = any(word in user_lower for word in health_indicators)
        
        # Look at conversation context - if they've been discussing health for a while
        if conversation_history:
            recent_conversation = " ".join([msg.get('user', '') + ' ' + msg.get('assistant', '') 
                                         for msg in conversation_history[-3:]])
            context_health = any(word in recent_conversation.lower() for word in health_indicators)
            
            # If health has been discussed and user provides more details
            if context_health and len(user_input.split()) > 3:
                return True
        
        return health_mentioned

    def _get_smart_fallback(self, user_input: str, conversation_history: List) -> str:
        """Provide contextual fallback responses with natural conversation"""
        user_lower = user_input.lower()
        
        # Handle greetings
        if any(greeting in user_lower for greeting in ['hi', 'hello', 'hey', 'sup']):
            return "Hello! I'm here to help you find the right doctor for any health concerns. How can I assist you today?"
        
        # Handle thanks/goodbye
        if any(word in user_lower for word in ['thanks', 'thank you', 'bye', 'goodbye']):
            return "You're welcome! Take care of your health, and don't hesitate to reach out if you need any doctor recommendations."
        
        # Handle "how are you"
        if 'how are you' in user_lower:
            return "I'm doing well, thank you for asking! I'm here to help you with any health concerns or doctor recommendations. How are you feeling?"
        
        # For health symptoms - ask follow-up questions naturally first
        health_symptoms = ['pain', 'hurt', 'sick', 'symptoms', 'problem', 'ache', 'sore', 'fever', 'headache', 'stomach', 'chest', 'breathing', 'cough', 'dizzy', 'nausea']
        
        if any(symptom in user_lower for symptom in health_symptoms):
            # Check if this is first mention or if we need more info
            if not conversation_history or len(conversation_history) < 2:
                # Ask natural follow-up questions first
                if 'chest' in user_lower and 'pain' in user_lower:
                    return "I'm sorry to hear about your chest pain. That's definitely something to take seriously. How long have you been experiencing this chest pain? Is it sharp, dull, or more like pressure?"
                elif 'stomach' in user_lower:
                    return "Sorry to hear about your stomach troubles. Can you tell me more about what kind of stomach issues you're having? Is it pain, nausea, or something else?"
                elif 'headache' in user_lower or 'head' in user_lower:
                    return "Headaches can be really uncomfortable. How severe would you say this headache is, and how long have you been dealing with it?"
                elif 'breathing' in user_lower or 'cough' in user_lower:
                    return "I understand you're having breathing issues. Can you describe what's happening - is it shortness of breath, a persistent cough, or something else?"
                else:
                    return f"I'm sorry to hear you're not feeling well. Can you tell me a bit more about what's bothering you? The more details you can share, the better I can help you find the right doctor."
            else:
                # If we've already been talking, provide recommendations
                return self._analyze_symptoms_and_recommend_fallback(user_input, conversation_history)
        
        # Default response
        return "I'm here to help you find the right doctor for your health needs. What's on your mind today?"

    def process_query(self, user_input: str, session_id: str = "default") -> str:
        """Process user query with natural conversation flow"""
        
        # Initialize conversation if new
        if session_id not in self.conversations:
            self.conversations[session_id] = {'messages': []}
        
        conversation = self.conversations[session_id]
        user_input_clean = user_input.strip()
        
        # Build conversation context for API
        system_prompt = self._create_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent conversation history (last 6 messages to keep context but stay within limits)
        recent_history = conversation['messages'][-6:] if len(conversation['messages']) > 6 else conversation['messages']
        for msg in recent_history:
            messages.append({"role": "user", "content": msg['user']})
            messages.append({"role": "assistant", "content": msg['assistant']})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input_clean})
        
        # Try to get AI response
        ai_response = self._call_deepseek_api(messages)
        
        if ai_response:
            # Store conversation
            conversation['messages'].append({'user': user_input, 'assistant': ai_response})
            
            # Clean up conversation history if it gets too long
            if len(conversation['messages']) > 12:
                conversation['messages'] = conversation['messages'][-10:]
            
            return ai_response
        
        else:
            # Smart fallback when AI fails
            fallback_response = self._get_smart_fallback(user_input_clean, conversation['messages'])
            conversation['messages'].append({'user': user_input, 'assistant': fallback_response})
            return fallback_response

# Initialize chatbot
chatbot = HealthAssistantChatbot()

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
                'response': 'Hi there! I\'m here to help you with any health concerns or doctor recommendations. What\'s on your mind?',
                'session_id': session_id,
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        print(f"Natural chat processing: '{user_message}' for session: {session_id}")
        
        response_text = chatbot.process_query(user_message, session_id)
        
        return jsonify({
            'response': response_text,
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'Hi! I\'m here to help you find the right doctor for any health concerns. How can I assist you today?',
            'session_id': 'error_session',
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'Natural Health Assistant AI - DeepSeek R1 0528',
        'timestamp': datetime.datetime.now().isoformat(),
        'doctors_loaded': len(chatbot.doctors),
        'model': chatbot.model
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Natural Health Assistant Chatbot API - DeepSeek R1 0528',
        'status': 'online',
        'model': 'deepseek/deepseek-r1:free',
        'features': [
            'Natural conversation flow',
            'Contextual doctor recommendations', 
            'Empathetic responses',
            'Flexible interaction patterns',
            'Smart fallback system'
        ],
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/health (GET)'
        },
        'usage': 'Send POST request to /api/chat with {"message": "your message", "session_id": "optional_session_id"}',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🤖 Starting Natural Health Assistant Chatbot on port {port}")
    print(f"👨‍⚕️ Loaded {len(chatbot.doctors)} doctors")
    print(f"🧠 Using model: {chatbot.model}")
    print("🗣️  Ready for natural conversations!")
    app.run(host='0.0.0.0', port=port, debug=False)
