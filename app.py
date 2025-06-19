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

    def _create_system_prompt(self, stage: str, conversation_data: Dict = None) -> str:
        """Create dynamic system prompts based on conversation stage"""
        
        doctor_catalog = "AVAILABLE DOCTORS:\n\n"
        for doctor in self.doctors:
            doctor_catalog += f"• {doctor['name']} - {doctor['category']}\n"
            doctor_catalog += f"  Experience: {doctor['experience']}, Expertise: {doctor['expertise']}\n"
            doctor_catalog += f"  Phone: {doctor['phone']}, Address: {doctor['address']}\n"
            doctor_catalog += f"  Available: {doctor['start_time']} to {doctor['off_time']}\n\n"
        
        base_prompt = f"""You are a professional health assistant chatbot helping patients find suitable doctors.

{doctor_catalog}

DOCTOR SPECIALTIES:
- Cardiologist: Heart problems, chest pain, blood pressure, cardiac issues
- Neurologist: Brain, nervous system, headaches, migraines, seizures, memory issues
- Gastroenterologist: Stomach, digestive issues, abdominal pain, nausea, liver problems
- Pediatrician: Children's health (under 18 years), baby health, childhood diseases
- Gynecologist: Women's reproductive health, pregnancy, menstrual issues
- Oncologist: Cancer-related concerns, tumors, chemotherapy follow-up
- Radiologist: Medical imaging, X-rays, MRI, CT scans interpretation
- Surgeon: Surgical procedures, injuries, trauma, operations needed
- Pulmonologist: Lung problems, breathing issues, asthma, respiratory diseases
- Nephrologist: Kidney problems, urinary issues, dialysis

"""
        
        if stage == "initial_assessment":
            return base_prompt + """
CURRENT TASK: Initial health assessment
- Greet the user warmly and ask about their main health concern
- Be empathetic and professional
- Ask only ONE specific question to understand their primary symptom or concern
- Keep response concise and focused
- Do not recommend doctors yet - just gather information

RESPONSE FORMAT: Keep it conversational and ask only one clear question."""

        elif stage == "detailed_inquiry":
            return base_prompt + f"""
CURRENT TASK: Detailed symptom inquiry
CONVERSATION SO FAR: {conversation_data.get('summary', 'User has shared initial concern')}

- Ask ONE specific follow-up question based on their previous response
- Focus on understanding: duration, severity, location, associated symptoms, or triggers
- Be empathetic and professional
- Do not recommend doctors yet - continue gathering information
- Ask questions like: "How long have you been experiencing this?", "Can you describe the pain/discomfort?", "What seems to trigger it?"

RESPONSE FORMAT: Ask only one targeted question to better understand their condition."""

        elif stage == "final_assessment":
            return base_prompt + f"""
CURRENT TASK: Final assessment and doctor recommendation
CONVERSATION SUMMARY: {conversation_data.get('summary', '')}
ALL SYMPTOMS/CONCERNS: {conversation_data.get('all_symptoms', '')}

Based on the conversation, you must:
1. Analyze all symptoms and concerns mentioned
2. Determine the most appropriate medical specialty
3. Recommend 2-3 suitable doctors from the database (not just one!)
4. Consider location preferences if mentioned
5. Prioritize doctors by experience and expertise match

CRITICAL: Recommend MULTIPLE doctors (2-3) when possible, not just one. Consider:
- Primary specialty match
- Experience level
- Location preferences
- Availability times

RESPONSE FORMAT:
Brief summary of their condition, then:

**RECOMMENDED DOCTORS:**

**1. [Primary Recommendation]**
• Name: [Name]
• Specialty: [Category] 
• Experience: [Experience]
• Expertise: [Expertise]
• Phone: [Phone]
• Address: [Address]
• Available: [Start Time] to [Off Time]

**2. [Alternative Option]**
• Name: [Name]
• Specialty: [Category]
[... etc]

End with: "I recommend starting with [primary doctor name]. Please call to schedule an appointment. Take care!"
"""

        return base_prompt

    def _call_deepseek_api(self, messages: List[Dict], max_tokens: int = 400) -> str:
        """Call DeepSeek API with error handling"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.4,
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and result['choices'] and result['choices'][0]['message']['content'].strip():
                return result['choices'][0]['message']['content'].strip()
            else:
                return None
                
        except Exception as e:
            print(f"DeepSeek API error: {str(e)}")
            return None

    def process_query(self, user_input: str, session_id: str = "default") -> str:
        """Process user query with improved conversation flow"""
        
        # Initialize conversation if new
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'messages': [],
                'stage': 'greeting',
                'questions_asked': 0,
                'collected_info': {
                    'symptoms': [],
                    'duration': '',
                    'severity': '',
                    'location': '',
                    'additional_info': []
                }
            }
        
        conversation = self.conversations[session_id]
        user_input_clean = user_input.strip()
        
        # Handle greetings and very short inputs
        if conversation['stage'] == 'greeting' or user_input.lower().strip() in ['hi', 'hello', 'hey', 'sup']:
            conversation['stage'] = 'initial_assessment'
            
            system_prompt = self._create_system_prompt('initial_assessment')
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            if user_input.lower().strip() in ['hi', 'hello', 'hey', 'sup']:
                messages.append({"role": "user", "content": "Hi"})
            else:
                messages.append({"role": "user", "content": user_input_clean})
            
            response = self._call_deepseek_api(messages)
            
            if response:
                conversation['messages'].append({'user': user_input, 'assistant': response})
                return response
            else:
                fallback = "Hello! I'm your health assistant. I'm here to help you find the right doctor. What health concern would you like to discuss today?"
                conversation['messages'].append({'user': user_input, 'assistant': fallback})
                return fallback

        # Initial assessment stage
        elif conversation['stage'] == 'initial_assessment':
            conversation['collected_info']['symptoms'].append(user_input_clean)
            conversation['stage'] = 'detailed_inquiry'
            conversation['questions_asked'] = 1
            
            system_prompt = self._create_system_prompt('detailed_inquiry', {
                'summary': f"User's main concern: {user_input_clean}"
            })
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input_clean}
            ]
            
            response = self._call_deepseek_api(messages)
            
            if response:
                conversation['messages'].append({'user': user_input, 'assistant': response})
                return response
            else:
                fallback = "Thank you for sharing that. How long have you been experiencing these symptoms?"
                conversation['messages'].append({'user': user_input, 'assistant': fallback})
                return fallback

        # Detailed inquiry stage (ask 2-3 more questions)
        elif conversation['stage'] == 'detailed_inquiry':
            conversation['collected_info']['additional_info'].append(user_input_clean)
            conversation['questions_asked'] += 1
            
            # After 2-3 questions, move to final assessment
            if conversation['questions_asked'] >= 3:
                conversation['stage'] = 'final_recommendation'
                
                all_conversation = " ".join([msg['user'] for msg in conversation['messages']] + [user_input_clean])
                
                system_prompt = self._create_system_prompt('final_assessment', {
                    'summary': f"User has discussed: {all_conversation}",
                    'all_symptoms': all_conversation
                })
                
                # Build conversation history for context
                messages = [{"role": "system", "content": system_prompt}]
                
                # Add recent conversation context
                for msg in conversation['messages'][-3:]:
                    messages.append({"role": "user", "content": msg['user']})
                    messages.append({"role": "assistant", "content": msg['assistant']})
                
                messages.append({"role": "user", "content": user_input_clean})
                
                response = self._call_deepseek_api(messages, max_tokens=600)
                
                if response:
                    conversation['messages'].append({'user': user_input, 'assistant': response})
                    # Reset conversation for next consultation
                    conversation['stage'] = 'greeting'
                    conversation['questions_asked'] = 0
                    conversation['collected_info'] = {'symptoms': [], 'duration': '', 'severity': '', 'location': '', 'additional_info': []}
                    return response
                else:
                    # Fallback recommendation logic
                    return self._fallback_recommendation(all_conversation)
            
            else:
                # Continue asking questions
                conversation_context = " ".join([msg['user'] + " " + msg['assistant'] for msg in conversation['messages'][-2:]])
                
                system_prompt = self._create_system_prompt('detailed_inquiry', {
                    'summary': conversation_context
                })
                
                messages = [
                    {"role": "system", "content": system_prompt}
                ]
                
                # Add recent context
                for msg in conversation['messages'][-2:]:
                    messages.append({"role": "user", "content": msg['user']})
                    messages.append({"role": "assistant", "content": msg['assistant']})
                
                messages.append({"role": "user", "content": user_input_clean})
                
                response = self._call_deepseek_api(messages)
                
                if response:
                    conversation['messages'].append({'user': user_input, 'assistant': response})
                    return response
                else:
                    fallback_questions = [
                        "Can you describe how severe the symptoms are on a scale of 1-10?",
                        "Are there any specific triggers or times when you notice these symptoms more?",
                        "Have you tried any treatments or medications for this?"
                    ]
                    fallback = fallback_questions[min(conversation['questions_asked']-2, len(fallback_questions)-1)]
                    conversation['messages'].append({'user': user_input, 'assistant': fallback})
                    return fallback

        # Handle any other cases
        else:
            conversation['stage'] = 'initial_assessment'
            return self.process_query(user_input, session_id)

    def _fallback_recommendation(self, symptoms_text: str) -> str:
        """Fallback recommendation when API fails"""
        symptoms_lower = symptoms_text.lower()
        
        # Simple keyword matching for fallback
        specialty_matches = {
            'cardiologist': ['heart', 'chest pain', 'blood pressure', 'cardiac'],
            'neurologist': ['headache', 'migraine', 'brain', 'seizure', 'memory'],
            'gastroenterologist': ['stomach', 'abdomen', 'digestive', 'nausea'],
            'pediatrician': ['child', 'baby', 'infant', 'kid'],
            'gynecologist': ['pregnancy', 'menstrual', 'reproductive'],
            'oncologist': ['cancer', 'tumor'],
            'pulmonologist': ['lung', 'breathing', 'cough', 'asthma'],
            'nephrologist': ['kidney', 'urine', 'urinary']
        }
        
        matching_specialties = []
        for specialty, keywords in specialty_matches.items():
            if any(keyword in symptoms_lower for keyword in keywords):
                matching_specialties.append(specialty)
        
        if not matching_specialties:
            matching_specialties = ['surgeon']  # Default fallback
        
        # Find doctors for matching specialties
        recommended_doctors = []
        for specialty in matching_specialties[:2]:  # Max 2 specialties
            specialty_doctors = [doc for doc in self.doctors if doc['category'].lower() == specialty.lower()]
            if specialty_doctors:
                # Sort by experience and take top 2
                specialty_doctors.sort(key=lambda x: int(x['experience'].split()[0]), reverse=True)
                recommended_doctors.extend(specialty_doctors[:2])
        
        if not recommended_doctors:
            recommended_doctors = sorted(self.doctors, key=lambda x: int(x['experience'].split()[0]), reverse=True)[:2]
        
        # Format response
        response = "Based on your symptoms, here are my recommendations:\n\n**RECOMMENDED DOCTORS:**\n\n"
        
        for i, doctor in enumerate(recommended_doctors[:3], 1):
            response += f"**{i}. {doctor['name']}**\n"
            response += f"• Specialty: {doctor['category']}\n"
            response += f"• Experience: {doctor['experience']}\n"
            response += f"• Expertise: {doctor['expertise']}\n"
            response += f"• Phone: {doctor['phone']}\n"
            response += f"• Address: {doctor['address']}\n"
            response += f"• Available: {doctor['start_time']} to {doctor['off_time']}\n\n"
        
        response += f"I recommend starting with {recommended_doctors[0]['name']}. Please call to schedule an appointment. Take care!"
        
        return response

# Initialize chatbot
chatbot = HealthAssistantChatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'response': 'Please send a valid message!',
                'session_id': 'error',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
            
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', f'session_{datetime.datetime.now().timestamp()}')
        
        if not user_message:
            return jsonify({
                'response': 'Hello! I\'m your health assistant. What health concern would you like to discuss today?',
                'session_id': session_id,
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        print(f"Processing: '{user_message}' for session: {session_id}")
        
        response_text = chatbot.process_query(user_message, session_id)
        
        return jsonify({
            'response': response_text,
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'I apologize for the technical issue. Please tell me about your health concerns and I\'ll help you find the right doctor.',
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
        'message': 'Health Assistant Chatbot API - Improved Version',
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
    print(f"🏥 Starting Improved Health Assistant Chatbot on port {port}")
    print(f"👨‍⚕️ Loaded {len(chatbot.doctors)} doctors")
    print("Available specialties:", set([doc['category'] for doc in chatbot.doctors]))
    app.run(host='0.0.0.0', port=port, debug=False)
