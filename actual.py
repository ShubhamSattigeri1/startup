# From 
# tota weight
# type of product
# name
# msil id
# TO
import pandas as pd
import random
import smtplib
from email.message import EmailMessage
import keyring
import re

class From:
    def __init__(self, name = None, surname = None, mail = None, from1 = None, to = None, depat_date = None, arr_date = None, departure_pincode=None):
        self.name = name
        self.surname = surname
        self.mail = mail
        self.from1 = from1
        self.to = to
        self.depat_date = depat_date
        self.arr_date = arr_date
        self.departure_pincode = departure_pincode

    def from_traveler(self, name = None, surname = None, mail = None, from1 = None, to = None, depat_date = None, arr_date = None, departure_pincode=None):
        if not name:
            name = input("\nEnter Your Name :  ")
            while not name:
                print("\nPlease Enter a valid name.")
                name = input("\nEnter a valid Name : ")
        self.name = name

        if not surname:
            surname = input("Enter Your surname :  ")
            while not surname:
                print("Please Enter a valid surname.")
                surname = input("Enter a valid surname : ")
        self.surname = surname      

        otp = ""
        for i in range(6):
            otp += str(random.randint(0, 9))
        service_name = "PythonEmailSenderOTP"
        from_mail = 'sattigeriandsonspvtltd@gmail.com'

        app_password = keyring.get_password(service_name, from_mail)

        if not app_password:
            raise ValueError(
        f"Password not found for service '{service_name}' and user '{from_mail}'. "
        "Please run the 'store_password.py' script first to store your App Password.")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Secure the connection
        server.login(from_mail, app_password) # Use the securely retrieved App Password

        if not mail:
            mail = input("Enter the recipient Gmail ID: ")
            if re.search(r"^[a-zA-Z0-9._]+@gmail\.com$", mail):
                self.mail = mail
                msg = EmailMessage()
                msg['Subject'] = 'OTP Verification.'
                msg['From'] = from_mail
                msg['To'] = mail
                msg.set_content(f"Your One-Time Password (OTP) is: {otp}\n\nThis OTP is valid for a single use.")

                server.send_message(msg)
                print("OTP Email Sent Successfully!")

                server.quit()

                print("\n--- OTP Verification ---")
                otp2 = input("Enter the OTP you received: ") # Read OTP as a string
                if otp == otp2:
                    print('OTP verified with our system..')
                else:
                    while otp != otp2:
                        print("Enter Correct OTP, PLEASE DON'T WASTE OUR TIME.")
                        otp2 = input("Enter the OTP you received: ") # Read OTP as a string        
        else:
            print("invalid")
            while re.search(r"^[a-zA-Z0-9._]+@gmail\.com$", mail) != True:
                print("Please enter your mail id.")
                tmail = input("Enter Your Gmail ID : ")
                
        
        if not from1:
            from1 = input("Enter Your from1 :  ")
            while not from1:
                print("Please Enter a valid from1.")
                from1 = input("Enter a valid from1 : ")
        self.from1 = from1

        if not to:
            name = input("Enter Your to :  ")
            while not to:
                print("Please Enter a valid to.")
                to = input("Enter a valid to : ")
        self.to = to

        if not depat_date:
            depat_date = input("Enter Your depat_date :  ")
            while not depat_date:
                print("Please Enter a valid depat_date.")
                depat_date = input("Enter a valid depat_date : ")
        self.depat_date = depat_date
        
        if not arr_date:
            arr_date = input("Enter Your arr_date :  ")
            while not arr_date:
                print("Please Enter a valid arr_date.")
                arr_date = input("Enter a arr_date : ")
        self.arr_date = arr_date

        if not departure_pincode:
            departure_pincode = input("Enter your Departure pincode : ")
            while not departure_pincode:
                print("Please Enter Departure pincode.")
                departure_pincode = input("Enter your Departure pincode : ")
        self.departure_pincode = departure_pincode        

    def data_entry(self):
        df = pd.read_csv('from_to.csv')    
        append_data = pd.DataFrame([{'name' : self.name, 'surname' : self.surname, 'mail' : self.mail, 'from1' : self.from1, 'to' : self.to, 'depat_date' : self.depat_date, 'arr_date' : self.arr_date, 'departure_pincode' : self.departure_pincode}])      
        df = pd.concat([df, append_data])
        df.to_csv('from_to.csv', index = False)
        print("\nDetails registered Successfully...")

class To:
    def __init__(self, from2 = None, to = None,departure_pincode=None):
        self.from2 = from2
        self.to = to
        self.departure_pincode = departure_pincode

    
    def to_traveler(self, from1 = None, to = None, deaparture_date= None,departure_pincode=None):
        if not from1:
            from1 = input("Enter the departure Destination : ")
            while not from1:
                print("\nPrint the Departure airport please.")
                from1 = input("Enter Departure Destination : ")
        self.from1 = from1

        if not to:
            to = input("Enter the Arrival Destination : ")
            while not to:
                print("\nPrint the Arrival airport please.")
                to = input("Enter Arrival Destination : ")
        self.to = to

        if not deaparture_date:
            deaparture_date = input("Enter the deaparture_date : ")
            while not deaparture_date:
                print("\nPrint the deaparture_date please.")
                from1 = input("Enter deaparture_date : ")
        self.deaparture_date = deaparture_date

        if not departure_pincode:
            departure_pincode = input("Enter your Departure pincode : ")
            while not departure_pincode:
                print("Please Enter Departure pincode.")
                departure_pincode = input("Enter your Departure pincode : ")
        self.departure_pincode = departure_pincode   

        df2 = pd.read_csv('from_to.csv')
        output_df = df2[(df2['from1'] == from1) & (df2['to'] == to) | (df2['departure_pincode'] == departure_pincode)]
        
        if output_df.empty:
            print("OOPs..! No traveler was found on your route, might you are the pioneer of this route.")  
        else:
            print(output_df[['name','surname','from1','to','depat_date','departure_pincode']].to_string(index=False))

def privacy():
    """
    Prints the SureCarry Privacy Policy.
    """
    privacy_policy_text = """Privacy Policy – SureCarry
1. Introduction
SureCarry (“we”, “our”, or “us”) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, store, and disclose your personal information when you use our mobile application and related services (collectively, the “Platform”).
2. Information We Collect
We may collect the following types of information:
- Personal Identification Information: Name, email address, phone number, address, ID documents.
- Flight and Travel Information: Traveler routes, dates, airline details.
- Package Details: Weight, dimensions, declared contents.
- Technical Information: IP address, device type, OS, app version, and usage data.
3. How We Use Your Information
We use your information to:
- Facilitate sender-traveler connections.
- Ensure safety and security of transactions.
- Improve our services and user experience.
- Comply with legal obligations under Indian law, including requests from law enforcement agencies.
4. Legal Basis for Processing
Our legal basis for processing your data includes:
- Consent: When you voluntarily provide information.
- Contract: To fulfill obligations under the Terms and Conditions.
- Legal Obligation: Under Section 91 CrPC and Section 69 of the Information Technology Act, 2000.
- Legitimate Interest: To operate, improve, and secure the Platform.
5. Data Sharing and Disclosure
We do not sell or rent your personal information. However, we may share your data with:
- Law enforcement and government agencies upon valid legal requests.
- Payment processors and IT service providers under strict confidentiality.
- Other users only as necessary for service fulfillment (e.g., sender and traveler coordination).
6. Data Retention
We retain your data only as long as necessary to fulfill the purposes outlined in this Policy, or as required by law. This may include retention after account deactivation for compliance and audit purposes.
7. User Rights
You have the right to:
- Access and review your personal data.
- Request correction or deletion of your data.
- Withdraw consent where processing is based on consent.
- Lodge a complaint with appropriate authorities under the IT Act, 2000.
8. Data Security
We implement industry-standard security practices in accordance with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011. These include encryption, access control, and periodic audits.
9. Children's Privacy
Our Platform is not intended for users under the age of 18. We do not knowingly collect personal information from minors.
10. Changes to This Policy
We may update this Privacy Policy from time to time. You are encouraged to review this page periodically. Continued use of the Platform signifies acceptance of the revised Policy.
11. Contact Us
If you have any questions or concerns regarding this Privacy Policy, contact us at:
Email: samarthmalusarnsg@gmail.com"""
    print(privacy_policy_text)


def TnC():
    TnC = """Privacy Policy – SureCarry
Terms and Conditions – SureCarry
1. Nature of the Platform
SureCarry is a digital intermediary that facilitates the connection between package senders and travelers willing to carry items during their travel. The Company acts only as a neutral, technology-driven platform and does not assume the role of a courier, logistics service, or contractual party to the delivery transaction between users.

2. Eligibility
You must be 18 years or older and competent to contract as per the Indian Contract Act, 1872 to use the Platform. You agree to provide truthful, lawful, and complete information during registration and use of the Platform.

3. Responsibilities of Users

3.1 Senders:
Must ensure that the contents of the package are lawful, not restricted under customs or airline rules, and comply with Indian law, including but not limited to:
- The Narcotic Drugs and Psychotropic Substances Act, 1985
- The Arms Act, 1959
- The Explosives Act, 1884
- The Wildlife Protection Act, 1972
Senders are solely liable for the nature, content, and legality of the package.

3.2 Travelers:
Travelers must verify the contents of the package before accepting it for transit. The Company assumes no responsibility for any illegal items handed to a traveler with or without their knowledge. The traveler is individually liable for ensuring that they are not transporting contraband or prohibited goods, as per:
- Sections 23, 24, 25 of the NDPS Act
- Sections 471, 474, 489 of the Indian Penal Code (IPC)
- Airport Authority Guidelines and Customs Law

3.3 Receivers:
Must inspect the package upon receipt and immediately notify the sender of any issues.

4. Platform Disclaimer & Legal Liability
ViaWings is not liable for:
- Loss, theft, delay, or damage to goods by the traveler.
- Any misuse, smuggling, or transport of illegal goods by users.
- Disputes arising between sender, traveler, or receiver.
In accordance with Sections 34 and 120B of the IPC, ViaWings has no common intention or conspiracy in the transaction and cannot be held criminally liable for individual user conduct.
In case of criminal activity, users are solely responsible under:
- Section 403 IPC – Dishonest misappropriation of property
- Section 406 IPC – Criminal breach of trust
- Section 420 IPC – Cheating and dishonestly inducing delivery of property
- Section 468 IPC – Forgery for the purpose of cheating
- Customs Act, 1962 and relevant Airlines and Aviation Security Regulations

5. Cooperation with Legal Authorities
If any user violates Indian law, SureCarry shall not be held accountable. Upon receipt of a valid request or notice under:
- Section 91 of CrPC (Production of Documents) or
- Section 69 of the Information Technology Act, 2000,
we will provide user data, transaction logs, and communication history to law enforcement agencies.
This includes cooperation with CISF, Customs, DGCA, local police, and cybercrime authorities.

6. Code of Conduct
Users are strictly prohibited from:
- Transporting items banned under international or Indian law.
- Misrepresenting the nature of the goods.
- Using the platform for money laundering, trafficking, or terrorist financing, in violation of the Prevention of Money Laundering Act, 2002 or UAPA, 1967.

7. Limitation of Liability
We shall not be liable for any direct, indirect, incidental, special, or consequential damages arising out of or relating to:
- Use or inability to use the Platform,
- Unauthorized access or alteration of user transmissions,
- Acts of third-party service providers or users,
even if we have been advised of the possibility of such damages.

8. Termination and Suspension
We reserve the right to suspend or terminate any user account at our sole discretion for violation of these Terms or applicable laws. In case of any legal violation, your data may be retained and shared with the appropriate authorities.

9. Intellectual Property
All content, branding, software, and design elements in SureCarry are intellectual property of the Company. Users may not copy, reverse engineer, or distribute any part of the Platform without explicit permission.

10. Privacy and Data Security
Our handling of personal data is governed by our Privacy Policy. We comply with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011.

11. Governing Law and Jurisdiction
These Terms are governed by the laws of the Republic of India. Any disputes shall be subject to the exclusive jurisdiction of the courts of Pune, Maharashtra.

12. Contact
For any questions or legal concerns, contact us at:
Email: samarthmalusarnsg@gmail.com

By accessing or using the SureCarry Platform, you confirm that you have read, understood, and agree to abide by these legally binding Terms and Conditions."""
    print(TnC)

def main():
    print("1. Add my name.")
    print("2. Fetch people for my need.")
    print("3. Privacy-Policy")
    print("4. Terms and Condition.")
    prio = int(input("\nEnter The operation that you want to carry : "))
    if prio == 1:
        a1 = From()
        a1.from_traveler()
        a1.data_entry()
        print(a1)  
    elif prio == 3:
        privacy()
    elif prio == 4:
        TnC()       
    else:
        a2 = To()
        a2.to_traveler()
        print(a2)  

if __name__ == '__main__':
    main()