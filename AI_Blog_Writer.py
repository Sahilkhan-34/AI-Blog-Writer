import streamlit as st
import pandas as pd
import google.generativeai as genai


# Define user data
users = [
    {"name": "Pratik Jadhav", "email": "pratik@gmail.com", "number": "1234567890", "password": "password123", "dob": "2002-02-01"},
    {"name": "Sahil Khan", "email": "sahil@gmail.com", "number": "0987654321", "password": "password456", "dob": "2000-02-02"},
    {"name": "testuser", "email": "testuser@mail.com", "number": "0987654321", "password": "testpass", "dob": "2000-02-03"}
]

# Create DataFrame and save to CSV
user_data = pd.DataFrame(users)
user_data.to_csv('user_data_no.csv', index=False)

# Load user data from CSV file
user_data = pd.read_csv("user_data_no.csv")

# Function to display the login form
def show_login_form():
    st.title("AI Blog Writer")
    st.subheader("Login")
    st.write("Use default login Email : 'testuser@mail.com' & Password : 'testpass' ")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email not in user_data["email"].values:
            st.error("Email not found!")
        else:
            user_index = user_data.index[user_data["email"] == email].tolist()[0]
            stored_password = user_data["password"].iloc[user_index]
            if stored_password == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user_data["name"].iloc[user_index]
                st.success("Login successful!")
                st.experimental_rerun()  # Redirect to the next page
            else:
                st.error("Incorrect password!")

# Function to display the AI Blog Generator page
def show_next_page():
    st.write(f"Hello, you are welcome {st.session_state['username']}!")
    st.title("AI Blog Writer")
    st.subheader('Unleash the power of Generative AI to seamlessly generate amazing blogs.')
    apikey = st.text_input("Enter Google Gemini API Key Here", type='password')
    if st.button("Submit") and apikey is not None:
   
        genai.configure(api_key=apikey)

        topic = st.text_input("Enter the main topic of your Blog")
        headline =  st.text_input("Enter the title of your Blog")
        description = st.text_area("Give the descriptive idea of what should be in your blog")
        words = st.text_input("Enter the number of words limit of your Blog")

        prompt = f"""
        write a blog on the given {topic}, The title of my blog should be {headline}, use the {description} as a context 
        in the blog and the length of my blog should be {words} , generate the blog
        """

        if st.button("Generate Blog"):
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content([prompt])
            st.write(response.text)
    else:
        st.error("Enter Correct API Key")

# Main app flow
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

if not st.session_state["logged_in"]:
    show_login_form()
else:
    show_next_page()
