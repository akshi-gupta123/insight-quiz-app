import streamlit as st
import pandas as pd
import time
from datetime import datetime
import random
import os
import json

# Page configuration
st.set_page_config(
    page_title="AI Knowledge Quiz",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    /* Main background and styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Question card styling */
    .question-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 0.8rem 0;
    }
    
    /* Question text styling - SET TO BLACK FOR BETTER VISIBILITY */
    .question-text {
        color: #000000 !important;
        font-size: 1.5rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 1rem;
    }
            
    /* New styles for important notes */
    .important-note {
        background: #fffaf0;
        border: 2px solid #d69e2e;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .goodies-notice {
        background: #f0fff4;
        border: 2px solid #38a169;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .logo-item {
        text-align: center;
        margin: 1rem;
        flex: 1;
        min-width: 200px;
    }
    
    .logo-image {
        max-width: 150px;
        max-height: 100px;
        margin-bottom: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .logo-input {
        width: 80% !important;
        margin: 0 auto;
    }
    
    /* Explanation card styling */
    .explanation-card {
        background: #f0fff4;
        border: 2px solid #9ae6b4;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .explanation-title {
        color: #22543d;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .explanation-text {
        color: #2d3748;
        font-size: 1.1rem;
        line-height: 1.5;
    }
    
    /* Timer styling */
    .timer {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #764ba2;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .timer.warning {
        color: #ff6b6b;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Progress bar styling */
    .progress-text {
        text-align: center;
        font-size: 1.2rem;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6E8CFB, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .stButton>button:disabled {
        background: #a0aec0;
        cursor: not-allowed;
        transform: none;
    }
    
    .stButton>button:disabled:hover {
        transform: none;
        box-shadow: none;
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Title styling */
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #000000 !important; /* Set to black for better visibility */
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Result card */
    .result-card {
        background: white;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .score-display {
        font-size: 4rem;
        font-weight: bold;
        color: #667eea;
        margin: 2rem 0;
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    
    /* Email requirement text */
    .email-requirement {
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    /* Option text styling */
    .option-text {
        color: #2d3748;
        font-size: 1.1rem;
    }
    
    /* Ensure all text in question cards is visible */
    .question-card h2,
    .question-card h3,
    .question-card p,
    .question-card strong {
        color: #000000 !important;
    }
    
    /* Result details text */
    .result-details {
        color: #000000 !important;
    }
    
    /* Auto-scroll functionality */
    .scroll-to-bottom {
        scroll-behavior: smooth;
    }
    
    /* Leaderboard specific styles */
    .leaderboard-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    
    .gold-rank {
        background: linear-gradient(135deg, #FFD700, #FFEC8B);
        border: 2px solid #FFD700;
    }
    
    .silver-rank {
        background: linear-gradient(135deg, #C0C0C0, #E8E8E8);
        border: 2px solid #C0C0C0;
    }
    
    .bronze-rank {
        background: linear-gradient(135deg, #CD7F32, #E8B886);
        border: 2px solid #CD7F32;
    }
    
    .normal-rank {
        background: white;
        border: 1px solid #667eea;
    }
    
    .rank-badge {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin-right: 0.8rem;
        min-width: 40px;
    }
    
    .stats-card {
        background: rgba(255,255,255,0.95);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem;
        text-align: center;
    }
    
    .participant-name {
        font-size: 1.1rem;
        margin: 0;
        color: #2d3748;
    }
    
    .participant-email {
        font-size: 0.8rem;
        margin: 0;
        color: #718096;
    }
    
    .participant-score {
        font-size: 1.1rem;
        margin: 0;
        color: #667eea;
    }
    
    .participant-details {
        font-size: 0.8rem;
        margin: 0;
        color: #718096;
    }
    
    </style>
    
    <script>
    function scrollToBottom() {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    }
    </script>
""", unsafe_allow_html=True)

# Load logos data
@st.cache_data
def load_logos_data():
    """Load logos data from GitHub URL using secrets configuration"""
    import json
    import requests
    
    try:
        # Get base URL from secrets and derive specific URLs
        try:
            base_url = st.secrets["base_url"]
            logos_data_url = base_url + "logos_data.json"
            logos_base_url = base_url + "logos/"
        except KeyError as secret_error:
            st.error(f"Secret configuration error: {secret_error}")
            st.error("Available secrets keys: " + str(list(st.secrets.keys()) if hasattr(st.secrets, 'keys') else "No secrets found"))
            return []
        
        # Load logos data from GitHub URL
        response = requests.get(logos_data_url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Debug information for deployment
        if response.status_code != 200:
            st.error(f"HTTP Error: {response.status_code} - {response.reason}")
            return []
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type and 'text/plain' not in content_type:
            st.error(f"Unexpected content type: {content_type}")
            st.error(f"Response preview: {response.text[:200]}")
            return []
        
        # Try to parse JSON
        try:
            logos_data = response.json()
        except json.JSONDecodeError as json_err:
            st.error(f"JSON parsing failed: {json_err}")
            st.error(f"Response content (first 500 chars): {response.text[:500]}")
            return []
        
        # Update image paths to use GitHub raw URLs
        for logo in logos_data:
            if 'image' in logo:
                # Extract filename from the original path
                filename = logo['image'].split('/')[-1]
                logo['image'] = logos_base_url + filename
        
        return logos_data
    
    except KeyError as e:
        st.error(f"Missing required secret configuration: {e}. Please check your secrets.toml file.")
        return []
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please check your internet connection and try again.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching logos data from GitHub: {e}")
        st.error(f"URL attempted: {logos_data_url}")
        return []
    except Exception as e:
        st.error(f"Unexpected error loading logos data: {e}")
        return []

# Get logos data
all_logos = load_logos_data()

def check_logo_answer(user_answer, correct_name, alt_names):
    """Check if user answer matches correct name or alternative names (case insensitive)"""
    user_answer_clean = user_answer.strip().lower()
    correct_names = [correct_name.lower()] + [alt.lower() for alt in alt_names]
    return user_answer_clean in correct_names

# Load quiz data
@st.cache_data
def load_quiz_data():
    import json
    import requests
    
    try:
        # Get base URL from secrets and derive specific URL
        try:
            base_url = st.secrets["base_url"]
            quiz_data_url = base_url + "quiz_data.json"
        except KeyError as secret_error:
            st.error(f"Secret configuration error: {secret_error}")
            st.error("Available secrets keys: " + str(list(st.secrets.keys()) if hasattr(st.secrets, 'keys') else "No secrets found"))
            return pd.DataFrame()
        
        # Load quiz data from GitHub URL
        response = requests.get(quiz_data_url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Debug information for deployment
        if response.status_code != 200:
            st.error(f"HTTP Error: {response.status_code} - {response.reason}")
            return pd.DataFrame()
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type and 'text/plain' not in content_type:
            st.error(f"Unexpected content type: {content_type}")
            st.error(f"Response preview: {response.text[:200]}")
            return pd.DataFrame()
        
        # Try to parse JSON
        try:
            data = response.json()
        except json.JSONDecodeError as json_err:
            st.error(f"JSON parsing failed: {json_err}")
            st.error(f"Response content (first 500 chars): {response.text[:500]}")
            return pd.DataFrame()
            
    except KeyError as e:
        st.error(f"Missing required secret configuration: {e}. Please check your secrets.toml file.")
        return pd.DataFrame()
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please check your internet connection and try again.")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching quiz data from GitHub: {e}")
        st.error(f"URL attempted: {quiz_data_url}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected error loading quiz data: {e}")
        return pd.DataFrame()
    # Verify all arrays have the same length
    expected_length = len(data['Question'])
    for key, value in data.items():
        if len(value) != expected_length:
            print(f"Warning: {key} has {len(value)} elements, expected {expected_length}")
    
    return pd.DataFrame(data)

# Initialize session state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.email = ""
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.start_time = None
    st.session_state.quiz_completed = False
    st.session_state.show_explanation = False
    st.session_state.explanation_start_time = None
    st.session_state.explanation_data = None
    st.session_state.question_submitted = False
    st.session_state.current_page = "quiz"  # Track current page

# Functions for email tracking
def get_attempted_emails():
    """Retrieve list of emails that have attempted the quiz"""
    try:
        # Using session state to store attempted emails (persists during session)
        if 'attempted_emails' not in st.session_state:
            st.session_state.attempted_emails = set()
        return st.session_state.attempted_emails
    except:
        return set()

def store_attempted_email(email):
    """Store an email that has attempted the quiz"""
    try:
        if 'attempted_emails' not in st.session_state:
            st.session_state.attempted_emails = set()
        st.session_state.attempted_emails.add(email)
    except:
        pass

# For persistent storage across sessions (using a file)
def get_persistent_attempted_emails():
    """Retrieve emails from persistent storage"""
    try:
        # Create a simple file-based storage
        try:
            with open('attempted_emails.txt', 'r') as f:
                emails = set(line.strip().lower() for line in f if line.strip())
                return emails
        except FileNotFoundError:
            return set()
    except:
        return set()

def store_persistent_attempted_email(email):
    """Store email in persistent storage"""
    try:
        # Read existing emails
        existing_emails = get_persistent_attempted_emails()
        # Add new email
        existing_emails.add(email.lower())
        # Write back to file
        with open('attempted_emails.txt', 'w') as f:
            for email in existing_emails:
                f.write(email + '\n')
    except:
        pass

# Updated email validation function that checks both session and persistent storage
def has_email_attempted(email):
    """Check if email has already attempted the quiz"""
    email = email.lower()
    # Check session state (current run)
    if email in get_attempted_emails():
        return True
    # Check persistent storage (across sessions)
    if email in get_persistent_attempted_emails():
        return True
    return False

def store_email_attempt(email):
    """Store email in both session and persistent storage"""
    email = email.lower()
    store_attempted_email(email)
    store_persistent_attempted_email(email)

def get_single_logo_question(exclude_logos=None):
    """Get a single random logo for questions 7 and 8"""
    if exclude_logos is None:
        exclude_logos = []
    
    available_logos = [logo for logo in all_logos if logo['name'] not in exclude_logos]
    
    if not available_logos:
        # If all logos are excluded, fall back to all logos
        available_logos = all_logos
    
    logo = random.choice(available_logos)
    return {
        'type': 'single_logo_quiz',
        'question': 'Identify the following logo:',
        'logo': logo,
        'correct_answer': logo['name']
    }

def select_random_questions(df, num_questions=6):
    """Select random questions from different categories"""
    categories = df['Category'].unique()
    selected_questions = []
    
    # Randomly select one question from each category until we have 6 questions
    random.shuffle(list(categories))
    
    for category in categories:
        if len(selected_questions) >= num_questions:
            break
        category_questions = df[df['Category'] == category].sample(n=1)
        selected_questions.append(category_questions.iloc[0])
    
    # If we still need more questions, randomly select from all
    while len(selected_questions) < num_questions:
        remaining = df.sample(n=1).iloc[0]
        if not any(q['Question'] == remaining['Question'] for q in selected_questions):
            selected_questions.append(remaining)
    
    random.shuffle(selected_questions)
    
    # Add two single logo quiz questions (7th and 8th questions) with different logos
    first_logo_question = get_single_logo_question()
    excluded_logos = [first_logo_question['logo']['name']]
    second_logo_question = get_single_logo_question(exclude_logos=excluded_logos)
    
    selected_questions.append(first_logo_question)  # 7th question
    selected_questions.append(second_logo_question)  # 8th question
    
    return selected_questions

def get_time_remaining():
    """Calculate remaining time for current question"""
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        # Questions 7 and 8 (index 6 and 7) get 25 seconds, others get 20
        if st.session_state.current_question in [6, 7]:  # 7th and 8th questions
            remaining = max(0, 25 - int(elapsed))
        else:
            remaining = max(0, 20 - int(elapsed))
        return remaining
    return 20

def get_explanation_time_remaining():
    """Calculate remaining time for explanation display"""
    if st.session_state.explanation_start_time:
        elapsed = time.time() - st.session_state.explanation_start_time
        remaining = max(0, 10 - int(elapsed))
        return remaining
    return 10

# Add this function to store quiz results
def store_quiz_result(email, score, total_questions, attempted_questions, correct_answers, answers_data, time_taken):
    """Store quiz results in a JSON file"""
    
    result_data = {
        "email": email,
        "score": score,
        "total_questions": total_questions,
        "attempted_questions": attempted_questions,
        "correct_answers": correct_answers,
        "percentage": int((correct_answers / attempted_questions * 100)) if attempted_questions > 0 else 0,
        "timestamp": datetime.now().isoformat(),
        "time_taken_seconds": time_taken,
        "answers": answers_data
    }
    
    try:
        # Try to read existing data
        try:
            with open('quiz_results.json', 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {"quiz_attempts": []}
        
        # Append new result
        existing_data["quiz_attempts"].append(result_data)
        
        # Write back to file
        with open('quiz_results.json', 'w') as f:
            json.dump(existing_data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error storing quiz result: {e}")
        return False

# Add this function to calculate time taken
def calculate_total_time():
    """Calculate total time taken for the quiz"""
    if st.session_state.start_time:
        return int(time.time() - st.session_state.start_time)
    return 0

# Leaderboard functions
def load_quiz_results():
    """Load quiz results from JSON file"""
    try:
        with open('quiz_results.json', 'r') as f:
            data = json.load(f)
        return data.get('quiz_attempts', [])
    except FileNotFoundError:
        st.error("No quiz results found. The quiz hasn't been taken yet.")
        return []
    except Exception as e:
        st.error(f"Error loading quiz results: {e}")
        return []

def create_leaderboard_data(results):
    """Create leaderboard data from results - show only best attempt per user"""
    leaderboard_data = []
    
    # Group attempts by email and keep only the best attempt for each user
    user_best_attempts = {}
    
    for result in results:
        email = result['email']
        percentage = result['percentage']
        
        # If this user doesn't exist yet, or this attempt is better, update their best attempt
        if email not in user_best_attempts:
            user_best_attempts[email] = result
        else:
            # Compare percentages, if equal compare by time (faster is better)
            if percentage > user_best_attempts[email]['percentage']:
                user_best_attempts[email] = result
            elif percentage == user_best_attempts[email]['percentage']:
                # If same percentage, take the faster attempt
                if result['time_taken_seconds'] < user_best_attempts[email]['time_taken_seconds']:
                    user_best_attempts[email] = result
    
    # Convert to list for leaderboard
    for result in user_best_attempts.values():
        # Extract username from email
        email = result['email']
        username = email.split('@')[0].replace('.', ' ').title()
        
        leaderboard_data.append({
            'username': username,
            'email': email,
            'score': result['correct_answers'],
            'total_questions': result['total_questions'],
            'percentage': result['percentage'],
            'attempted_questions': result['attempted_questions'],
            'time_taken': result['time_taken_seconds'],
            'timestamp': result['timestamp']
        })
    
    return pd.DataFrame(leaderboard_data)

def display_leaderboard():
    """Display the leaderboard"""
    st.markdown("<h1 style='color: white; text-align: center; margin-bottom: 1.5rem;'>🏆 AI Quiz Leaderboard</h1>", unsafe_allow_html=True)
    
    # Add navigation button to go back to quiz
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔙 Back to Quiz"):
            st.session_state.current_page = "quiz"
            st.query_params.clear()
            st.rerun()
    
    results = load_quiz_results()
    
    if not results:
        st.markdown("""
            <div style='text-align: center; color: white; padding: 3rem;'>
                <h3>No quiz results yet!</h3>
                <p>Take the AI Quiz to see your name on the leaderboard.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    df = create_leaderboard_data(results)
    
    # Overall statistics - simplified
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <h4 style='margin: 0; color: #4a5568;'>Total Participants</h4>
                <h3 style='margin: 0; color: #667eea;'>{len(df)}</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_score = df['percentage'].mean()
        st.markdown(f"""
            <div class="stats-card">
                <h4 style='margin: 0; color: #4a5568;'>Average Score</h4>
                <h3 style='margin: 0; color: #667eea;'>{avg_score:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        best_score = df['percentage'].max()
        st.markdown(f"""
            <div class="stats-card">
                <h4 style='margin: 0; color: #4a5568;'>Best Score</h4>
                <h3 style='margin: 0; color: #667eea;'>{best_score}%</h3>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sort by percentage (primary) and time taken (secondary)
    df_sorted = df.sort_values(['percentage', 'time_taken'], ascending=[False, True])
    
    # Display leaderboard
    for idx, (_, participant) in enumerate(df_sorted.iterrows(), 1):
        if idx == 1:
            card_class = "gold-rank"
            rank_emoji = "🥇"
        elif idx == 2:
            card_class = "silver-rank"
            rank_emoji = "🥈"
        elif idx == 3:
            card_class = "bronze-rank"
            rank_emoji = "🥉"
        else:
            card_class = "normal-rank"
            rank_emoji = f"#{idx}"
        
        # Create a single row for each participant
        st.markdown(f"""
            <div class='leaderboard-card {card_class}'>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center;">
                        <div class='rank-badge'>{rank_emoji}</div>
                        <div>
                            <p class='participant-name'>{participant['username']}</p>
                            <p class='participant-email'>{participant['email']}</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p class='participant-score'>{participant['percentage']}%</p>
                        <p class='participant-details'>
                            {participant['score']}/{participant['total_questions']} • {participant['time_taken']}s
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Main app navigation
def main():
    # Check URL parameters for navigation
    query_params = st.query_params
    if 'page' in query_params and query_params['page'] == 'leaderboard':
        st.session_state.current_page = "leaderboard"
    
    if st.session_state.current_page == "leaderboard":
        display_leaderboard()
        return
    
    # Original quiz app code
    st.markdown("<h1>Insight Engine Booth</h1>", unsafe_allow_html=True)

    # Email input screen
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div class="question-card">
                    <h2 style="text-align: center; color: #667eea;">Welcome to the AI Quiz! 🧠</h2>
                    <p style="text-align: center; font-size: 1.1rem; color: #4a5568; margin: 1rem 0;">
                        You'll have 20 to 25 seconds to answer each question.<br>
                        <strong style="color: #e53e3e;">🎁 Exciting goodies will be provided to Winners!</strong><br>
                        <strong style="color: #d69e2e;">⚠️ Rewards will be provided only to valid users, carefully fill your email.</strong><br>
                        <strong style="color: #d69e2e;">⚠️ </strong> Remember to click the <strong>Submit Answer</strong> button for each question!<br><br>
                        <strong>Ready to challenge yourself?</strong>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input("📧 Enter your email address:", placeholder="your.name@spglobal.com")
            
            if st.button("🚀 Start Quiz"):
                if email:
                    email = email.strip()
                    if '@spglobal.com' in email.lower():
                        # Check if email already attempted the quiz
                        if has_email_attempted(email):
                            st.error("🚫 This email has already attempted the quiz. Each user can only attempt once.")
                        else:
                            # Store the email in attempted emails
                            store_email_attempt(email)
                            st.session_state.email = email
                            df = load_quiz_data()
                            st.session_state.questions = select_random_questions(df, 6)
                            st.session_state.quiz_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                    else:
                        st.error("⚠️ Please use a valid @spglobal.com email address!")
                else:
                    st.error("⚠️ Please enter your email address!")

    # Quiz screen
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        current_q_idx = st.session_state.current_question
        
        if current_q_idx < len(st.session_state.questions):
            question_data = st.session_state.questions[current_q_idx]
            
            # Progress indicator
            progress = (current_q_idx) / len(st.session_state.questions)
            st.progress(progress)
            st.markdown(f"""
                <div class="progress-text">
                    Question {current_q_idx + 1} of {len(st.session_state.questions)}
                </div>
            """, unsafe_allow_html=True)
            
            # Timer (only show if question not submitted)
            if not st.session_state.question_submitted:
                time_remaining = get_time_remaining()
                timer_class = "timer warning" if time_remaining <= 5 else "timer"
                timer_placeholder = st.empty()
                timer_placeholder.markdown(f'<div class="{timer_class}">⏱️ {time_remaining}s</div>', unsafe_allow_html=True)
                
                # Auto-submit if time runs out
                if time_remaining == 0:
                    if question_data.get('type') == 'single_logo_quiz':
                        # For single logo quiz, store empty answer
                        st.session_state.answers.append({
                            'question': question_data['question'],
                            'type': 'single_logo_quiz',
                            'logo': question_data['logo'],
                            'user_answer': '',
                            'correct_answer': question_data['correct_answer'],
                            'is_correct': False,
                            'timed_out': True
                        })
                    else:
                        st.session_state.answers.append({
                            'question': question_data['Question'],
                            'selected': None,
                            'correct': question_data['Correct_Answer'],
                            'is_correct': False,
                            'explanation': question_data['Explanation'],
                            'timed_out': True
                        })
                    st.session_state.question_submitted = True
                    st.session_state.explanation_start_time = time.time()
                    st.rerun()
            
            # Question card
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                if question_data.get('type') == 'single_logo_quiz':
                    # Single logo quiz question (questions 7 and 8)
                    st.markdown(f"""
                        <div class="question-card">
                            <h2 style="color: #000000;">{question_data['question']}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the single logo in the center
                    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
                    with col_img2:
                        st.image(question_data['logo']['image'], width=200)
                        user_input = st.text_input("Enter the logo name:", key=f"logo_{current_q_idx}", disabled=st.session_state.question_submitted)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Submit button for single logo quiz
                    if not st.session_state.question_submitted:
                        if st.button("✅ Submit Answer", key=f"submit_{current_q_idx}"):
                            # Check the answer
                            is_correct = check_logo_answer(user_input, question_data['correct_answer'], question_data['logo'].get('alt', []))
                            
                            if is_correct:
                                st.session_state.score += 1
                            
                            st.session_state.answers.append({
                                'question': question_data['question'],
                                'type': 'single_logo_quiz',
                                'logo': question_data['logo'],
                                'user_answer': user_input,
                                'correct_answer': question_data['correct_answer'],
                                'is_correct': is_correct,
                                'timed_out': False
                            })
                            
                            st.session_state.question_submitted = True
                            st.session_state.explanation_start_time = time.time()
                            st.rerun()
                    
                    # Show answer feedback and explanation if submitted
                    if st.session_state.question_submitted:
                        last_answer = st.session_state.answers[-1]
                        is_correct = last_answer['is_correct']
                        status_color = "#51cf66" if is_correct else "#ff6b6b"
                        status_text = "✅ Correct!" if is_correct else "❌ Incorrect"
                        
                        st.markdown(f"""
                            <div style="background: {'#f0fff4' if is_correct else '#fff5f5'}; 
                                        border: 2px solid {'#9ae6b4' if is_correct else '#fed7d7'}; 
                                        border-radius: 10px; padding: 1rem; margin: 1rem 0;">
                                <div style="color: {status_color}; font-size: 1.3rem; font-weight: bold; text-align: center;">
                                    {status_text}
                                </div>
                                <div style="color: #2d3748; text-align: center; margin-top: 0.5rem;">
                                    <strong>Your answer:</strong> {last_answer['user_answer'] if last_answer['user_answer'] else 'No answer provided'}<br>
                                    <strong>Correct answer:</strong> {last_answer['correct_answer']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Show explanation
                        st.markdown(f"""
                            <div class="explanation-card">
                                <div class="explanation-title">💡 Explanation</div>
                                <div class="explanation-text">
                                    Correct answer: {last_answer['correct_answer']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Auto-proceed timer and manual button
                        explanation_time_remaining = get_explanation_time_remaining()
                        
                        # Auto-proceed if time runs out
                        if explanation_time_remaining <= 0:
                            st.session_state.question_submitted = False
                            st.session_state.current_question += 1
                            
                            if st.session_state.current_question < len(st.session_state.questions):
                                st.session_state.start_time = time.time()
                            else:
                                st.session_state.quiz_completed = True
                            st.rerun()
                        else:
                            # Show countdown timer
                            st.markdown(f"""
                                <div style="text-align: center; margin: 1rem 0;">
                                    <p style="color: #667eea; font-size: 1.1rem;">
                                        Auto-proceeding in <strong>{explanation_time_remaining}</strong> seconds...
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Next question button
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("➡️ Next Question", key=f"next_{current_q_idx}"):
                            st.session_state.question_submitted = False
                            st.session_state.current_question += 1
                            
                            if st.session_state.current_question < len(st.session_state.questions):
                                st.session_state.start_time = time.time()
                            else:
                                st.session_state.quiz_completed = True
                            st.rerun()

                else:
                    # Regular multiple choice question
                    st.markdown(f"""
                        <div class="question-card">
                            <h2 style="color: #000000;">{question_data['Question']}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Options
                    options = {
                        'A': question_data['Option_A'],
                        'B': question_data['Option_B'],
                        'C': question_data['Option_C'],
                        'D': question_data['Option_D']
                    }
                    
                    # Show options (disabled if submitted)
                    if not st.session_state.question_submitted:
                        selected = st.radio(
                            "Select your answer:",
                            options.keys(),
                            format_func=lambda x: f"{x}. {options[x]}",
                            key=f"q_{current_q_idx}",
                            index=None  # This prevents any option from being pre-selected
                        )
                    else:
                        # Show selected answer as disabled
                        last_answer = st.session_state.answers[-1]
                        selected = last_answer['selected']
                        st.radio(
                            "Select your answer:",
                            options.keys(),
                            format_func=lambda x: f"{x}. {options[x]}",
                            key=f"q_{current_q_idx}_disabled",
                            index=list(options.keys()).index(selected) if selected else None,
                            disabled=True
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Submit button
                    if not st.session_state.question_submitted:
                        if st.button("✅ Submit Answer", key=f"submit_{current_q_idx}", disabled=selected is None):
                            is_correct = selected == question_data['Correct_Answer']
                            if is_correct:
                                st.session_state.score += 1
                            
                            st.session_state.answers.append({
                                'question': question_data['Question'],
                                'selected': selected,
                                'correct': question_data['Correct_Answer'],
                                'is_correct': is_correct,
                                'explanation': question_data['Explanation'],
                                'timed_out': False
                            })
                            
                            st.session_state.question_submitted = True
                            st.session_state.explanation_start_time = time.time()
                            st.rerun()
                    
                    # Show answer feedback and explanation if submitted
                    if st.session_state.question_submitted:
                        last_answer = st.session_state.answers[-1]
                        is_correct = last_answer['is_correct']
                        status_color = "#51cf66" if is_correct else "#ff6b6b"
                        status_text = "✅ Correct!" if is_correct else "❌ Incorrect"
                        
                        st.markdown(f"""
                            <div style="background: {'#f0fff4' if is_correct else '#fff5f5'}; 
                                        border: 2px solid {'#9ae6b4' if is_correct else '#fed7d7'}; 
                                        border-radius: 10px; padding: 1rem; margin: 1rem 0;">
                                <div style="color: {status_color}; font-size: 1.3rem; font-weight: bold; text-align: center;">
                                    {status_text}
                                </div>
                                <div style="color: #2d3748; text-align: center; margin-top: 0.5rem;">
                                    <strong>Your answer:</strong> {last_answer['selected']} &nbsp; | &nbsp;
                                    <strong>Correct answer:</strong> {last_answer['correct']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Show explanation
                        st.markdown(f"""
                            <div class="explanation-card">
                                <div class="explanation-title">💡 Explanation</div>
                                <div class="explanation-text">
                                    {last_answer['explanation']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Auto-proceed timer and manual button
                        explanation_time_remaining = get_explanation_time_remaining()
                        
                        # Auto-proceed if time runs out
                        if explanation_time_remaining <= 0:
                            st.session_state.question_submitted = False
                            st.session_state.current_question += 1
                            
                            if st.session_state.current_question < len(st.session_state.questions):
                                st.session_state.start_time = time.time()
                            else:
                                st.session_state.quiz_completed = True
                            st.rerun()
                        else:
                            # Show countdown timer
                            st.markdown(f"""
                                <div style="text-align: center; margin: 1rem 0;">
                                    <p style="color: #667eea; font-size: 1.1rem;">
                                        Auto-proceeding in <strong>{explanation_time_remaining}</strong> seconds...
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Next question button
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("➡️ Next Question", key=f"next_{current_q_idx}"):
                            st.session_state.question_submitted = False
                            st.session_state.current_question += 1
                            
                            if st.session_state.current_question < len(st.session_state.questions):
                                st.session_state.start_time = time.time()
                            else:
                                st.session_state.quiz_completed = True
                            st.rerun()
            
            # Auto-scroll to bottom when explanation is shown
            if st.session_state.question_submitted:
                st.markdown("""
                    <script>
                    setTimeout(function() {
                        scrollToBottom();
                    }, 100);
                    </script>
                """, unsafe_allow_html=True)
            
            # Auto-refresh for timer (only if not submitted) or explanation timer
            if not st.session_state.question_submitted:
                time.sleep(1)
                st.rerun()
            elif st.session_state.question_submitted and st.session_state.explanation_start_time:
                # Auto-refresh for explanation timer
                time.sleep(1)
                st.rerun()
        
    # Results screen
    elif st.session_state.quiz_completed:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Calculate score based on attempted questions only
            attempted_questions = [ans for ans in st.session_state.answers if ans.get('selected') is not None or ans.get('user_answer') or ans.get('timed_out')]
            correct_answers = [ans for ans in attempted_questions if ans.get('is_correct', False)]
            
            total_attempted = len(attempted_questions)
            total_correct = len(correct_answers)
            total_time = calculate_total_time()

            # Store the quiz result
            store_quiz_result(
                email=st.session_state.email,
                score=st.session_state.score,
                total_questions=len(st.session_state.questions),
                attempted_questions=total_attempted,
                correct_answers=total_correct,
                answers_data=st.session_state.answers,
                time_taken=total_time
            )
            
            # Calculate percentage based on attempted questions, not total questions
            if total_attempted > 0:
                percentage_score = int((total_correct / total_attempted) * 100)
            else:
                percentage_score = 0
            
            st.markdown(f"""
                <div class="result-card">
                    <h1 style="color: #667eea;">🎉 Quiz Completed!</h1>
                    <p style="font-size: 1.2rem; color: #4a5568; margin-bottom: 1rem;">
                        Thank you for participating, <strong>{st.session_state.email}</strong>!
                    </p>
                    <div class="score-display">
                        {total_correct} / {total_attempted}
                    </div>
                    <p style="font-size: 1.2rem; color: #4a5568;">
                        You scored {percentage_score}% on attempted questions
                    </p>
                    <p style="font-size: 1rem; color: #718096;">
                        Questions attempted: {total_attempted} out of {len(st.session_state.questions)}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Add leaderboard button in the result section
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🏆 View Leaderboard", use_container_width=True):
                    st.session_state.current_page = "leaderboard"
                    st.query_params["page"] = "leaderboard"
                    st.rerun()
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Detailed results
            st.markdown("""
                <div class="question-card">
                    <h2 style="color: #667eea; text-align: center;">📊 Detailed Results</h2>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, answer in enumerate(st.session_state.answers, 1):
                if answer.get('timed_out'):
                    status = "⏱️ Time's Up!"
                    color = "#ff6b6b"
                elif answer.get('is_correct'):
                    status = "✅ Correct"
                    color = "#51cf66"
                elif answer.get('selected') is None and not answer.get('user_answer'):
                    status = "⏭️ Not Attempted"
                    color = "#a0aec0"
                else:
                    status = "❌ Incorrect"
                    color = "#ff6b6b"
                
                if answer.get('type') == 'single_logo_quiz':
                    # Single logo quiz result
                    st.markdown(f"""
                        <div class="question-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h3 style="color: #000000; margin: 0;">Question {idx} (Logo Identification)</h3>
                                <span style="color: {color}; font-weight: bold; font-size: 1.2rem;">{status}</span>
                            </div>
                            <p style="font-size: 1.1rem; margin: 1rem 0; color: #000000;"><strong>{answer['question']}</strong></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the single logo
                    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
                    with col_img2:
                        st.image(answer['logo']['image'], width=150)
                        is_logo_correct = check_logo_answer(answer['user_answer'], answer['correct_answer'], answer['logo'].get('alt', []))
                        answer_color = "#51cf66" if is_logo_correct else "#ff6b6b"
                        st.markdown(f"""
                            <p style="color: {answer_color}; font-weight: bold; text-align: center;">
                                Your answer: {answer['user_answer'] if answer['user_answer'] else 'No answer'}<br>
                                Correct: {answer['correct_answer']}
                            </p>
                        """, unsafe_allow_html=True)
                else:
                    # Regular question result
                    st.markdown(f"""
                        <div class="question-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h3 style="color: #000000; margin: 0;">Question {idx}</h3>
                                <span style="color: {color}; font-weight: bold; font-size: 1.2rem;">{status}</span>
                            </div>
                            <p style="font-size: 1.1rem; margin: 1rem 0; color: #000000;"><strong>{answer['question']}</strong></p>
                            <p style="color: #000000;">
                                <strong>Your answer:</strong> {answer.get('selected', 'No answer (timeout)')}<br>
                                <strong>Correct answer:</strong> {answer['correct']}
                            </p>
                            {f'<p style="color: #000000; margin-top: 1rem;"><em>{answer.get("explanation", "")}</em></p>' if answer.get('selected') is not None and not answer.get('timed_out') else ''}
                        </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()