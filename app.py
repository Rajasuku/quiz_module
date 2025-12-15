import streamlit as st
import json
import csv
import os

st.set_page_config(page_title="ML Quiz", page_icon="🧠")

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)["questions"]

# Initialize session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False

st.title("🧠 Machine Learning Quiz")

# ------------------ STUDENT DETAILS ------------------
if not st.session_state.quiz_started:
    st.subheader("👤 Student Details")

    name = st.text_input("Student Name")
    email = st.text_input("Email ID")

    if st.button("Start Quiz"):
        if name.strip() == "" or email.strip() == "":
            st.warning("⚠️ Please enter both Name and Email ID")
        else:
            st.session_state.student_name = name
            st.session_state.email = email
            st.session_state.quiz_started = True
            st.rerun()

# ------------------ QUIZ QUESTIONS ------------------
elif st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]

    st.subheader(f"Question {st.session_state.current_q + 1} of {len(questions)}")
    st.write(q["question"])

    selected_option = st.radio(
        "Choose your answer:",
        q["options"],
        key=f"q_{st.session_state.current_q}"
    )

    if st.button("Next ➡️"):
        if selected_option == q["answer"]:
            st.session_state.score += 1

        st.session_state.current_q += 1
        st.rerun()

# ------------------ SUBMIT QUIZ ------------------
else:
    st.success("✅ Quiz Submitted Successfully!")

    st.write("Thank you for completing the quiz.")
    st.write("Your responses have been recorded.")

    if st.button("Submit"):
        file_exists = os.path.isfile("quiz_results.csv")

        with open("quiz_results.csv", "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["Student Name", "Email ID", "Score"])

            writer.writerow([
                st.session_state.student_name,
                st.session_state.email,
                st.session_state.score
            ])

        st.balloons()
        st.success("📁 Your submission has been saved!")
