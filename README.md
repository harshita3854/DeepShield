# DeepShield - AI-Based Deepfake Image Detection System

## Overview
DeepShield is an AI-powered web application designed to detect whether an uploaded image is real or AI-generated (deepfake). The system uses a trained deep learning model to classify images and display the prediction result with confidence.

---

## Features

- User Registration and Login
- Upload Image for Detection
- Deepfake Image Detection using Deep Learning
- Confidence Score Prediction
- User-Friendly Interface
- Secure Authentication

---

## Technologies Used

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Backend
- Python
- Django

### AI/ML
- TensorFlow
- Keras
- OpenCV
- NumPy

### Database
- SQLite

---

## Project Structure

```
DeepShield/
│── dataset/
│── detector_app/
│── models_store/
│── static/
│── templates/
│── media/
│── manage.py
│── requirements.txt
│── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/harshita3854/DeepShield.git
```

### Navigate to the project folder

```bash
cd DeepShield
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Model

The trained model file is **not included** in this repository because it exceeds GitHub's file size limit.

Place the trained model inside:

```
models_store/
```

Example:

```
models_store/
    deepfake_detector_model.h5
```

---

## Future Enhancements

- Video Deepfake Detection
- Real-Time Webcam Detection
- Explainable AI Visualizations
- Mobile Application
- Cloud Deployment

---

## Author

**Harshita Yadav**

B.Tech Computer Science Engineering (AI & ML)

---

## License

This project is developed for educational and research purposes.
