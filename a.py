import pandas as pd
import random
import smtplib
from email.message import EmailMessage
import keyring
import hashlib
import re
import streamlit as st
import os
from datetime import date
from streamlit_option_menu import option_menu

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SureCarry - Secure Package Delivery",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PROFESSIONAL UI STYLING ---
def apply_professional_ui():
    """
    Applies a sophisticated, modern, and professional UI theme.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --background-color: #0a0a0a;
            --primary-color: #1c1c1e;
            --secondary-color: #2c2c2e;
            --accent-color: #007aff;
            --text-color: #f5f5f7;
            --subtle-text-color: #8e8e93;
            --success-color: #34c759;
            --error-color: #ff3b30;
        }

        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: var(--background-color);
        }

        /* Main content container */
        .main .block-container {
            max-width: 900px;
            padding: 2rem 2rem 6rem 2rem;
            margin: auto;
        }

        /* Custom Header */
        .app-header {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem 0;
            border-bottom: 1px solid var(--secondary-color);
            margin-bottom: 2rem;
        }
        .app-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }
        .app-header .logo {
            font-size: 2.5rem;
            margin-right: 1rem;
        }

        /* Custom Cards */
        .custom-card {
            background-color: var(--primary-color);
            border: 1px solid var(--secondary-color);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }

        h3 {
            color: var(--text-color);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        p, .stMarkdown {
            color: var(--subtle-text-color);
            font-size: 1rem;
            line-height: 1.6;
        }

        /* Input fields styling */
        .stTextInput > div > div > input,
        .stDateInput > div > div > input {
            background-color: var(--secondary-color);
            color: var(--text-color);
            border: 1px solid #444;
            border-radius: 10px;
            padding: 1rem;
            font-size: 1rem;
            transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .stTextInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.3);
        }
        .stTextInput > label, .stDateInput > label {
            color: var(--text-color);
            font-weight: 500;
        }

        /* Button Styling */
        .stButton > button {
            background-color: var(--accent-color);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            transition: transform 0.2s ease, background-color 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #0056b3;
            transform: scale(1.03);
        }
        .stButton > button:active {
            transform: scale(0.98);
        }
        
        /* Alert Boxes */
        .stAlert {
            border-radius: 10px;
            border: none;
            font-weight: 500;
        }
        .stAlert[data-baseweb="alert-error"] { background-color: rgba(255, 59, 48, 0.2); color: var(--error-color); }
        .stAlert[data-baseweb="alert-success"] { background-color: rgba(52, 199, 89, 0.2); color: var(--success-color); }

        /* Search Result Card */
        .result-card {
            background-color: var(--secondary-color);
            border: 1px solid #444;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1rem;
            display: flex;
            align-items: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.4);
        }
        .result-icon { font-size: 2.5rem; margin-right: 1.5rem; color: var(--accent-color); }
        .result-details { flex-grow: 1; }
        .result-details strong { color: var(--text-color); }
        .result-details p { margin: 0.2rem 0; color: var(--subtle-text-color); }
        .result-contact { background-color: var(--accent-color); color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 500; }

        /* Footer */
        .footer { text-align: center; padding: 2rem 0; color: var(--subtle-text-color); font-size: 0.9rem; }
        </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
def initialize_session_state():
    """Initializes all required session state variables."""
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 'form'
    if 'generated_otp' not in st.session_state:
        st.session_state.generated_otp = None
    if 'traveler_data' not in st.session_state:
        st.session_state.traveler_data = None
    if 'otp_attempts' not in st.session_state:
        st.session_state.otp_attempts = 0

# --- SECURITY & VALIDATION HELPERS ---
def is_valid_name(name):
    """Validates name to allow letters, spaces, and basic punctuation."""
    return re.match(r"^[a-zA-Z\s'-]{2,}$", name)

def is_valid_pincode(pincode):
    """Validates a 6-digit Indian pincode."""
    return re.match(r"^\d{6}$", pincode)

# --- CORE LOGIC CLASSES ---
class TravelerRegistration:
    def __init__(self, name, surname, email, from_city, to_city, departure_date, arrival_date, departure_pincode):
        self.name = name.strip()
        self.surname = surname.strip()
        self.email = email.strip()
        self.from_city = from_city.strip()
        self.to_city = to_city.strip()
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.departure_pincode = departure_pincode

    def validate_email(self):
        """Validates Gmail address format."""
        return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", self.email)

    def send_otp(self):
        """Sends a secure OTP to the user's email via smtplib."""
        try:
            otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
            service_name = "PythonEmailSenderOTP"
            from_mail = 'sattigeriandsonspvtltd@gmail.com'
            app_password = keyring.get_password(service_name, from_mail)

            if not app_password:
                st.error("Email service credentials not configured on this server. Please contact the administrator.")
                return None

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_mail, app_password)
            msg = EmailMessage()
            msg['Subject'] = f'Your SureCarry Verification Code: {otp}'
            msg['From'] = from_mail
            msg['To'] = self.email
            msg.set_content(f"Hello {self.name},\n\nYour one-time verification code for SureCarry is: {otp}\n\nThis code is valid for 5 minutes. Do not share it with anyone.\n\nThank you,\nThe SureCarry Team")
            server.send_message(msg)
            server.quit()
            return otp
        except Exception as e:
            st.error(f"Failed to send OTP. Please check server logs or contact support. Error: {e}")
            return None

    def save_to_csv(self):
        """Saves user data to CSV."""
        try:
            csv_file = 'travelers.csv'
            new_data = {'name': self.name, 'surname': self.surname, 'email': self.email, 'from_city': self.from_city, 'to_city': self.to_city, 'departure_date': str(self.departure_date), 'arrival_date': str(self.arrival_date), 'departure_pincode': self.departure_pincode}
            
            if not os.path.exists(csv_file):
                df = pd.DataFrame([new_data])
            else:
                df = pd.read_csv(csv_file)
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            
            df.to_csv(csv_file, index=False)
            return True
        except Exception as e:
            st.error(f"A database error occurred while saving your data. Error: {e}")
            return False

class TravelerSearch:
    def search(self, from_city, to_city, departure_pincode):
        """Searches for travelers in the CSV database."""
        try:
            csv_file = 'travelers.csv'
            if not os.path.exists(csv_file): return pd.DataFrame()
            df = pd.read_csv(csv_file)
            df['departure_pincode'] = df['departure_pincode'].astype(str)
            
            # Perform case-insensitive and whitespace-insensitive search
            results = df[
                (df['from_city'].str.strip().str.lower() == from_city.strip().lower()) &
                (df['to_city'].str.strip().str.lower() == to_city.strip().lower()) &
                (df['departure_pincode'].str.strip() == departure_pincode.strip())
            ]
            # Exclude password hash from search results if it exists
            return results.drop(columns=['password'], errors='ignore')
        except Exception as e:
            st.error(f"An error occurred during the search. Error: {e}")
            return pd.DataFrame()

# --- UI RENDERING FUNCTIONS ---
def render_header():
    """Renders the main application header and navigation."""
    st.markdown('<div class="app-header"><span class="logo">✈️</span><h1>SureCarry</h1></div>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, options=["Register", "Find Traveler", "Info"],
        icons=["person-plus-fill", "search", "info-circle-fill"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "border-bottom": "1px solid #2c2c2e"},
            "icon": {"color": "#007aff", "font-size": "20px"},
            "nav-link": {
                "font-size": "1rem",
                "font-weight": "600",
                "color": "#8e8e93",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#2c2c2e",
            },
            "nav-link-selected": {"background-color": "#2c2c2e", "color": "#f5f5f7"},
        }
    )
    return selected

def render_registration_page():
    """Manages the multi-step registration flow."""
    if st.session_state.registration_step == 'form':
        render_registration_form()
    elif st.session_state.registration_step == 'otp':
        render_otp_verification()
    elif st.session_state.registration_step == 'complete':
        render_registration_complete()

def render_registration_form():
    """Renders the main user registration form with validation."""
    with st.form("traveler_registration_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("<h3>Register as a Traveler</h3><p>Complete the form below to join our network. All fields are required.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("First Name", placeholder="e.g., Anjali")
            from_city = st.text_input("Departure City", placeholder="e.g., Pune")
            departure_date = st.date_input("Departure Date", min_value=date.today())
            departure_pincode = st.text_input("Departure Pincode", placeholder="e.g., 411033", max_chars=6)
            
        with col2:
            surname = st.text_input("Last Name", placeholder="e.g., Sharma")
            to_city = st.text_input("Destination City", placeholder="e.g., Delhi")
            arrival_date = st.date_input("Arrival Date", min_value=date.today())
        
        email = st.text_input("Gmail Address for Verification", placeholder="your.email@gmail.com")
        
        st.markdown("</div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Register & Send OTP", use_container_width=True)

    if submit_btn:
        # --- Comprehensive Validation ---
        errors = []
        if not is_valid_name(name) or not is_valid_name(surname) or not is_valid_name(from_city) or not is_valid_name(to_city):
            errors.append("Names and cities must contain only letters and spaces.")
        if not is_valid_pincode(departure_pincode):
            errors.append("Please enter a valid 6-digit pincode.")
        if departure_date >= arrival_date:
            errors.append("Arrival date must be after the departure date.")
        
        traveler = TravelerRegistration(name, surname, email, from_city, to_city, departure_date, arrival_date, departure_pincode)
        if not traveler.validate_email():
            errors.append("Please enter a valid Gmail address.")
            
        if errors:
            for error in errors: st.error(error)
        else:
            with st.spinner("Sending verification code..."):
                otp = traveler.send_otp()
            if otp:
                st.session_state.traveler_data = traveler
                st.session_state.generated_otp = otp
                st.session_state.registration_step = 'otp'
                st.session_state.otp_attempts = 0 # Reset attempts on new OTP
                st.success("Verification code sent! Please check your email.")
                st.rerun()

def render_otp_verification():
    """Renders the OTP verification step with brute-force protection."""
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown(f"<h3>Enter Verification Code</h3><p>A 6-digit code was sent to <strong>{st.session_state.traveler_data.email}</strong>.</p>", unsafe_allow_html=True)
    
    if st.session_state.otp_attempts >= 3:
        st.error("Too many failed attempts. Please restart the registration process.")
    else:
        with st.form("otp_verification_form"):
            entered_otp = st.text_input("Verification Code", placeholder="______", max_chars=6)
            verify_btn = st.form_submit_button("Verify & Complete Registration", use_container_width=True)
        
        if verify_btn:
            if entered_otp == st.session_state.generated_otp:
                with st.spinner("Finalizing your registration..."):
                    if st.session_state.traveler_data.save_to_csv():
                        st.session_state.registration_step = 'complete'
                        st.rerun()
            else:
                st.session_state.otp_attempts += 1
                attempts_left = 3 - st.session_state.otp_attempts
                st.error(f"Invalid code. You have {attempts_left} attempt(s) left.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_registration_complete():
    """Displays a success message upon completion."""
    st.balloons()
    st.success("Registration Successful! Welcome to SureCarry.")
    st.markdown('<div class="custom-card"><h3>You are now part of our trusted network!</h3><p>Senders looking for travelers on your route can now find and contact you. Thank you for joining.</p></div>', unsafe_allow_html=True)
    if st.button("Register Another Traveler"):
        initialize_session_state()
        st.rerun()

def render_search_page():
    """Renders the traveler search form and displays results."""
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("<h3>Find a Traveler</h3><p>Enter a route to find registered travelers who can carry your package.</p>", unsafe_allow_html=True)
    
    with st.form("search_form"):
        col1, col2, col3 = st.columns(3)
        with col1: search_from = st.text_input("From City", placeholder="e.g., Pune")
        with col2: search_to = st.text_input("To City", placeholder="e.g., Delhi")
        with col3: search_pincode = st.text_input("Departure Pincode", placeholder="e.g., 411033", max_chars=6)
        search_btn = st.form_submit_button("Search Travelers", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    if search_btn:
        errors = []
        if not is_valid_name(search_from) or not is_valid_name(search_to):
            errors.append("Please enter valid city names.")
        if not is_valid_pincode(search_pincode):
            errors.append("Please enter a valid 6-digit pincode.")
        
        if errors:
            for error in errors: st.error(error)
        else:
            searcher = TravelerSearch()
            with st.spinner("Searching for travelers..."):
                results = searcher.search(search_from, search_to, search_pincode)
            
            st.markdown(f"### Search Results ({len(results)})")
            if results.empty:
                st.warning("No travelers found for this route. Be the first to register for it!")
            else:
                for _, row in results.iterrows():
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-icon">👤</div>
                        <div class="result-details">
                            <p><strong>{row['name']} {row['surname']}</strong></p>
                            <p>✈️ {row['from_city']} → {row['to_city']}</p>
                            <p>📅 {row['departure_date']} to {row['arrival_date']}</p>
                        </div>
                        <a href="mailto:{row['email']}" class="result-contact">Contact</a>
                    </div>
                    """, unsafe_allow_html=True)

def render_info_page():
    """Renders the info page with legal policies."""
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("<h3>Information Center</h3><p>Review our policies to understand your rights and responsibilities.</p>", unsafe_allow_html=True)
    with st.expander("🔒 Privacy Policy", expanded=True):
        st.markdown("""*(A comprehensive, legally-vetted privacy policy would be inserted here, detailing data collection, usage, storage, user rights, and compliance with Indian laws like the IT Act, 2000 and DPDP Act, 2023.)*""")
    with st.expander("⚖️ Terms & Conditions"):
        st.markdown("""*(A detailed Terms & Conditions document would be here, outlining the platform's role as an intermediary, user responsibilities, liability limitations, and legal disclaimers as per Indian contract and criminal law.)*""")
    st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN APPLICATION ---
def main():
    initialize_session_state()
    apply_professional_ui()
    
    selected_page = render_header()

    if selected_page == "Register":
        render_registration_page()
    elif selected_page == "Find Traveler":
        render_search_page()
    elif selected_page == "Info":
        render_info_page()
        
    st.markdown("<div class='footer'>© 2025 SureCarry | A Secure Peer-to-Peer Delivery Network</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
