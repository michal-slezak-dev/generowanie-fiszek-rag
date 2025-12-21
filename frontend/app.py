import streamlit as st

def next_card():
    if st.session_state.current_card_index < len(st.session_state.cards) - 1:
        st.session_state.current_card_index += 1
        st.session_state.is_flipped = False

def prev_card():
    if st.session_state.current_card_index > 0:
        st.session_state.current_card_index -= 1
        st.session_state.is_flipped = False

def flip_card():
    st.session_state.is_flipped = not st.session_state.is_flipped

st.set_page_config(page_title="WikiCard AI - RAG-Powered Flashcard Generation", page_icon="🧠")

# Initialize Session State
if "cards" not in st.session_state:
    st.session_state.cards = []
if "current_card_index" not in st.session_state:
    st.session_state.current_card_index = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "selected_deck_name" not in st.session_state:
    st.session_state.selected_deck_name = ""

test_flashcards1 = [
    {
        "question": "Question 1",
        "answer": "Answer 1"
    },
    {
        "question": "Question 2",
        "answer": "Answer 2"
    }
]

test_flashcards2 = [
    {
        "question": "Question 2-1",
        "answer": "Answer 2-1"
    },
    {
        "question": "Question 2-2",
        "answer": "Answer 2-2"
    },
    {
        "question": "Question 3-3",
        "answer": "Answer 3-3"
    }
]

# Sidebar with test flashcard decks (later loaded from our db)
with st.sidebar:
    st.title("📚 Your Saved Decks")
    st.write("Click a deck to study")

    col1, col2 = st.columns([4, 2])
    with col1:
        if st.button("📁 Test Deck 1", use_container_width=True, key="deck_1"):
            st.session_state.cards = test_flashcards1
            st.session_state.current_card_index = 0
            st.session_state.is_flipped = False
            st.session_state.selected_deck_name = "Test Deck 1"
        
    with col2:
        if st.button("", icon="🗑️", use_container_width=True, help="Delete Deck", key="del_1"):
            st.warning("Deleting deck...")

    col3, col4 = st.columns([4, 2])
    with col3:
        if st.button("📁 Test Deck 2", use_container_width=True, key="deck_2"):
            st.session_state.cards = test_flashcards2
            st.session_state.current_card_index = 0
            st.session_state.is_flipped = False
            st.session_state.selected_deck_name = "Test Deck 2"
        
    with col4:
        if st.button("", icon="🗑️", use_container_width=True, help="Delete Deck", key="del_2"):
            st.warning("Deleting deck...")