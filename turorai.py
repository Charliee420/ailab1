import streamlit as st
import google.generativeai as genai

genai.configure(api_key='AIzaSyBMl0IeB6js1nuAFE3Dtjzn1eFN__LCfTs')
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI in Education Tutor", layout="centered")
st.title("🎓 AI in Education: Virtual Tutor")
st.header("📘 Personalized Learning Suggestion")

score = st.slider("Enter your last test score (0-100):", 0, 100, 0)
topics = [(30, "Basics of Python"), (40, "If Else Statement"), (50, "Functions and Loops"),
          (60, "List, Tuples, Dist"), (70, "Make some projects and practice it Well"), (100, "Object-Oriented Programming")]
for t, msg in topics:
    if score <= t:
        st.success(f"Recommended Topic: {msg}")
        break

st.header("💡 Ask the AI Tutor a Question")
q = st.text_input("Type your question (e.g., What is Python?)")
if q:
    r = model.generate_content(f"give me answer in 5 line for this question {q}")
    st.markdown(f"**Tutor Answer:** {r.text}")

st.header("🧠 Self-Grading (Answers fetched from Wikipedia)")
questions = ["What is Python?", "What is artificial intelligence?", "What is a function in programming?"]

if st.checkbox("Attempt quiz with AI-checked answers"):
    st.markdown("### Answer the questions:")
    answers = [st.text_input(f"{i+1}. {q}", key=f"q{i}") for i, q in enumerate(questions)]

    if st.button("Submit Answers"):
        st.markdown("---\n### 📖 Correct Answers & Grading:")
        total = 0
        for i, q in enumerate(questions):
            try:
                p = f"""You're an AI teacher. Provide a 1-line correct answer and grade the student.
Question: {q}
Student's Answer: {answers[i]}
Respond in this format:
Correct Answer: <answer>
Score: <1 / 0.5 / 0>
Explanation: <optional>"""
                res = model.generate_content(p).text.strip().splitlines()
                a = res[0].replace("Correct Answer: ", "").strip()
                s = float(res[1].replace("Score: ", "").strip())
                e = res[2].replace("Explanation: ", "").strip() if len(res) > 2 else ""
                total += s
                st.markdown(f"**Q{i+1}: {q}**")
                st.write(f"Your Answer: `{answers[i]}`")
                st.write(f"Correct Answer: `{a}`")
                if s == 1: st.success("✅ Fully Correct (1 mark)")
                elif s == 0.5: st.info(f"🟡 Partially Correct (0.5 mark) — {e}")
                else: st.error(f"❌ Incorrect (0 mark) — {e}")
                st.markdown("---")
            except Exception as e:
                st.error(f"Error: {e}")
        pct = (total / len(questions)) * 100
        st.subheader(f"Final Score: {total}/{len(questions)} ({pct:.2f}%)")
        if pct < 50: st.warning("You might want to review the material.")
        elif pct < 75: st.info("Good job! A bit more practice will help.")
        else: st.success("Excellent work! Keep it up!")
