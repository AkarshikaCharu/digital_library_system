import streamlit as st
import re
from database_manager import LibraryDB

db = LibraryDB()


def show_auth_page():
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        if 'mode' not in st.session_state: st.session_state.mode = 'login'

        if st.session_state.mode == 'login':
            st.markdown("<h2>Member Login</h2>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("Username")
                u = st.text_input("U", key="l_u", label_visibility="collapsed", placeholder="Username")
                st.markdown("Password")
                p = st.text_input("P", type="password", key="l_p", label_visibility="collapsed", placeholder="Password")

                if st.button("Login", use_container_width=True):
                    res = db.verify_user(u, p)
                    if res:
                        st.session_state.update({"logged_in": True, "user": res[0], "role": res[1], "id": res[2]})
                        st.rerun()
                    else:
                        st.error("Invalid Credentials")

            st.markdown("<p style='text-align:center;'>New here?</p>", unsafe_allow_html=True)
            if st.button("Sign Up", use_container_width=True):
                st.session_state.mode = 'signup';
                st.rerun()

        else:
            st.markdown("<h2>Sign Up</h2>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("Username")
                nu = st.text_input("nu", key="s_u", label_visibility="collapsed")
                st.markdown("Email ID")
                ne = st.text_input("ne", key="s_e", label_visibility="collapsed")
                st.markdown("Password")
                np = st.text_input("np", type="password", key="s_p", label_visibility="collapsed")
                st.markdown("Role")
                # Dropdown text will be white inside black box due to CSS
                role = st.selectbox("r", ["Student", "Faculty"], key="s_r", label_visibility="collapsed")

                ident = "FACULTY-STAFF"
                if role == "Student":
                    st.markdown("Roll Number (UPPERCASE)")
                    ident = st.text_input("ni", key="s_i", label_visibility="collapsed")

                if st.button("Create Account", use_container_width=True):
                    if role == "Student" and not re.match("^[A-Z0-9]+$", ident):
                        st.error("Roll No must be Uppercase Alphanumeric!")
                    elif nu and ne and np:
                        if db.create_user(nu, ne, np, role, ident):
                            st.success("Success! Please Login.");
                            st.session_state.mode = 'login';
                            st.rerun()
                        else:
                            st.error("Username taken!")

            if st.button("Back to Login", use_container_width=True):
                st.session_state.mode = 'login';
                st.rerun()