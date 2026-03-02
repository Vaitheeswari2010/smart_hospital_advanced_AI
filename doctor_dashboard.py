import streamlit as st
from smart_hospital_advanced.bot.multilingual_bot import multilingual_bot
from smart_hospital_advanced.utils.sentiment_utils import analyze_sentiment
from smart_hospital_advanced.utils.whatsapp_utils import send_whatsapp
from smart_hospital_advanced.utils.discharge_summary_utils import generate_discharge_summary
from smart_hospital_advanced.utils.risk_prediction_utils import predict_risk
from smart_hospital_advanced.utils.los_prediction_utils import predict_los
from smart_hospital_advanced.utils.vitals_prediction_utils import predict_vitals
from datetime import datetime, timedelta
from smart_hospital_advanced.utils.patient_segmentation_utils import predict_segment
from smart_hospital_advanced.utils.association_utils import check_patient_patterns
from smart_hospital_advanced.utils.kidney_predictor import predict_kidney
from smart_hospital_advanced.utils.brain_predictor import predict_brain
def show_doctor_dashboard():

    if "section" not in st.session_state:
        st.session_state.section = "home"

    render_header()
    render_navbar()

    if st.session_state.section == "home":
        render_home()

    elif st.session_state.section == "feedback":
        render_feedback()

    elif st.session_state.section == "chat":
        render_chat()

    elif st.session_state.section == "discharge":
        render_discharge()

    elif st.session_state.section == "predictions":
        render_predictions()

    elif st.session_state.section == "image_analysis":
        render_image_analysis()


def render_header():

    doctor_name = st.session_state.get("name", "Doctor")
    department = st.session_state.get("department", "Department")
    email = st.session_state.get("email", "")

    st.title("👨‍⚕ Doctor Dashboard")

    st.success(f"Welcome, {doctor_name}")
    st.write(f"📧 {email}")
    st.write(f"🏥 Department: {department}")

    st.divider()



def render_navbar():

    col1, col2, col3, col4, col5 , col6 = st.columns(6)

    with col1:
        if st.button("🏠 Home"):
            st.session_state.section = "home"

    with col2:
        if st.button("📢 Feedback"):
            st.session_state.section = "feedback"

    with col3:
        if st.button("💬 Chat With Me"):
            st.session_state.section = "chat"

    with col4:
        if st.button("📄 Discharge Summary"):
            st.session_state.section = "discharge"

    with col5:
        if st.button("📊 Predictions"):
            st.session_state.section = "predictions"
    with col6:
        if st.button("🧠 Image Analysis"):
            st.session_state.section = "image_analysis"
    st.divider()



def render_home():

    department = st.session_state.get("department", "Department")

    images = {
        "Cardiology": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\cardilogy.jpg",
        "Neurology": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\neurology.webp",
        "Nephrology": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\nephrology.jpg",
        "urology": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\uro;ogy.jpg",
        "Orthopaedics": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\orthopedictics.jpgdit",
        "Paediatrics": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\orthopedictics.jpg",
        "gynecology": r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\gyneco;ogy.webp",
    }

    image_path = images.get(department, r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\frontend\images\hospital_image.jpg")

    st.image(image_path, width=500)



def render_feedback():
    st.subheader("📢 Feedback")


    department = st.selectbox(
        "Select Department",
        [
            "Cardiology",
            "Neurology",
            "Nephrology",
            "ICU",
            "General Surgery",
            "Orthopaedics",
            "Gynaecology",
            "Paediatrics",
            "Laboratory",
            "Radiology",
            "Pulmonology",
            "Urology",
            "Endocrinology"
        ]
    )

    feedback_text = st.text_area("Enter feedback")

    if st.button("Submit Feedback"):
        if feedback_text.strip() == "":
            st.warning("Please enter feedback")
        else:
            # Combine department + feedback
            full_message = f"""
    🚨 Department: {department}
    👨‍⚕ Doctor: {st.session_state.name}
    📩 Feedback:
    {feedback_text}
    """

            label, score = analyze_sentiment(feedback_text)

            # Send WhatsApp only if negative
            if label == "NEGATIVE":
                send_whatsapp(full_message)

            st.success("Feedback processed successfully")



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



def render_discharge():
    st.subheader("📄 Discharge Summary")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    sex = st.selectbox("Sex", ["Male", "Female"])
    hospital_no = st.text_input("Hospital Number")
    ip_no = st.text_input("IP Number")

    admission_date = st.date_input("Admission Date")
    discharge_date = st.date_input("Discharge Date")
    followup = st.date_input("Follow-up Date")
    surgery_date = st.date_input("Surgery Date")
    diagnosis = st.text_area("Diagnosis")
    medical_condition = st.text_area("Medical Condition")
    treatment = st.text_area("Treatment Given")
    condition = st.text_area("Condition at Discharge")
    advice = st.text_area("Advice on Discharge")
    follow_up = st.text_input("Follow Up Date")

    if st.button("Create Discharge Summary"):
        data = {
            "name": name,
            "ip_no": ip_no,
            "age": age,
            "sex": sex,
            "admission_date": str(admission_date),
            "surgery_date": str(surgery_date),
            "discharge_date": str(discharge_date),
            "diagnosis": diagnosis,
            "treatment": treatment,
            "condition": condition,
            "advice": advice,
            "followup": str(followup)
        }

        pdf_file = generate_discharge_summary(data)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "Download Discharge Summary",
                f,
                file_name="Discharge_Summary.pdf"
            )


def render_predictions():

    st.subheader("📊 Prediction Modules")

    option = st.selectbox(
        "Select Prediction Type",
        [
            "Lab Vitals Prediction",
            "Risk Level Prediction",
            "Length of Stay Prediction",
            "Patient Segmentation",
            "Association Prediction"
        ]
    )


    if option == "Risk Level Prediction":

        st.markdown("### 🩺 Enter Patient Details")

        age = st.number_input("Age", 0, 120)
        oxygen = st.number_input("Oxygen Saturation (SpO2)")
        sys_bp = st.number_input("Systolic BP")
        dia_bp = st.number_input("Diastolic BP")
        resp = st.number_input("Respiratory Rate")
        sugar = st.number_input("Fasting Blood Sugar")
        creat = st.number_input("Serum Creatinine")
        bmi = st.number_input("BMI")

        disease_stage = st.selectbox("Disease Stage", [0,1,2,3])
        acute = st.selectbox("Acute (0) / Chronic (1)", [0,1])

        if st.button("Predict Risk"):

            input_data = [
                age,
                oxygen,
                sys_bp,
                dia_bp,
                resp,
                sugar,
                creat,
                bmi,
                disease_stage,
                acute
            ]

            label, prob = predict_risk(input_data)

            if label == "High Risk":
                st.error(f"🚨 {label}")
            else:
                st.success(f"✅ {label}")

            st.info(f"Confidence: {prob}%")
    elif option == "Length of Stay Prediction":

        st.markdown("### 🏥 Enter LOS Details")

        age = st.number_input("Age", 0, 120)
        acute = st.selectbox("Condition Type", ["Acute", "Chronic"])
        disease = st.selectbox("Disease Name", ["Other", "Diabetes Mellitus"])
        hba1c = st.number_input("HbA1c")
        dialysis = st.selectbox("Dialysis Required", [0, 1])
        icu = st.selectbox("ICU Required", [0, 1])
        risk_score = st.number_input("Risk Score")
        creat = st.number_input("Serum Creatinine")

        if st.button("Predict LOS"):
            # Convert categorical to training format
            acute_chronic = 1 if acute == "Chronic" else 0
            diabetes_flag = 1 if disease == "Diabetes Mellitus" else 0

            input_data = [
                acute_chronic,
                diabetes_flag,
                hba1c,
                dialysis,
                icu,
                risk_score,
                creat,
                age
            ]



            label, days = predict_los(input_data)

            st.success(f"Predicted Length of Stay: {days} days")
            st.info(f"Category: {label}")



    elif option == "Lab Vitals Prediction":

            st.markdown("### 📈 Enter Last 4 Vitals Readings")

            current_time = datetime.now()

            vitals = []

            # Generate last 4 time slots (10 min gap)
            time_slots = [
                current_time - timedelta(minutes=40),
                current_time - timedelta(minutes=30),
                current_time - timedelta(minutes=20),
                current_time - timedelta(minutes=10),
            ]

            for i, time_slot in enumerate(time_slots):
                formatted_time = time_slot.strftime("%H:%M")

                st.markdown(f"#### Reading at {formatted_time}")

                bp = st.number_input(f"BP at {formatted_time}", key=f"bp{i}")
                hr = st.number_input(f"Heart Rate at {formatted_time}", key=f"hr{i}")
                spo2 = st.number_input(f"SpO2 at {formatted_time}", key=f"spo2{i}")
                temp = st.number_input(f"Temperature at {formatted_time}", key=f"temp{i}")

                vitals.append([bp, hr, spo2, temp])

            if st.button("Predict Next Vitals"):


                bp, hr, spo2, temp = predict_vitals(vitals)

                next_time = current_time.strftime("%H:%M")

                st.success(f"🧠 Predicted Vitals for {next_time}")

                st.write(f"BP: {bp}")
                st.write(f"Heart Rate: {hr}")
                st.write(f"SpO2: {spo2}")
                st.write(f"Temperature: {temp}")
    elif option == "Patient Segmentation":

        st.markdown("### 🧬 Enter Patient Metrics")

        age = st.number_input("Age", 0, 120)
        height_cm = st.number_input("Height (cm)")
        systolic_bp = st.number_input("Systolic BP")
        diastolic_bp = st.number_input("Diastolic BP")
        heart_rate = st.number_input("Heart Rate")
        respiratory_rate = st.number_input("Respiratory Rate")
        body_temperature = st.number_input("Body Temperature")
        oxygen_saturation = st.number_input("Oxygen Saturation")
        fasting_blood_sugar = st.number_input("Fasting Blood Sugar")
        hba1c = st.number_input("HbA1c")
        serum_creatinine = st.number_input("Serum Creatinine")
        hemoglobin = st.number_input("Hemoglobin")
        cholesterol_total = st.number_input("Total Cholesterol")

        if st.button("Segment Patient"):

            input_data = [
                age,
                height_cm,
                systolic_bp,
                diastolic_bp,
                heart_rate,
                respiratory_rate,
                body_temperature,
                oxygen_saturation,
                fasting_blood_sugar,
                hba1c,
                serum_creatinine,
                hemoglobin,
                cholesterol_total
            ]

            segment = predict_segment(input_data)

            if segment == "High Risk Critical":
                st.error(f"🔴 {segment}")
            elif segment == "Moderate Chronic":
                st.warning(f"🟡 {segment}")
            else:
                st.success(f"🟢 {segment}")
    elif option == "Association Prediction":

          from smart_hospital_advanced.utils.association_utils import check_patient_patterns

          st.markdown("### 🧠 Clinical Similarity Analyzer")
          systolic_bp = st.number_input("Systolic BP")
          fasting_blood_sugar = st.number_input("Fasting Blood Sugar")
          hba1c = st.number_input("HbA1c")
          serum_creatinine = st.number_input("Serum Creatinine")
          oxygen_saturation = st.number_input("Oxygen Saturation")
          cholesterol_total = st.number_input("Total Cholesterol")
          hemoglobin = st.number_input("Hemoglobin")
          heart_rate = st.number_input("Heart Rate")
          respiratory_rate = st.number_input("Respiratory Rate")

          if st.button("Analyze Clinical Similarity"):

                    patient_input = {
                        "systolic_bp": systolic_bp,
                        "fasting_blood_sugar": fasting_blood_sugar,
                        "hba1c": hba1c,
                        "serum_creatinine": serum_creatinine,
                        "oxygen_saturation": oxygen_saturation,
                        "cholesterol_total": cholesterol_total,
                        "hemoglobin": hemoglobin,
                        "heart_rate": heart_rate,
                        "respiratory_rate": respiratory_rate
                    }

                    results = check_patient_patterns(patient_input)

                    if results:

                        st.markdown("### 🔍 Similar Historical Case Insights")

                        for r in results:
                            st.warning(
                                f"""
                🧠 This patient profile is statistically similar to historical cases associated with:

                ➡️ {', '.join(r['disease'])}

                Observed Risk Indicators:
                • {', '.join(r['conditions'])}

                📊 Statistical Evidence:
                • Confidence: {r['confidence']}%
                • Lift: {r['lift']}
                • Support: {r['support']}%

                ⚠️ This is NOT a confirmed diagnosis.
                Clinical evaluation by the treating physician is required.
                                    """
                            )

                    else:
                        st.success("No strong association patterns detected for this patient profile.")





def render_image_analysis():
    st.subheader("🧠 Medical Image Analysis")

    scan_type = st.selectbox(
        "Select Scan Type",
        ["Kidney", "Brain"]
    )

    uploaded_file = st.file_uploader(
        "Upload Medical Scan Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:


        st.image(uploaded_file, width=300)

        if st.button("Analyze Image"):

            if scan_type == "Kidney":
                result, confidence = predict_kidney(uploaded_file)

            elif scan_type == "Brain":

                result, confidence = predict_brain(uploaded_file)

            st.success(f"🩺 Result: {result}")
            st.info(f"Confidence: {confidence}%")
