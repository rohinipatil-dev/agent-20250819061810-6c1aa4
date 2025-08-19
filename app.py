import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

SYSTEM_PROMPT = (
    "You are ProgJester, an upbeat comedian assistant who specializes in programming humor.\n"
    "- Tell only programming-related jokes (topics like code, bugs, compilers, dev life, infra, AI, etc.).\n"
    "- Keep jokes short, witty, and punchy. Prefer one-liners unless the user asks for a specific format.\n"
    "- Keep it clean and friendly (PG). Avoid profanity, slurs, harassment, or targeted insults.\n"
    "- If the user asks for non-programming content, gently steer back to programming humor.\n"
    "- If asked, optionally add a brief one-line explanation after the joke (prefixed with 'Explanation:')."
)

def get_response(history, model="gpt-4", temperature=0.8, max_tokens=200):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Oops! I ran into an error contacting the model: {e}"

def render_chat(history):
    for msg in history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

def main():
    st.set_page_config(page_title="ProgJester - Programming Joke Bot", page_icon="💻")
    st.title("💻 ProgJester")
    st.caption("A light-hearted bot that tells programming jokes. Keep it nerdy!")

    # Sidebar controls
    with st.sidebar:
        st.subheader("Settings")
        model = st.selectbox("Model", options=["gpt-4", "gpt-3.5-turbo"], index=0)
        temperature = st.slider("Creativity (temperature)", 0.0, 1.5, 0.8, 0.05)
        max_tokens = st.slider("Max tokens (response length)", 50, 512, 200, 10)
        st.markdown("---")
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.experimental_rerun()
        st.markdown("Tip: Try 'one-liner', 'knock-knock', 'haiku', or 'explain the joke'.")

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Starter joke to break the ice
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Why do programmers prefer dark mode? Because light attracts bugs."
        })

    # Render chat history
    render_chat(st.session_state.messages)

    # Chat input
    user_input = st.chat_input("Ask for a programming joke or a style (e.g., 'knock-knock', 'one-liner')...")
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Cooking up some code comedy..."):
                reply = get_response(st.session_state.messages, model=model, temperature=temperature, max_tokens=max_tokens)
                st.write(reply)
        # Append assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()