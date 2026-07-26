# Crime Alert System

## Overview

The Crime Alert System is an AI-powered web application designed to analyze crime data, identify crime hotspots, and provide timely alerts through an interactive dashboard. The system enables users to visualize crime trends, monitor high-risk areas, and support data-driven decision-making for public safety.

---

## Features

- Interactive dashboard for crime statistics
- Crime hotspot visualization
- AI/ML-based crime prediction
- Crime alert generation
- Search and filter crime records
- Data analytics and visualization
- REST API backend
- SQL database integration

---

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- SQLAlchemy

### Database
- SQLite

### Machine Learning
- Scikit-learn
- Pandas
- NumPy

### Data Visualization
- Chart.js
- Interactive Maps

### Deployment
- Zoho Catalyst (Planned)

---

## Project Structure

```text
crime-alert-system/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── ml/
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── datasets/
│
├── README.md
└── .gitignore
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/<username>/crime-alert-system.git
cd crime-alert-system
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate the environment.

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Run the application

```bash
cd backend
python app.py
```

The application will be available at the configured local host.

---

## Dataset

The project uses the Karnataka Crime Dataset for analysis and prediction. The dataset undergoes preprocessing before being used for visualization and machine learning.

---

## System Workflow

1. Collect crime data.
2. Preprocess and clean the dataset.
3. Analyze data using machine learning models.
4. Store processed information in the database.
5. Display crime statistics and hotspots through the dashboard.
6. Generate alerts for high-risk areas.

---

## Future Enhancements

- Real-time crime data integration
- Push notifications
- Mobile application
- Route safety recommendations
- Anonymous crime reporting
- Role-based authentication
- Enhanced AI prediction models

---

## Team

Developed as part of the Karnataka State Police Datathon.

Team Members:
- Ryan
- Nirupama
- Mrinal
- Goury
- Nandana

---

## License

This project is developed for academic and prototype purposes.
