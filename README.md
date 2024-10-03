# Gym Exercise Detector using Mediapipe and Streamlit

This project is a gym exercise detector that utilizes your webcam to track and analyze workout movements. It calculates the angles between body joints using mathematical formulas to count repetitions and provide feedback. If a movement is incomplete, it won't count the repetition. The project also includes a calorie calculator and an articles page.

## Features
- **Exercise Detection**: Detects gym exercises using Mediapipe by analyzing your body's movements via webcam.
- **Rep Counting**: Uses angle measurements between joints to accurately count completed reps.
- **Feedback Mechanism**: If an exercise is not performed correctly, it will notify the user and won't count the rep.
- **Calorie Calculator**: Allows users to calculate calories burned based on their workout.
- **Articles Page**: Provides useful articles related to fitness and health.

## Technologies Used
- **Mediapipe**: For real-time human pose estimation.
- **Streamlit**: To build and host the web application.
- **Python**: Core language for logic and calculations.

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gym-exercise-detector.git



Install the required dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py


Usage
Open the app in your browser.
Navigate to the "Exercise Detector" page to start tracking your workout via webcam.
Perform exercises in front of the webcam, and the system will automatically count your reps and give feedback if a movement is incomplete.
Explore the "Calorie Calculator" page to estimate your burned calories.

