import streamlit as st
import os
import re
import requests
from mail_utils import send_resume_to_hr
from dashboards.user_dashboard import show_user_dashboard
from dashboards.receptionist_dashboard import show_receptionist_dashboard
from smart_hospital_advanced.dashboards.doctor_dashboard import show_doctor_dashboard


st.set_page_config(
    page_title="Susila Multispeciality Hospital 🩺",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8000"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None


if st.session_state.logged_in:

    role = str(st.session_state.role).lower()  # case safe

    if role == "patient":
        show_user_dashboard()

    elif role == "receptionist":
        show_receptionist_dashboard()


    elif role == "doctor":

        show_doctor_dashboard()


    elif role in ["admin", "hr", "manager"]:
        st.title("🏢 Admin / HR Dashboard")
        st.success(f"Welcome, {st.session_state.name}")


    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    st.stop()


st.markdown("""
<style>
body { background-color: #ffffff; }

.hospital-name {
    font-size: 30px;
    font-weight: 700;
    color: #0b5394;
    text-align: center;
}

.navbar {
    display: flex;
    justify-content: center;
    gap: 30px;
    background-color: #0b5394;
    padding: 12px;
}

.navbar a {
    color: white;
    font-weight: 600;
    text-decoration: none;
}

.navbar a:hover {
    text-decoration: underline;
}

.section { padding: 30px; }

.footer {
    background-color: #0b5394;
    color: white;
    text-align: center;
    padding: 20px;
    margin-top: 40px;
}
.footer a {
    color: #ffdd57;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)


c1, c2, c3 = st.columns([1,4,1])
with c1:
    st.image(r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\logo.jpg", width=70)
with c2:
    st.markdown("<div class='hospital-name'>Susila Multispeciality Hospital</div>", unsafe_allow_html=True)


st.markdown("""
<div class="navbar">
<a href="?page=home">Home</a>
<a href="?page=services">Scope of Services</a>
<a href="?page=about">About Us</a>
<a href="?page=careers">Careers</a>
<a href="?page=contact">Contact Us</a>
<a href="?page=login">Login</a>
</div>
""", unsafe_allow_html=True)

page = st.query_params.get("page", "home")


if page == "home":
    st.markdown("<div class='section'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,2])
    with col1:
        st.image(r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\hospital.webp", width=320)
    with col2:
        st.markdown("## Care with Compassion")
        st.markdown("### *நம்பிக்கையுடன் சிகிச்சை*")
        st.markdown("Advanced technology • Expert doctors • Affordable care")

    st.markdown("---")
    st.subheader("📸 Hospital Gallery")

    uploads = st.file_uploader(
        "Upload Hospital Photos",
        type=["jpg","png","jpeg"],
        accept_multiple_files=True
    )

    if uploads:
        cols = st.columns(4)
        for i, img in enumerate(uploads):
            cols[i % 4].image(img, use_column_width=True)

    st.markdown("---")
    st.subheader("👨‍⚕️ Our Doctors")

    d1, d2, d3 = st.columns(3)
    d1.image(r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\d1.jpg", width=150)
    d1.caption("Dr. A. Kumar – Cardiology")
    d2.image(r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\d3.jpg", width=150)
    d2.caption("Dr. S. Priya dharshan – Neurology")
    d3.markdown("⭐ 10,000+ Happy Patients\n\n⭐ 25+ Years Experience")

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "services":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## Scope of Services")

    services = [
        "General Medicine","Cardiology","Neurology","Nephrology",
        "Orthopaedics","General Surgery","Paediatrics",
        "Obstetrics & Gynaecology","ICU & Emergency",
        "CT Scan","MRI","X-Ray","Laboratory",
        "Star Health Insurance","CMCHISTN","Govt Schemes"
    ]

    cols = st.columns(3)
    for i, s in enumerate(services):
        cols[i % 3].markdown(f"✔ {s}")

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "about":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## About Us")

    st.image(r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\awards.jpg")
    st.markdown("""
    - High-risk surgeries success  
    - Emergency life-saving care  
    - Trusted by thousands of families  
    """)

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "careers":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## Careers")

    candidate_name = st.text_input("Your Name")
    dept = st.selectbox(
        "Select Department",
        ["Doctors","Nursing","Lab","Pharmacy","Front Office","ICU","Admin"]
    )

    resume = st.file_uploader("Upload Resume", type=["pdf","docx"])

    if st.button("Submit Application"):
        if not candidate_name or not resume:
            st.warning("All fields required")
        else:
            os.makedirs("temp_resumes", exist_ok=True)
            path = os.path.join("temp_resumes", resume.name)
            with open(path, "wb") as f:
                f.write(resume.getbuffer())

            try:
                send_resume_to_hr(candidate_name, dept, path)
                st.success("Resume sent to HR successfully ✅")
            except Exception as e:
                st.error(f"Mail failed ❌ {e}")

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "login":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## Login")

    login_type = st.radio(
        "Login As",
        ["Doctor","User / Patient","Receptionist","Office Staff (HR / Admin)"]
    )

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if login_type == "Doctor":
        reg_no = st.text_input("Doctor Registration Number")
    elif login_type != "User / Patient":
        emp_no = st.text_input("Employee Number")

    if st.button("Login"):
        payload = {"email": email, "password": password}

        try:
            res = requests.post(f"{API_BASE_URL}/login", json=payload)
            if res.status_code != 200:
                st.error(res.json().get("detail"))
                st.stop()

            data = res.json()
            role = data["role"]
            name = data.get("name")
            department = data.get("department")
            # Role validation
            if login_type == "Doctor" and role != "doctor":
                st.error("Not a doctor account")
                st.stop()
            if login_type == "User / Patient" and role != "patient":
                st.error("Not a patient account")
                st.stop()
            if login_type == "Receptionist" and role != "receptionist":
                st.error("Not a receptionist account")
                st.stop()
            if login_type == "Office Staff (HR / Admin)" and role not in ["admin","hr","manager"]:
                st.error("Not office staff")
                st.stop()

            st.success(f"Welcome {data['name']} 👋")

            st.session_state["logged_in"] = True
            st.session_state["role"] = role
            st.session_state["name"] = name
            st.session_state["department"] = department  # ← ADD THIS
            st.session_state["email"] = email
            st.rerun()


        except Exception as e:
            st.error(f"API error ❌ {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### New User Registration (Users Only)")

    name = st.text_input("Full Name")
    reg_email = st.text_input("Email", key="reg")
    pwd = st.text_input("Password", type="password", key="p1")
    cpwd = st.text_input("Confirm Password", type="password", key="p2")

    if st.button("Register"):
        if pwd != cpwd:
            st.error("Passwords mismatch")
        else:
            payload = {"name": name, "email": reg_email, "password": pwd}
            res = requests.post(f"{API_BASE_URL}/register", json=payload)
            if res.status_code == 200:
                st.success("Registered successfully ✅ Please login")
            else:
                st.error(res.json().get("detail"))

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "contact":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("""
    **Susila Multispeciality Hospital**  
    Pudukkottai  

    📞 <a href="tel:9876543210">98765 43210</a>  
    📧 hospital@gmail.com
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("""
<div class="footer">
© 2026 Susila Multispeciality Hospital <br>
📞 <a href="tel:9876543210">98765 43210</a> |
📧 hospital@gmail.com
</div>
""", unsafe_allow_html=True)