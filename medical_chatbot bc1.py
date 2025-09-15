# Medical Knowledge Base based on WHO guidelines and medical best practices
# This dataset contains information about common symptoms, conditions, and WHO-verified treatments

# WHO Essential Medicines List - Verified medications
WHO_VERIFIED_MEDICINES = {
    "pain_relief": {
        "acetaminophen": {
            "brand_names": ["Tylenol", "Paracetamol"],
            "dosage": "500-1000mg every 4-6 hours (max 4000mg/day)",
            "uses": ["Fever", "Mild to moderate pain", "Headaches"],
            "who_approved": True,
            "side_effects": ["Liver damage with overdose", "Rare allergic reactions"],
            "contraindications": ["Severe liver disease", "Alcoholism"]
        },
        "ibuprofen": {
            "brand_names": ["Advil", "Motrin", "Brufen"],
            "dosage": "200-400mg every 4-6 hours (max 2400mg/day)",
            "uses": ["Pain", "Fever", "Inflammation"],
            "who_approved": True,
            "side_effects": ["Stomach upset", "Increased bleeding risk"],
            "contraindications": ["Stomach ulcers", "Kidney disease", "Heart disease"]
        },
        "aspirin": {
            "brand_names": ["Bayer", "Ecotrin"],
            "dosage": "325-650mg every 4 hours (max 4000mg/day)",
            "uses": ["Pain", "Fever", "Anti-inflammatory", "Blood thinner"],
            "who_approved": True,
            "side_effects": ["Stomach irritation", "Bleeding risk"],
            "contraindications": ["Children under 18", "Bleeding disorders", "Stomach ulcers"]
        }
    },
    "cold_flu": {
        "oseltamivir": {
            "brand_names": ["Tamiflu"],
            "dosage": "75mg twice daily for 5 days",
            "uses": ["Influenza treatment and prevention"],
            "who_approved": True,
            "side_effects": ["Nausea", "Vomiting", "Headache"],
            "contraindications": ["Severe kidney disease"]
        },
        "pseudoephedrine": {
            "brand_names": ["Sudafed", "Claritin-D"],
            "dosage": "30-60mg every 4-6 hours",
            "uses": ["Nasal congestion", "Sinus pressure"],
            "who_approved": True,
            "side_effects": ["Insomnia", "Nervousness", "Increased heart rate"],
            "contraindications": ["High blood pressure", "Heart disease", "Glaucoma"]
        },
        "dextromethorphan": {
            "brand_names": ["Robitussin", "Delsym"],
            "dosage": "15-30mg every 4-6 hours",
            "uses": ["Dry cough suppression"],
            "who_approved": True,
            "side_effects": ["Drowsiness", "Dizziness", "Nausea"],
            "contraindications": ["MAOI medications", "Severe liver disease"]
        }
    },
    "antihistamines": {
        "loratadine": {
            "brand_names": ["Claritin"],
            "dosage": "10mg once daily",
            "uses": ["Allergies", "Hay fever", "Hives"],
            "who_approved": True,
            "side_effects": ["Drowsiness", "Dry mouth", "Headache"],
            "contraindications": ["Severe liver disease"]
        },
        "cetirizine": {
            "brand_names": ["Zyrtec"],
            "dosage": "5-10mg once daily",
            "uses": ["Allergies", "Hay fever", "Chronic urticaria"],
            "who_approved": True,
            "side_effects": ["Drowsiness", "Dry mouth", "Fatigue"],
            "contraindications": ["Severe kidney disease"]
        }
    },
    "antacids": {
        "omeprazole": {
            "brand_names": ["Prilosec"],
            "dosage": "20-40mg once daily",
            "uses": ["GERD", "Stomach ulcers", "Acid reflux"],
            "who_approved": True,
            "side_effects": ["Headache", "Nausea", "Diarrhea"],
            "contraindications": ["Severe liver disease"]
        },
        "ranitidine": {
            "brand_names": ["Zantac"],
            "dosage": "150mg twice daily",
            "uses": ["Stomach ulcers", "GERD", "Acid indigestion"],
            "who_approved": True,
            "side_effects": ["Headache", "Dizziness", "Constipation"],
            "contraindications": ["Severe kidney disease"]
        }
    },
    "diabetes": {
        "metformin": {
            "brand_names": ["Glucophage"],
            "dosage": "500-2000mg daily in divided doses",
            "uses": ["Type 2 diabetes management"],
            "who_approved": True,
            "side_effects": ["Nausea", "Diarrhea", "Metallic taste"],
            "contraindications": ["Severe kidney disease", "Liver disease"]
        },
        "insulin_regular": {
            "brand_names": ["Humulin R", "Novolin R"],
            "dosage": "As prescribed by doctor",
            "uses": ["Type 1 and Type 2 diabetes"],
            "who_approved": True,
            "side_effects": ["Hypoglycemia", "Weight gain", "Injection site reactions"],
            "contraindications": ["Hypoglycemia", "Allergy to insulin"]
        }
    },
    "hypertension": {
        "lisinopril": {
            "brand_names": ["Prinivil", "Zestril"],
            "dosage": "10-40mg once daily",
            "uses": ["High blood pressure", "Heart failure"],
            "who_approved": True,
            "side_effects": ["Dry cough", "Dizziness", "Fatigue"],
            "contraindications": ["Pregnancy", "Bilateral renal artery stenosis"]
        },
        "amlodipine": {
            "brand_names": ["Norvasc"],
            "dosage": "5-10mg once daily",
            "uses": ["High blood pressure", "Chest pain (angina)"],
            "who_approved": True,
            "side_effects": ["Swelling of ankles", "Dizziness", "Flushing"],
            "contraindications": ["Severe aortic stenosis"]
        }
    }
}

MEDICAL_KNOWLEDGE = {
    "flu_symptoms": {
        "condition": "Influenza (Flu)",
        "symptoms": [
            "Fever (usually high, 100-102°F or higher)",
            "Chills and sweats",
            "Headache",
            "Muscle aches and body aches",
            "Fatigue and weakness",
            "Nasal congestion",
            "Sore throat",
            "Cough (usually dry)",
            "Loss of appetite",
            "Nausea and vomiting (more common in children)"
        ],
        "treatments": [
            "Rest and plenty of fluids",
            "WHO-verified pain relievers: Acetaminophen (Tylenol) 500-1000mg every 4-6 hours",
            "WHO-verified anti-inflammatory: Ibuprofen (Advil) 200-400mg every 4-6 hours",
            "WHO-verified antiviral: Oseltamivir (Tamiflu) 75mg twice daily for 5 days (prescription required)",
            "Stay home to avoid spreading the virus",
            "Use humidifier to ease breathing"
        ],
        "prevention": [
            "Annual flu vaccination",
            "Frequent hand washing",
            "Avoid close contact with sick people",
            "Cover mouth and nose when coughing or sneezing"
        ],
        "when_to_see_doctor": "Seek medical attention if you have difficulty breathing, persistent chest pain, severe dehydration, or if symptoms worsen after 3-4 days"
    },
    
    "cold_symptoms": {
        "condition": "Common Cold",
        "symptoms": [
            "Runny or stuffy nose",
            "Sneezing",
            "Sore throat",
            "Cough",
            "Mild headache",
            "Mild body aches",
            "Low-grade fever (rare in adults, more common in children)",
            "Watery eyes",
            "Mild fatigue"
        ],
        "treatments": [
            "Rest and stay hydrated",
            "Saline nasal sprays or drops",
            "WHO-verified decongestant: Pseudoephedrine (Sudafed) 30-60mg every 4-6 hours",
            "WHO-verified cough suppressant: Dextromethorphan (Robitussin) 15-30mg every 4-6 hours",
            "Throat lozenges for sore throat",
            "Warm salt water gargle",
            "Honey for cough (adults only)",
            "Steam inhalation"
        ],
        "prevention": [
            "Frequent hand washing",
            "Avoid touching face with unwashed hands",
            "Stay away from people with colds",
            "Don't share personal items"
        ],
        "when_to_see_doctor": "See a doctor if symptoms last more than 10 days, you have a high fever, or develop severe symptoms"
    },
    
    "fever": {
        "condition": "Fever",
        "symptoms": [
            "Body temperature above 100.4°F (38°C)",
            "Chills and shivering",
            "Sweating",
            "Headache",
            "Muscle aches",
            "Loss of appetite",
            "Dehydration",
            "General weakness"
        ],
        "treatments": [
            "Rest and plenty of fluids",
            "WHO-verified fever reducer: Acetaminophen (Tylenol) 500-1000mg every 4-6 hours",
            "WHO-verified anti-inflammatory: Ibuprofen (Advil) 200-400mg every 4-6 hours",
            "Cool compresses on forehead",
            "Light clothing and cool room temperature",
            "Warm baths (not cold)",
            "Stay hydrated with water, clear broths, or electrolyte solutions"
        ],
        "prevention": [
            "Good hygiene practices",
            "Stay up to date with vaccinations",
            "Avoid close contact with sick people"
        ],
        "when_to_see_doctor": "Seek immediate medical attention if fever is above 103°F (39.4°C), lasts more than 3 days, or is accompanied by severe symptoms like difficulty breathing, confusion, or severe headache"
    },
    
    "headache": {
        "condition": "Headache",
        "symptoms": [
            "Pain in head or neck area",
            "Throbbing or constant pain",
            "Sensitivity to light or sound",
            "Nausea or vomiting (in severe cases)",
            "Tension in neck and shoulder muscles"
        ],
        "treatments": [
            "Rest in a quiet, dark room",
            "WHO-verified pain reliever: Acetaminophen (Tylenol) 500-1000mg every 4-6 hours",
            "WHO-verified anti-inflammatory: Ibuprofen (Advil) 200-400mg every 4-6 hours",
            "WHO-verified pain reliever: Aspirin (Bayer) 325-650mg every 4 hours (adults only)",
            "Cold or warm compress on head or neck",
            "Gentle massage of temples and neck",
            "Stay hydrated",
            "Regular sleep schedule"
        ],
        "prevention": [
            "Manage stress through relaxation techniques",
            "Maintain regular sleep patterns",
            "Stay hydrated",
            "Limit caffeine and alcohol",
            "Regular exercise"
        ],
        "when_to_see_doctor": "Seek immediate medical attention for sudden, severe headache; headache with fever, stiff neck, or confusion; or if headache follows head injury"
    },
    
    "cough": {
        "condition": "Cough",
        "symptoms": [
            "Dry cough (no mucus)",
            "Wet cough (with mucus/phlegm)",
            "Persistent coughing",
            "Chest discomfort",
            "Sore throat from coughing",
            "Difficulty sleeping due to coughing"
        ],
        "treatments": [
            "Stay hydrated with warm liquids",
            "Honey (adults only) - 1-2 teaspoons",
            "Over-the-counter cough suppressants for dry cough",
            "Expectorants for wet cough",
            "Throat lozenges",
            "Steam inhalation",
            "Elevate head while sleeping"
        ],
        "prevention": [
            "Avoid irritants like smoke and dust",
            "Use humidifier in dry environments",
            "Practice good hand hygiene",
            "Stay away from people with respiratory infections"
        ],
        "when_to_see_doctor": "See a doctor if cough lasts more than 3 weeks, produces blood, is accompanied by fever, or causes difficulty breathing"
    },
    
    "sore_throat": {
        "condition": "Sore Throat",
        "symptoms": [
            "Pain or scratchiness in throat",
            "Difficulty swallowing",
            "Swollen glands in neck",
            "Hoarse voice",
            "Red and swollen tonsils",
            "White patches on tonsils (in some cases)"
        ],
        "treatments": [
            "Warm salt water gargle (1/4 to 1/2 teaspoon salt in 8 ounces warm water)",
            "Throat lozenges or hard candy",
            "Warm liquids (tea with honey, broth)",
            "Over-the-counter pain relievers",
            "Rest your voice",
            "Use humidifier"
        ],
        "prevention": [
            "Frequent hand washing",
            "Avoid sharing drinks or utensils",
            "Stay away from people with sore throats",
            "Don't smoke and avoid secondhand smoke"
        ],
        "when_to_see_doctor": "See a doctor if sore throat is severe, lasts more than a week, is accompanied by fever, or if you have difficulty breathing or swallowing"
    },
    
    "diabetes": {
        "condition": "Diabetes",
        "symptoms": [
            "Increased thirst and urination",
            "Extreme fatigue",
            "Blurred vision",
            "Slow-healing sores or cuts",
            "Unexplained weight loss (Type 1)",
            "Frequent infections",
            "Tingling or numbness in hands/feet"
        ],
        "treatments": [
            "Blood glucose monitoring",
            "Insulin therapy (Type 1 and some Type 2)",
            "Oral medications (Type 2)",
            "Healthy diet with controlled carbohydrates",
            "Regular physical activity",
            "Weight management",
            "Regular medical check-ups"
        ],
        "prevention": [
            "Maintain healthy weight",
            "Regular physical activity",
            "Healthy diet low in sugar and processed foods",
            "Regular blood sugar monitoring if at risk",
            "Avoid smoking and excessive alcohol"
        ],
        "when_to_see_doctor": "Seek immediate medical attention for symptoms of diabetic ketoacidosis (nausea, vomiting, abdominal pain, fruity breath odor) or if blood sugar is extremely high or low"
    },
    
    "hypertension": {
        "condition": "High Blood Pressure (Hypertension)",
        "symptoms": [
            "Often no symptoms (silent condition)",
            "Headaches (in severe cases)",
            "Shortness of breath",
            "Nosebleeds (rare)",
            "Dizziness or lightheadedness",
            "Chest pain (in severe cases)"
        ],
        "treatments": [
            "Lifestyle modifications: DASH diet, regular exercise, weight management",
            "Medications as prescribed by doctor (ACE inhibitors, diuretics, etc.)",
            "Limit sodium intake",
            "Reduce alcohol consumption",
            "Quit smoking",
            "Stress management techniques"
        ],
        "prevention": [
            "Maintain healthy weight",
            "Regular physical activity (150 minutes/week moderate intensity)",
            "Healthy diet rich in fruits, vegetables, whole grains",
            "Limit sodium to less than 2,300mg/day",
            "Limit alcohol consumption",
            "Don't smoke",
            "Manage stress"
        ],
        "when_to_see_doctor": "Regular monitoring is essential. Seek immediate medical attention for severe headache, chest pain, difficulty breathing, or blood pressure readings above 180/120"
    }
}

def get_medicine_info(medicine_name):
    """
    Get detailed information about a specific WHO-verified medicine
    """
    medicine_lower = medicine_name.lower()
    
    # Search through all medicine categories
    for category, medicines in WHO_VERIFIED_MEDICINES.items():
        for med_name, med_info in medicines.items():
            if medicine_lower in med_name.lower() or any(brand.lower() in medicine_lower for brand in med_info['brand_names']):
                return med_info
    
    return None

def get_medical_info(query):
    """
    Search for medical information based on user query
    """
    query_lower = query.lower()
    
    # Check for specific medicine names first (more specific matching)
    medicine_info = get_medicine_info(query)
    if medicine_info:
        return {"type": "medicine", "data": medicine_info}
    
    # Check for medicine category requests
    if any(word in query_lower for word in ['pain relief', 'pain reliever', 'pain medicine', 'pain medication']):
        return {"type": "medicine_category", "data": "pain_relief"}
    elif any(word in query_lower for word in ['cold medicine', 'flu medicine', 'cold medication', 'flu medication']):
        return {"type": "medicine_category", "data": "cold_flu"}
    elif any(word in query_lower for word in ['allergy medicine', 'antihistamine']):
        return {"type": "medicine_category", "data": "antihistamines"}
    elif any(word in query_lower for word in ['diabetes medicine', 'diabetes medication']):
        return {"type": "medicine_category", "data": "diabetes"}
    elif any(word in query_lower for word in ['blood pressure medicine', 'hypertension medicine']):
        return {"type": "medicine_category", "data": "hypertension"}
    
    # Check for general medicine requests
    if any(word in query_lower for word in ['medicine', 'medication', 'drug', 'pill', 'tablet', 'capsule', 'give me']):
        return {"type": "medicine_list", "data": "all"}
    
    # Check for specific conditions
    if any(word in query_lower for word in ['flu', 'influenza']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['flu_symptoms']}
    elif any(word in query_lower for word in ['cold', 'common cold']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['cold_symptoms']}
    elif any(word in query_lower for word in ['fever', 'temperature', 'fiver']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['fever']}
    elif any(word in query_lower for word in ['headache', 'head pain']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['headache']}
    elif any(word in query_lower for word in ['cough', 'coughing']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['cough']}
    elif any(word in query_lower for word in ['sore throat', 'throat pain']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['sore_throat']}
    elif any(word in query_lower for word in ['diabetes', 'diabetic']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['diabetes']}
    elif any(word in query_lower for word in ['blood pressure', 'hypertension', 'high blood pressure']):
        return {"type": "condition", "data": MEDICAL_KNOWLEDGE['hypertension']}
    
    return None

def format_medical_response(medical_info):
    """
    Format medical information into a readable response
    """
    if not medical_info:
        return "I don't have specific information about that condition or medicine. Please consult with a healthcare professional for accurate medical advice."
    
    if medical_info.get("type") == "medicine":
        med_data = medical_info["data"]
        response = f"**WHO-Verified Medicine: {med_data.get('generic_name', 'Unknown')}**\n\n"
        
        response += "**Brand Names:**\n"
        for brand in med_data['brand_names']:
            response += f"• {brand}\n"
        
        response += f"\n**Dosage:**\n{med_data['dosage']}\n"
        
        response += "\n**Uses:**\n"
        for use in med_data['uses']:
            response += f"• {use}\n"
        
        response += "\n**Side Effects:**\n"
        for side_effect in med_data['side_effects']:
            response += f"• {side_effect}\n"
        
        response += "\n**Contraindications (Do not use if):**\n"
        for contraindication in med_data['contraindications']:
            response += f"• {contraindication}\n"
        
        response += f"\n✅ **WHO Approved:** {med_data['who_approved']}\n"
        
    elif medical_info.get("type") == "medicine_category":
        category = medical_info["data"]
        medicines = WHO_VERIFIED_MEDICINES.get(category, {})
        
        response = f"**WHO-Verified {category.replace('_', ' ').title()} Medicines:**\n\n"
        
        for med_name, med_data in medicines.items():
            response += f"**{med_name.title()}**\n"
            response += f"• Brand Names: {', '.join(med_data['brand_names'])}\n"
            response += f"• Dosage: {med_data['dosage']}\n"
            response += f"• Uses: {', '.join(med_data['uses'])}\n"
            response += f"• Side Effects: {', '.join(med_data['side_effects'])}\n\n"
        
        response += "Ask me about any specific medicine for detailed information!\n"
        
    elif medical_info.get("type") == "medicine_list":
        response = "**Available WHO-Verified Medicines by Category:**\n\n"
        
        for category, medicines in WHO_VERIFIED_MEDICINES.items():
            response += f"**{category.replace('_', ' ').title()}:**\n"
            for med_name, med_data in medicines.items():
                response += f"• {med_name.title()} ({', '.join(med_data['brand_names'])})\n"
            response += "\n"
        
        response += "Ask me about any specific medicine for detailed information!\n"
        
    else:  # condition
        condition_data = medical_info["data"]
        response = f"**{condition_data['condition']}**\n\n"
        
        response += "**Common Symptoms:**\n"
        for symptom in condition_data['symptoms']:
            response += f"• {symptom}\n"
        
        response += "\n**Treatment Options:**\n"
        for treatment in condition_data['treatments']:
            response += f"• {treatment}\n"
        
        response += "\n**Prevention Tips:**\n"
        for prevention in condition_data['prevention']:
            response += f"• {prevention}\n"
        
        response += f"\n**When to See a Doctor:**\n{condition_data['when_to_see_doctor']}\n"
    
    response += "\n⚠️ **Important Disclaimer:** This information is for educational purposes only and should not replace professional medical advice. Always consult with a qualified healthcare provider for proper diagnosis and treatment."
    
    return response
        