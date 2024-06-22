import smtplib
from email.message import EmailMessage
import streamlit as st
import pandas as pd

st.title("Professor Automator")

# Load the dataframe
df = pd.read_csv("Professor Automator - UTD.csv")

st.header("Professors to Email")
st.write(df)

st.subheader("Which Ones Would You Like to Email?")

# Slider to select the range of professors
start = st.slider("First Professor", min_value=0, max_value=len(df)-1, value=0)
end = st.slider("Last Professor", min_value=0, max_value=len(df)-1, value=len(df)-1)
st.write(f"You will email professors from {start} to {end}.")

# Load the email content from a file
msg = EmailMessage()
msg['Subject'] = st.text_input("Subject:")

contents = st.text_area("Message Content:")
msg.set_content(contents)

msg['From'] = st.secrets["email"]["user"]
msg['Cc'] = 'pmunipallep@gmail.com, harneksab@gmail.com'

st.header("Greetings and Customization")
greetings = ["Hello", "Dear", "Welcome", "Other"]
chosenGreeting = st.selectbox("Choose Greeting", greetings)
ending = st.text_input("What would you like to end with {eg. Sincerely, Regards}")
if chosenGreeting == "Other":
    chosenGreeting = st.text_input("Your Greeting:")

sample = st.write(f"{chosenGreeting}, Dr. ___,\n\n{contents}\n\n {ending}, Arjan)")
# Function to send email
def send_email(email_message):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(st.secrets["email"]["user"], st.secrets["email"]["password"])
            smtp.send_message(email_message)
            st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

sampleEmail = st.text_input("Sample Email To Send To:")

if st.button('Send Sample'):
        
    personalized_msg = EmailMessage()
    personalized_msg['From'] = msg['From']
    personalized_msg['To'] = msg['From']
    personalized_msg['Cc'] = msg['Cc']
    personalized_msg['Subject'] = msg['Subject']
        
    personalized_content = f"{chosenGreeting}, Dr. ___,\n\n {contents} \n\n {ending}, Arjan"
    personalized_msg.set_content(personalized_content)
    
    send_email(personalized_msg)

# Send emails to selected professors
if st.button('Send Email'):
    if st.button("ARE YOU SURE?"):
        for index in range(start, end + 1):
            professor = df.loc[index]
            professor_name = f"{professor['Last Name']}"
            professor_email = professor['Email']
            
            personalized_msg = EmailMessage()
            personalized_msg['From'] = msg['From']
            personalized_msg['To'] = professor_email
            personalized_msg['Cc'] = msg['Cc']
            personalized_msg['Subject'] = msg['Subject']
            
            personalized_content = f"{chosenGreeting}, Dr. {professor_name},\n\n{contents}\n\n {ending}, Arjan"
            personalized_msg.set_content(personalized_content)
            
            send_email(personalized_msg)
