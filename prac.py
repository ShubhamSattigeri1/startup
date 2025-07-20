import pandas as pd
import random
import smtplib
from email.message import EmailMessage
import keyring
import re
import streamlit as st
import os

# Configure Streamlit page
st.set_page_config(
    page_title="SureCarry - Travel Package Delivery",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class From:
    def __init__(self, name=None, surname=None, mail=None, from1=None, to=None, depat_date=None, arr_date=None, departure_pincode=None):
        self.name = name
        self.surname = surname
        self.mail = mail
        self.from1 = from1
        self.to = to
        self.depat_date = depat_date
        self.arr_date = arr_date
        self.departure_pincode = departure_pincode

    def send_otp(self, mail):
        """Send OTP to user's email"""
        try:
            otp = ""
            for i in range(6):
                otp += str(random.randint(0, 9))
            
            service_name = "PythonEmailSenderOTP"
            from_mail = 'sattigeriandsonspvtltd@gmail.com'

            app_password = keyring.get_password(service_name, from_mail)

            if not app_password:
                st.error("Email service not configured. Please contact administrator.")
                return None

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_mail, app_password)

            msg = EmailMessage()
            msg['Subject'] = 'OTP Verification - SureCarry'
            msg['From'] = from_mail
            msg['To'] = mail
            msg.set_content(f"Your One-Time Password (OTP) is: {otp}\n\nThis OTP is valid for a single use.\n\nThank you for using SureCarry!")

            server.send_message(msg)
            server.quit()
            
            return otp
        except Exception as e:
            st.error(f"Error sending OTP: {str(e)}")
            return None

    def validate_email(self, email):
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._]+@gmail\.com$"
        return re.match(pattern, email) is not None

    def data_entry(self):
        """Save user data to CSV"""
        try:
            # Check if CSV exists, if not create it
            csv_file = 'from_to.csv'
            if not os.path.exists(csv_file):
                df = pd.DataFrame(columns=['name', 'surname', 'mail', 'from1', 'to', 'depat_date', 'arr_date','departure_pincode'])
                df.to_csv(csv_file, index=False)
            
            df = pd.read_csv(csv_file)
            append_data = pd.DataFrame([{
                'name': self.name,
                'surname': self.surname,
                'mail': self.mail,
                'from1': self.from1,
                'to': self.to,
                'depat_date': self.depat_date,
                'arr_date': self.arr_date,
                'departure_pincode': self.departure_pincode
            }])
            df = pd.concat([df, append_data], ignore_index=True)
            df.to_csv(csv_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")
            return False

class To:
    def __init__(self, from2=None, to=None, departure_pincode=None):
        self.from2 = from2
        self.to = to
        self.departure_pincode = departure_pincode
    
    def search_travelers(self, from1, to, departure_pincode=None, departure_date=None):
        """Search for travelers on the specified route"""
        try:
            csv_file = 'from_to.csv'
            if not os.path.exists(csv_file):
                return pd.DataFrame()
            
            df = pd.read_csv(csv_file)
            
            # Filter by route (case-insensitive)
            output_df = df[(df['from1'].str.lower().str.strip() == from1.lower().strip()) & 
                          (df['to'].str.lower().str.strip() == to.lower().strip()) & (df['departure_pincode'].str.lower().str.strip() == departure_pincode.lower().strip())]
            
            # If departure date is specified, filter by it
            if departure_date:
                # Convert departure_date to string for comparison
                departure_date_str = str(departure_date)
                output_df = output_df[output_df['depat_date'].astype(str) == departure_date_str]
            
            return output_df
        except Exception as e:
            st.error(f"Error searching travelers: {str(e)}")
            return pd.DataFrame()

def privacy_policy():
    """Return the SureCarry Privacy Policy"""
    return """
    # Privacy Policy – SureCarry
    
    ## 1. Introduction
    SureCarry ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, store, and disclose your personal information when you use our mobile application and related services (collectively, the "Platform").
    
    ## 2. Information We Collect
    We may collect the following types of information:
    - **Personal Identification Information**: Name, email address, phone number, address, ID documents.
    - **Flight and Travel Information**: Traveler routes, dates, airline details.
    - **Package Details**: Weight, dimensions, declared contents.
    - **Technical Information**: IP address, device type, OS, app version, and usage data.
    
    ## 3. How We Use Your Information
    We use your information to:
    - Facilitate sender-traveler connections.
    - Ensure safety and security of transactions.
    - Improve our services and user experience.
    - Comply with legal obligations under Indian law, including requests from law enforcement agencies.
    
    ## 4. Legal Basis for Processing
    Our legal basis for processing your data includes:
    - **Consent**: When you voluntarily provide information.
    - **Contract**: To fulfill obligations under the Terms and Conditions.
    - **Legal Obligation**: Under Section 91 CrPC and Section 69 of the Information Technology Act, 2000.
    - **Legitimate Interest**: To operate, improve, and secure the Platform.
    
    ## 5. Data Sharing and Disclosure
    We do not sell or rent your personal information. However, we may share your data with:
    - Law enforcement and government agencies upon valid legal requests.
    - Payment processors and IT service providers under strict confidentiality.
    - Other users only as necessary for service fulfillment (e.g., sender and traveler coordination).
    
    ## 6. Data Retention
    We retain your data only as long as necessary to fulfill the purposes outlined in this Policy, or as required by law. This may include retention after account deactivation for compliance and audit purposes.
    
    ## 7. User Rights
    You have the right to:
    - Access and review your personal data.
    - Request correction or deletion of your data.
    - Withdraw consent where processing is based on consent.
    - Lodge a complaint with appropriate authorities under the IT Act, 2000.
    
    ## 8. Data Security
    We implement industry-standard security practices in accordance with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011. These include encryption, access control, and periodic audits.
    
    ## 9. Children's Privacy
    Our Platform is not intended for users under the age of 18. We do not knowingly collect personal information from minors.
    
    ## 10. Changes to This Policy
    We may update this Privacy Policy from time to time. You are encouraged to review this page periodically. Continued use of the Platform signifies acceptance of the revised Policy.
    
    ## 11. Contact Us
    If you have any questions or concerns regarding this Privacy Policy, contact us at:
    **Email**: samarthmalusarnsg@gmail.com
    """

def terms_and_conditions():
    """Return the SureCarry Terms and Conditions"""
    return """
    # Terms and Conditions – SureCarry
    
    ## 1. Nature of the Platform
    SureCarry is a digital intermediary that facilitates the connection between package senders and travelers willing to carry items during their travel. The Company acts only as a neutral, technology-driven platform and does not assume the role of a courier, logistics service, or contractual party to the delivery transaction between users.

    ## 2. Eligibility
    You must be 18 years or older and competent to contract as per the Indian Contract Act, 1872 to use the Platform. You agree to provide truthful, lawful, and complete information during registration and use of the Platform.

    ## 3. Responsibilities of Users

    ### 3.1 Senders:
    Must ensure that the contents of the package are lawful, not restricted under customs or airline rules, and comply with Indian law, including but not limited to:
    - The Narcotic Drugs and Psychotropic Substances Act, 1985
    - The Arms Act, 1959
    - The Explosives Act, 1884
    - The Wildlife Protection Act, 1972
    
    Senders are solely liable for the nature, content, and legality of the package.

    ### 3.2 Travelers:
    Travelers must verify the contents of the package before accepting it for transit. The Company assumes no responsibility for any illegal items handed to a traveler with or without their knowledge. The traveler is individually liable for ensuring that they are not transporting contraband or prohibited goods, as per:
    - Sections 23, 24, 25 of the NDPS Act
    - Sections 471, 474, 489 of the Indian Penal Code (IPC)
    - Airport Authority Guidelines and Customs Law

    ### 3.3 Receivers:
    Must inspect the package upon receipt and immediately notify the sender of any issues.

    ## 4. Platform Disclaimer & Legal Liability
    SureCarry is not liable for:
    - Loss, theft, delay, or damage to goods by the traveler.
    - Any misuse, smuggling, or transport of illegal goods by users.
    - Disputes arising between sender, traveler, or receiver.
    
    In accordance with Sections 34 and 120B of the IPC, SureCarry has no common intention or conspiracy in the transaction and cannot be held criminally liable for individual user conduct.
    
    In case of criminal activity, users are solely responsible under:
    - Section 403 IPC – Dishonest misappropriation of property
    - Section 406 IPC – Criminal breach of trust
    - Section 420 IPC – Cheating and dishonestly inducing delivery of property
    - Section 468 IPC – Forgery for the purpose of cheating
    - Customs Act, 1962 and relevant Airlines and Aviation Security Regulations

    ## 5. Cooperation with Legal Authorities
    If any user violates Indian law, SureCarry shall not be held accountable. Upon receipt of a valid request or notice under:
    - Section 91 of CrPC (Production of Documents) or
    - Section 69 of the Information Technology Act, 2000,
    
    we will provide user data, transaction logs, and communication history to law enforcement agencies.
    This includes cooperation with CISF, Customs, DGCA, local police, and cybercrime authorities.

    ## 6. Code of Conduct
    Users are strictly prohibited from:
    - Transporting items banned under international or Indian law.
    - Misrepresenting the nature of the goods.
    - Using the platform for money laundering, trafficking, or terrorist financing, in violation of the Prevention of Money Laundering Act, 2002 or UAPA, 1967.

    ## 7. Limitation of Liability
    We shall not be liable for any direct, indirect, incidental, special, or consequential damages arising out of or relating to:
    - Use or inability to use the Platform,
    - Unauthorized access or alteration of user transmissions,
    - Acts of third-party service providers or users,
    even if we have been advised of the possibility of such damages.

    ## 8. Termination and Suspension
    We reserve the right to suspend or terminate any user account at our sole discretion for violation of these Terms or applicable laws. In case of any legal violation, your data may be retained and shared with the appropriate authorities.

    ## 9. Intellectual Property
    All content, branding, software, and design elements in SureCarry are intellectual property of the Company. Users may not copy, reverse engineer, or distribute any part of the Platform without explicit permission.

    ## 10. Privacy and Data Security
    Our handling of personal data is governed by our Privacy Policy. We comply with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011.

    ## 11. Governing Law and Jurisdiction
    These Terms are governed by the laws of the Republic of India. Any disputes shall be subject to the exclusive jurisdiction of the courts of Pune, Maharashtra.

    ## 12. Contact
    For any questions or legal concerns, contact us at:
    **Email**: samarthmalusarnsg@gmail.com

    By accessing or using the SureCarry Platform, you confirm that you have read, understood, and agree to abide by these legally binding Terms and Conditions.
    """

def main():
    # Header
    st.title("✈️ SureCarry - Travel Package Delivery Platform")
    st.markdown("*Connecting travelers with package senders for secure and convenient delivery*")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Register as Traveler", "🔍 Find Travelers", "🔒 Privacy Policy", "📋 Terms & Conditions"])
    
    with tab1:
        st.header("Register as a Traveler")
        st.markdown("Register your travel details to help others send packages through you.")
        
        with st.form("traveler_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("First Name *", help="Enter your first name")
                surname = st.text_input("Last Name *", help="Enter your last name")
                mail = st.text_input("Gmail Address *", help="Enter your Gmail address for OTP verification")
                from1 = st.text_input("Departure City *", help="City you're departing from")
            
            with col2:
                to = st.text_input("Destination City *", help="City you're traveling to")
                depat_date = st.date_input("Departure Date *", help="Select your departure date")
                arr_date = st.date_input("Arrival Date *", help="Select your arrival date")
                departure_pincode = st.text_input("departure_pincode *", help="City you're living in.Pincode.")
            
            submit_button = st.form_submit_button("Register & Verify Email")
            
            if submit_button:
                # Validate required fields
                if not all([name, surname, mail, from1, to, depat_date, arr_date, departure_pincode]):
                    st.error("Please fill in all required fields.")
                elif not From().validate_email(mail):
                    st.error("Please enter a valid Gmail address.")
                else:
                    # Initialize session state for OTP
                    if 'otp_sent' not in st.session_state:
                        st.session_state.otp_sent = False
                    if 'generated_otp' not in st.session_state:
                        st.session_state.generated_otp = None
                    
                    # Send OTP
                    if not st.session_state.otp_sent:
                        traveler = From(name, surname, mail, from1, to, depat_date, arr_date, departure_pincode)
                        generated_otp = traveler.send_otp(mail)
                        
                        if generated_otp:
                            st.session_state.generated_otp = generated_otp
                            st.session_state.otp_sent = True
                            st.session_state.traveler_data = traveler
                            st.success("OTP sent successfully! Please check your email.")
                        else:
                            st.error("Failed to send OTP. Please try again.")
        
        # OTP Verification Section
        if st.session_state.get('otp_sent', False):
            st.markdown("---")
            st.subheader("Email Verification")
            
            with st.form("otp_form"):
                entered_otp = st.text_input("Enter OTP", max_chars=6, help="Enter the 6-digit OTP sent to your email")
                verify_button = st.form_submit_button("Verify OTP & Complete Registration")
                
                if verify_button:
                    if entered_otp == st.session_state.generated_otp:
                        # Save data
                        if st.session_state.traveler_data.data_entry():
                            st.success("✅ Registration completed successfully!")
                            st.balloons()
                            # Clear session state
                            st.session_state.otp_sent = False
                            st.session_state.generated_otp = None
                            st.session_state.traveler_data = None
                        else:
                            st.error("Failed to save registration data.")
                    else:
                        st.error("Invalid OTP. Please try again.")
    
    with tab2:
        st.header("Find Travelers")
        st.markdown("Search for travelers on your desired route.")
        
        with st.form("search_form"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                search_from = st.text_input("From City *", help="Enter departure city")
            with col2:
                search_to = st.text_input("To City *", help="Enter destination city")
            with col3:
                departure_pincode = st.text_input("departure_pincode", help="Entre your departure pincide.")       
            with col4:
                search_date = st.date_input("Travel Date (Optional)", help="Filter by specific travel date")
             
            
            search_button = st.form_submit_button("Search Travelers")
            
            if search_button:
                if not search_from or not search_to:
                    st.error("Please enter both departure and destination cities.")
                else:
                    searcher = To()
                    results = searcher.search_travelers(
                        search_from, 
                        search_to, 
                        departure_pincode,
                        search_date if search_date else None
                    )
                    
                    if results.empty:
                        st.warning("🔍 No travelers found on this route. You might be the pioneer of this route!")
                    else:
                        st.success(f"Found {len(results)} traveler(s) on your route:")
                        
                        # Display results in a nice format
                        for index, row in results.iterrows():
                            with st.expander(f"✈️ {row['name']} {row['surname']} - {row['from1']} → {row['to']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Name:** {row['name']} {row['surname']}")
                                    st.write(f"**Email:** {row['mail']}")
                                    st.write(f"**Route:** {row['from1']} → {row['to']}")
                                with col2:
                                    st.write(f"**Departure Date:** {row['depat_date']}")
                                    st.write(f"**Arrival Date:** {row['arr_date']}")
                                    st.write(f"**departure_pincode:** {row['departure_pincode']}")
                                
                                st.info("💡 Contact this traveler directly via email to coordinate package delivery.")
    
    with tab3:
        st.header("Privacy Policy")
        st.markdown(privacy_policy())
    
    with tab4:
        st.header("Terms & Conditions")
        st.markdown(terms_and_conditions())

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>© 2024 SureCarry - Travel Package Delivery Platform</p>
            <p>For support, contact: samarthmalusarnsg@gmail.com</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    main()