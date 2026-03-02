# 🏥 Smart Hospital AI Platform

## 📌 Project Overview
Smart Hospital AI Platform is an intelligent hospital management and medical decision-support system built using Artificial Intelligence, Machine Learning, and NLP.  

The system provides multiple dashboards for users, doctors, receptionists, and HR/admin staff. It integrates chatbots, medical prediction models, automated discharge summaries, and image-based disease detection.

The goal of this system is to improve hospital workflow, assist doctors with AI insights, and enhance patient experience.

---

# 🚀 Key Features

## 🖥 Hospital Website UI
The system starts with a hospital website interface that includes:

### Top Navigation Bar
- Hospital Name
- Hospital Logo

### Second Navigation Bar
- Home
- Scope of Services
- About Us
- Careers
- Contact Us
- Login

---

## 🏠 Home Page
The home page displays:

- Experienced doctor images
- Hospital infrastructure images
- Hospital slogans
- Hospital introduction

---

## 🏥 Scope of Services
Displays all hospital medical services such as:

- General Medicine
- Surgery
- Cardiology
- Neurology
- Orthopedics
- Emergency Care
- ICU Services

---

## ℹ About Us
Shows hospital achievements including:

- Awards
- Certifications
- Hospital achievements
- Institutional milestones

---

## 💼 Careers Page
A job application form for hiring hospital staff.

Features:
- Applicant uploads resume
- Resume is automatically sent to HR email
- Used for staff recruitment

---

# 🔐 Login System

Four types of login access:

1. User
2. Receptionist
3. Doctor
4. HR / Admin

New users can register before login.

---

# 👤 User Dashboard

User dashboard includes:

### AI Medical Chatbot
- Languages supported:
  - English
  - Hindi
  - Malayalam
- Built using **RAG (Retrieval Augmented Generation)**

### Review & Feedback System
- Users can submit feedback
- Sentiment Analysis model analyzes positive/negative feedback

---

# 🧾 Receptionist Dashboard

Receptionist panel manages hospital patient records.

Features include:

### IP Registration
- Register inpatients
- Store patient details in database

### Patient Update & Discharge
- Update patient treatment details
- Enter doctor notes
- Discharge patient records

### Doctor Notes Retrieval
Old doctor notes can be searched using **BioBERT NLP model**.

### Receptionist Chatbot
Multilingual chatbot support.

---

# 🩺 Doctor Dashboard

Doctor panel contains an advanced AI-assisted system.

### Navigation Menu
- Home
- Feedback
- Chatbot
- Automated Discharge Summary
- ML Prediction
- Image Prediction

---

## 🏠 Doctor Home Page
Displays department-related images and information.

---

## 📢 Staff Feedback Monitoring
If a staff member enters negative feedback:

- The system detects it
- Sends automatic alert message through **WhatsApp notification**

---

## 🤖 Doctor Chatbot
Multilingual chatbot for medical assistance:

- English
- Hindi
- Malayalam

---

## 📄 Automated Discharge Summary
Automatically generates patient discharge summary.

Features:
- Generate PDF discharge summary
- Downloadable document

---

# 📊 Machine Learning Predictions

The system includes several ML models:

### Length of Stay Prediction
Predicts how long a patient will stay in hospital.

### Risk Level Prediction
Predicts patient risk level based on medical parameters.

### Patient Segmentation
Groups patients into categories for better treatment planning.

### Patient Association Analysis
Finds relationships between diseases and treatments.

### Lab Vital Prediction (LSTM Model)
If nurse enters first 4 vitals, the system predicts upcoming lab vitals using an **LSTM deep learning model**.

---

# 🧠 Image-Based Disease Prediction

The system supports medical image analysis.

### Kidney Stone Detection
Detects kidney stones using medical images.

### Brain Tumor Detection
Detects brain tumors using CNN deep learning model.

---

# ⚙ Tech Stack

### Backend
- FastAPI

### Frontend
- Streamlit

### AI / ML
- TensorFlow
- Keras
- Scikit-learn
- BioBERT
- LSTM

### NLP
- RAG Chatbot
- Sentiment Analysis

### Image Processing

- CNN Models

### Database
- SQL Database

### APIs
- FastAPI REST APIs

---


