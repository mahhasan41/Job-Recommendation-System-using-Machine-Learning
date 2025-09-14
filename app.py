
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("monster_com-job_sample.csv")
    df = df.dropna(subset=['job_title', 'job_description'])
    df = df.fillna('')
    # Combine job description, type, and sector as the searchable job profile
    df['combined'] = df['job_description'] + ' ' + df['job_type'] + ' ' + df['sector']
    return df

# Calculate similarity scores between user input and jobs
@st.cache_data
def compute_similarity(df, user_input):
    vectorizer = TfidfVectorizer(stop_words='english')
    job_vecs = vectorizer.fit_transform(df['combined'])
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, job_vecs).flatten()
    return similarity

# Streamlit UI
st.set_page_config(page_title="SkillMatch - Job Recommender", layout="wide")
st.title("💼 SkillMatch: Job Recommendation System")
st.markdown("""
Welcome to **SkillMatch**! Fill in your profile below and let the AI recommend the most relevant jobs for you.
""")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        skills = st.text_input("🔧 Your Skills (comma-separated)", placeholder="e.g., Python, SQL, Excel")
        experience = st.selectbox("📊 Experience Level", ["Fresher", "1-2 years", "3-5 years", "5+ years"])
    with col2:
        location_pref = st.text_input("🌍 Preferred Location", placeholder="e.g., New York, Remote")
        interest_keywords = st.text_input("🎯 Job Interests / Keywords", placeholder="e.g., Data Analyst, Developer")
    submitted = st.form_submit_button("Find Jobs 🚀")

if submitted:
    if not skills.strip():
        st.warning("Please enter at least one skill to proceed.")
    else:
        with st.spinner("Finding the best matches for you..."):
            df = load_data()
            user_input = skills + " " + interest_keywords + " " + experience
            similarity_scores = compute_similarity(df, user_input)
            df['similarity'] = similarity_scores
            filtered = df[df['location'].str.contains(location_pref, case=False, na=False)] if location_pref.strip() else df
            top_matches = filtered.sort_values(by='similarity', ascending=False).head(5)

        if top_matches.empty:
            st.error("No matching jobs found. Try different keywords or broader location.")
        else:
            st.success(f"Top {len(top_matches)} Recommended Jobs for You:")
            for _, row in top_matches.iterrows():
                with st.container():
                    st.markdown(f"### 📌 {row['job_title']}")
                    st.markdown(f"**Location:** {row['location']}  |  **Job Type:** {row['job_type']}")
                    st.markdown(f"**Sector:** {row['sector']}")
                    st.markdown(f"**Job Description:** {row['job_description'][:500]}...")
                    if row['page_url']:
                        st.markdown(f"🔗 [View Job Posting]({row['page_url']})")
                    st.markdown("---")
