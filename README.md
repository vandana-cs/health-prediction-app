Use this inside your `README.md` file.

# AI-Powered Health Prediction System

## Project Overview

This project is a simple AI-based health prediction system developed using Python, Flask, SQLite, and Bootstrap. The application allows users to manage patient health records and predict possible health risks based on blood test values such as glucose, haemoglobin, and cholesterol levels.

The main objective of this project is to demonstrate CRUD operations, database integration, form validation, and basic AI-driven prediction logic in a healthcare-related application.

The system generates health-related remarks automatically after analysing the patient’s blood test values.

---

## Features

* Add new patient records
* View all patient details
* Edit existing patient information
* Delete patient records
* Automatic health risk prediction
* Email and date validation
* Responsive and user-friendly interface
* SQLite database integration
* AI-based remarks generation

---

### Workflow
1. Patient blood test data is collected.
2. Data is sent to the Hugging Face AI model.
3. The AI model generates a medical risk summary.
4. If the API is unavailable due to network restrictions, the application uses fallback prediction logic to ensure uninterrupted functionality.

---
## Technologies Used

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* Bootstrap

### Database

* SQLite

### Model Used
- google/flan-t5-base

### Other Libraries

* Jinja2
* Regular Expressions (re module)

## AI/ML API Integration

This project integrates the Hugging Face Inference API for generating AI-based medical remarks.

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Open Project Folder

```bash
cd health-prediction-app
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000
```

---

## Screenshots

### Dashboard Page

![alt text](<Screenshot (24).png>)

### Add Patient Page

![alt text](<Screenshot (25).png>)

### Edit Patient Page

![alt text](<Screenshot (26).png>)

### Prediction Output

![alt text](<Screenshot (24)-1.png>)

---

## AI Prediction Logic

The application predicts possible health risks based on blood test values entered by the user.

### Example Conditions

* High glucose level → Diabetes Risk
* Low haemoglobin level → Anaemia Risk
* High cholesterol level → Heart Disease Risk

The generated prediction is automatically displayed in the Remarks column.

---

## Future Improvements

Some additional features that can be added in future versions include:

* User authentication system
* Machine learning model integration
* Health report export as PDF
* Search and filter functionality
* Cloud database integration
* Dashboard charts and analytics
* Real-time API-based prediction system

---

## Conclusion

This project helped me understand Flask development, CRUD operations, database handling, frontend integration, and basic healthcare prediction logic. It also improved my understanding of form validation, routing, and full-stack web application development.
