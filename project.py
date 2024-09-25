import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Function to load existing data from JSON file (if exists)
def load_data():
    if os.path.exists("Signup_data.json"):
        return pd.read_json("Signup_data.json")
    else:
        # Return an empty DataFrame with the expected columns if file doesn't exist
        return pd.DataFrame(columns=['Username', 'Password', 'Phone', 'DOB'])

# Function to save updated data to JSON file
def save_data(df):
    df.to_json("Signup_data.json", orient='records')

# Load existing data
df = load_data()

# Initialize session state for login status and username if not already
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Sidebar to allow login/signup
log = st.sidebar.selectbox("Choose your option", ("Login", "Signup"))

# Signup functionality
if log == "Signup":
    st.title("Sign Up Page")
    with st.form("Sign_up"):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter a Password", type="password")
        Mob = st.text_input("Enter your phone number")
        dob = st.date_input("When were you born?")
        submitted = st.form_submit_button("Sign Up")
    
    if submitted:
        if username in df['Username'].values:
            st.warning("Username already exists. Try a different one.")
        else:
            # Append new user details to the DataFrame
            new_data = pd.DataFrame({
                'Username': [username],
                'Password': [password],
                'Phone': [Mob],
                'DOB': [dob]
            })
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("Sign up successful!")

# Login functionality
if log == 'Login' and not st.session_state.logged_in:
    st.title("Login Page")
    with st.form("Log in"):
        username_log = st.text_input("Enter your username")
        password_log = st.text_input("Enter your Password", type="password")
        submitted = st.form_submit_button("Log In")
    
    if submitted:
        if username_log in df['Username'].values:
            stored_password = df[df['Username'] == username_log]['Password'].values[0]
            if stored_password == password_log:
                st.success("Login Successful!")
                st.session_state.logged_in = True  # Set login status
                st.session_state.username = username_log  # Store username in session state
            else:
                st.error("Invalid Password")
        else:
            st.error("Username not found. Please sign up first.")

# Dashboard functionality after login
if st.session_state.logged_in:
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    # New page after login
    st.title(f"Welcome to your Dashboard, {st.session_state.username}")
    if not os.path.exists(st.session_state.username):
        os.makedirs(st.session_state.username)

    maths = st.select_slider("Enter your maths marks", options=range(0, 101))
    science = st.select_slider("Enter your science marks", options=range(0, 101))
    english = st.select_slider("Enter your english marks", options=range(0, 101))
    cs = st.select_slider("Enter your computer science marks", options=range(0, 101))
    geography = st.select_slider("Enter your geography marks", options=range(0, 101))
    history = st.select_slider("Enter your history marks", options=range(0, 101))
    electronics = st.select_slider("Enter your electronics marks", options=range(0, 101))
    submitted = st.button("Save Marks")

    if submitted:
        # Create a DataFrame to store the marks
        marks_data = pd.DataFrame({
            'Subject': ['Maths', 'Science', 'English', 'Computer Science', 'Geography', 'History', 'Electronics'],
            'Marks': [maths, science, english, cs, geography, history, electronics]
        })

        # Save the marks data to a JSON file in the user's folder
        marks_file_path = os.path.join(st.session_state.username, "marks.json")
        marks_data.to_json(marks_file_path, orient='records')

        st.success("Marks saved successfully!")
    

    # Plot the marks in different types of charts
    if st.button("Show Charts"):
        # Load the marks data
        marks_file_path = os.path.join(st.session_state.username, "marks.json")
        if os.path.exists(marks_file_path):
            marks_data = pd.read_json(marks_file_path)

            # Pie chart
            st.subheader("Pie Chart of Marks")
            fig_pie = px.pie(marks_data, names='Subject', values='Marks', title='Marks Distribution')
            st.plotly_chart(fig_pie)

            # Bar graph
            st.subheader("Bar Graph of Marks")
            fig_bar = px.bar(marks_data, x='Subject', y='Marks', title='Marks by Subject')
            st.plotly_chart(fig_bar)

            # Line graph
            st.subheader("Line Graph of Marks")
            fig_line = px.line(marks_data, x='Subject', y='Marks', title='Marks Trend')
            st.plotly_chart(fig_line)
        else:
            st.error("No marks data found. Please save your marks first.")
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False  # Reset login status
        st.session_state.username = ""  # Clear username  