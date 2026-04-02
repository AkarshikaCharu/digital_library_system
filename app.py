import streamlit as st
from database_manager import LibraryDB
from login import show_auth_page

db = LibraryDB()
# Updated tab title
st.set_page_config(page_title="Digital Library", layout="wide")

# FINAL MASTER CSS
st.markdown("""
    <style>
    /* 1. Background Lavender */
    .stApp { background-color: #E6E6FA !important; }

    /* 2. Black Input Boxes & Select Boxes */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox {
        background-color: #000000 !important;
        border-radius: 8px !important;
        border: 1px solid #7B61FF !important;
    }

    /* 3. White Text for Input & Selection */
    input, .stSelectbox div {
        color: white !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* Ensures the current selected value in dropdown is white */
    div[data-baseweb="select"] > div {
        color: white !important;
    }

    /* 4. Bold Black Labels (14px) */
    span, p, div, label, li {
        color: black !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 5. Headers Violet */
    h1, h2, h3, h4 { color: #7B61FF !important; font-weight: bold !important; }

    /* 6. Buttons Violet with White Bold Text */
    .stButton>button {
        background-color: #7B61FF !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    /* 7. Book Cards White */
    .book-card {
        background-color: white; padding: 20px; border-radius: 12px;
        border-left: 8px solid #7B61FF; box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_auth_page()
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.user}\n**Role:** {st.session_state.role}")
    if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()

    st.title(f"📚 Digital Library Portal")
    books = db.fetch_books()

    if st.session_state.role == "Faculty":
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Books", len(books))
        c2.metric("Issued", len([b for b in books if b[4] == 'Borrowed']))
        c3.metric("Available", len([b for b in books if b[4] == 'Available']))
        with st.expander("Add New Book to Inventory"):
            i, t, a = st.text_input("ISBN"), st.text_input("Title"), st.text_input("Author")
            if st.button("Save to Database"): db.add_book(i, t, a); st.rerun()

    st.divider()
    q = st.text_input("🔍 Search Library Catalog...", placeholder="Type title, author, or ISBN").lower()
    f_books = [b for b in books if q in b[2].lower() or q in b[3].lower() or q in b[1].lower()]

    cols = st.columns(3)
    for idx, b in enumerate(f_books):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="book-card"><span style="color:#7B61FF;">{b[1]}</span><h4>{b[2]}</h4><p>Author: {b[3]}</p><p>Status: {b[4]}</p></div>',
                unsafe_allow_html=True)
            if b[4] == "Available":
                if st.button("Borrow", key=f"b{b[0]}", use_container_width=True):
                    db.update_book_status(b[0], "Borrowed");
                    st.rerun()
            else:
                if st.button("Return", key=f"r{b[0]}", use_container_width=True):
                    db.update_book_status(b[0], "Available");
                    st.rerun()