from message_ai import get_ai_response
user_question = st.text_input("Ask your medicine/symptom question:")

if st.button("Ask AI"):
    answer = get_ai_response(user_question)

    st.write(answer)
