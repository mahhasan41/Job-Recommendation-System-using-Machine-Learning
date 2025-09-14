# main.py

import streamlit as st
import auth
import resume_parser
import recommender
import visualizer

# DB setup
auth.setup_session()

# Page config
st.set_page_config(page_title="Job Recommender", layout="wide")

# --- AUTH ---
if not st.session_state.logged_in:
    st.title("🔐 Login or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = auth.login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Register")
        name = st.text_input("Full Name")
        reg_username = st.text_input("New Username")
        email = st.text_input("Email")
        reg_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if auth.register_user(name, reg_username, email, reg_password):
                st.success("Account created. Please log in.")
            else:
                st.error("Username already exists or error occurred.")

# --- MAIN DASHBOARD ---
else:
    user = st.session_state.user
    st.sidebar.title("👤 Account")
    st.sidebar.write(f"Welcome, **{user[1]}**!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    #st.image("logo.png", width=180)
    st.title("🎯 SkillMatch- Job Recommender & Resume Screening")
    st.markdown("Upload your resume, add any extra details, and get smart job suggestions!")

    # --- RESUME UPLOAD ---
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    parsed_data = {}
    if uploaded_file:
        parsed_data = resume_parser.parse_resume(uploaded_file)
        st.success("Resume parsed successfully.")
        st.write("**👤 Name:**", parsed_data.get("name", ""))
        st.write("**📧 Email:**", parsed_data.get("email", ""))
        st.write("**📱 Phone:**", parsed_data.get("phone", ""))
        st.write("**🧠 Skills:**", ", ".join(parsed_data.get("skills", [])))

    st.subheader("📝 Complete Your Profile")

    col1, col2 = st.columns(2)
    with col1:
        manual_skills = st.text_input("Skills (comma-separated)", value=", ".join(parsed_data.get("skills", [])))
        experience = st.text_input("Experience Summary", placeholder="e.g., 2 years in Data Analysis")
    with col2:
        location = st.text_input("Preferred Job Location")
        interests = st.text_input("Job Interests", placeholder="e.g., Data Scientist, Web Dev")

    if st.button("🔍 Find Matching Jobs"):
        user_text = experience + " " + interests
        user_skills = [skill.strip().lower() for skill in manual_skills.split(',') if skill.strip()]

        jobs_df = recommender.load_jobs()
        matches_df = recommender.recommend_jobs(user_text, user_skills, jobs_df)

        st.subheader(f"🧭 Top {len(matches_df)} Matching Jobs")
        for _, row in matches_df.iterrows():
            with st.expander(f"📌 {row['job_title']}  ({round(row['similarity'] * 100)}% match)"):
                st.markdown(f"**📍 Location:** {row['location']}")
                st.markdown(f"**📂 Sector:** {row['sector']}")
                st.markdown(f"**🕒 Job Type:** {row['job_type']}")
                st.markdown(f"**📝 Description:** {row['job_description'][:500]}...")

        # --- Visuals ---
        visualizer.show_match_scores(matches_df)

        # --- Missing Skills (Optional: from top 1 job) ---
        top_job_desc = matches_df.iloc[0]['job_description']
        missing_skills = recommender.detect_missing_skills(user_skills, top_job_desc)
        visualizer.show_missing_skills(missing_skills)
