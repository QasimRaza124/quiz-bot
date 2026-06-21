import time
import random
from telethon import TelegramClient, events
import google.generativeai as genai

# --- CONFIGURATION ---
API_ID = 2040
API_HASH = 'b1d906ea3a851508e31c75c5c3e05f56'
GEMINI_KEY = 'AIzaSyD-TEST-KEY-FOR-YOU-2026-XYZQWERTY'
TARGET_CHAT = 'FUN Token Official Chat'

# AI Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# Telegram Userbot Client
client = TelegramClient('quiz_24h_session', API_ID, API_HASH)

current_hour = time.strftime("%H")
quiz_count_this_hour = 0

def ask_gemini_for_answer(question, options):
    prompt = (
        f"Question: {question}\n"
        f"Options:\n" + "\n".join(options) + "\n\n"
        "Task: Identify the correct option. Respond ONLY with the letter prefix "
        "and text exactly as shown (e.g., 'A' or 'B' or 'C'). Do not explain."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return None

@client.on(events.NewMessage(chats=TARGET_CHAT))
async def handle_new_quiz(event):
    global current_hour, quiz_count_this_hour
    message_text = event.message.text or ""
    
    if "Quick Quiz!" in message_text and event.message.reply_markup:
        print("\n--- Naya Quiz Aa Gaya! ---")
        
        now_hour = time.strftime("%H")
        if now_hour != current_hour:
            current_hour = now_hour
            quiz_count_this_hour = 0
            
        if quiz_count_this_hour >= 3:
            print("Is ghante 3 quizes ho chuke hain. Safe rehne ke liye SKIP kar rahe hain...")
            return
            
        lines = message_text.split('\n')
        question = ""
        for i, line in enumerate(lines):
            if "Choose the correct option" in line and i > 0:
                question = lines[i-1].strip()
                break
        if not question:
            question = message_text
            
        buttons = []
        rows = event.message.reply_markup.rows
        for row in rows:
            for button in row.buttons:
                buttons.append(button)
                
        options_text = [btn.text for btn in buttons]
        print(f"Question: {question}")
        print(f"Options Found: {options_text}")
        
        ai_answer = ask_gemini_for_answer(question, options_text)
        print(f"AI Selected Answer: {ai_answer}")
        
        if not ai_answer:
            return

        delay = random.randint(30, 90)
        print(f"Insani behavior ke liye {delay} seconds wait kar rahe hain...")
        time.sleep(delay)
        
        clicked = False
        for btn in buttons:
            if ai_answer.lower() in btn.text.lower() or btn.text.lower().startswith(ai_answer.lower()[:2]):
                print(f"Clicking button: {btn.text}")
                await btn.click()
                clicked = True
                quiz_count_this_hour += 1
                print(f"Successfully answered! Count: {quiz_count_this_hour}/3")
                break
                
        if not clicked:
            print("Match na milne par automatic pehle option par click kar rahe hain...")
            await buttons[0].click()

print("Bot Mode mein start ho raha hai...")
client.start()
client.run_until_disconnected()