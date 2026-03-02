import streamlit as st
from datetime import datetime
from smart_hospital_advanced.db_utils import generate_next_ip, save_patient, update_patient
from smart_hospital_advanced.bot.multilingual_bot import multilingual_bot
from smart_hospital_advanced.biobert.biobert_search import check_existing_patient



def show_receptionist_dashboard():

    if "section" not in st.session_state:
        st.session_state.section = "chat"

    render_header()
    render_navbar()

    if st.session_state.section == "chat":
        render_chat()

    elif st.session_state.section == "ip":
        render_ip_registration()

    elif st.session_state.section == "update":
        render_update_discharge()



def render_header():
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        st.image(
            r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\logo.jpg",
            width=70
        )

    with col2:
        st.markdown(
            "<h2 style='text-align:center;'>Susila Multispeciality Hospital</h2>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"<p style='text-align:right; font-weight:bold;'>Hi, {st.session_state.name}</p>",
            unsafe_allow_html=True
        )

    st.divider()



def render_navbar():
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💬 Chat With Me"):
            st.session_state.section = "chat"

    with col2:
        if st.button("📝 IP Registration"):
            st.session_state.section = "ip"

    with col3:
        if st.button("📄 Update / Discharge"):
            st.session_state.section = "update"

    st.divider()



def render_chat():
    st.subheader("💬 Smart Hospital Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**👤 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")

    st.divider()

    user_input = st.text_input("Ask something...")

    if st.button("Send"):
        if user_input.strip():
            st.session_state.chat_history.append(("user", user_input))

            with st.spinner("Thinking..."):
                response = multilingual_bot(user_input)

            st.session_state.chat_history.append(("bot", response))
            st.rerun()

def render_ip_registration():
    st.subheader("📝 IP Registration")

    next_ip = generate_next_ip()
    admission_time = datetime.now()

    st.text_input("IP Number", value=next_ip, disabled=True)
    st.text_input("Admission Date & Time", value=str(admission_time), disabled=True)

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    aadhaar = st.text_input("Aadhaar Number")
    abha = st.text_input("ABHA Number")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")

    department = st.text_input("Department")
    doctor = st.text_input("Doctor Name")

    diagnosis = st.text_area("Diagnosis")
    procedure = st.text_area("Procedure")
    notes = st.text_area("Clinical Notes")

    col1, col2 = st.columns(2)

    # Existing Patient Button (BioBERT logic later integrate)
    with col1:
        if st.button("Existing Patient"):

            input_text = f"""
            Diagnosis: {diagnosis}
            Procedure: {procedure}
            Notes: {notes}
            """

            result = check_existing_patient(input_text)

            if result:
                st.success("Existing Patient Found ✅")
                st.write("IP No:", result["ip_no"])
                st.write("Diagnosis:", result["diagnosis"])
                st.write("Procedure:", result["procedure"])
                st.write("Similarity Score:", result["score"])
            else:
                st.warning("No matching patient found.")

    # Save Button
    with col2:
        if st.button("Save"):
            if not name or not phone:
                st.warning("Please fill required fields")
                return

            data = {
                "name": name,
                "age": age,
                "sex": sex,
                "aadhaar": aadhaar,
                "abha": abha,
                "phone": phone,
                "address": address,
                "department": department,
                "doctor": doctor,
                "diagnosis": diagnosis,
                "procedure": procedure,
                "notes": notes
            }

            ip = save_patient(data)
            st.success(f"Patient Saved Successfully! IP No: {ip}")


def render_update_discharge():
    st.subheader("📄 Update / Discharge")

    ip_no = st.text_input("Enter IP Number")

    diagnosis = st.text_area("Diagnosis")
    procedure = st.text_area("Procedure")
    discharge_date = st.date_input("Discharge Date")
    notes = st.text_area("Doctor Notes")

    if st.button("Update"):
        if not ip_no:
            st.warning("Enter IP Number")
            return

        update_data = {
            "diagnosis": diagnosis,
            "procedure": procedure,
            "notes": notes,
            "discharge_date": discharge_date
        }

        update_patient(ip_no, update_data)
        st.success("Patient Updated Successfully!")
