import requests
import datetime
import json

# Your specific API Keys for EmailJS
SERVICE_ID = "service_e6qslfs"
TEMPLATE_ID = "template_mlfzooz"

# SECURITY: Paste your 'Public Key' from your Account settings below
USER_PUBLIC_KEY = "7kp1xc0x3pv9cxGMw" 
# SECURITY: Paste your 'Private Key' from your Account settings below (Required for Python backend)
PRIVATE_KEY = "cfb7sWi8SbZZYxH15cAL2"

# 1. Monitor User Input
CRISIS_KEYWORDS = ['suicide', 'self-harm', 'harm']

def scan_user_input(message):
    '''Scan every message for crisis keywords.'''
    lower_message = message.lower()
    for word in CRISIS_KEYWORDS:
        if word in lower_message:
            return True, word
    return False, None

def trigger_email_alert(detected_keyword):
    '''Format payload and trigger the EmailJS API.'''
    
    # 2. Format the Payload
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "service_id": SERVICE_ID,
        "template_id": TEMPLATE_ID,
        "user_id": USER_PUBLIC_KEY, 
        "accessToken": PRIVATE_KEY, 
        "template_params": {
            "user_name": "Mappillai",
            "risk_factor": detected_keyword,
            "time": current_time
        }
    }

    headers = {'Content-Type': 'application/json'}

    print(f"[ALERT] Crisis keyword detected: '{detected_keyword}'")
    print(f"[SYSTEM] Triggering automated email to guardian...")

    # 3. Trigger the API
    url = "https://api.emailjs.com/api/v1.0/email/send"
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("[SUCCESS] Email Successfully Sent to Guardian!")
        else:
            print(f"[ERROR] Failed to send email. Code: {response.status_code}. Msg: {response.text}")
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to connect to EmailJS API. Details: {str(e)}")


if __name__ == "__main__":
    print("--- Serene AI: Chat Monitoring System Active ---\n")
    
    # Simulating a user message
    user_message = "I am experiencing feelings of self-harm today."
    print(f"User (Mappillai) typed: \"{user_message}\"\n")
    
    is_crisis, keyword = scan_user_input(user_message)
    
    if is_crisis:
        trigger_email_alert(keyword)
    else:
        print("[SYSTEM] No crisis detected. Sending to Serene AI for normal response.")
