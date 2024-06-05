import av
import streamlit as st
import numpy as np
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp
import warnings
import json
from streamlit_lottie import st_lottie



st.set_page_config(page_title="Antrenman-module ", page_icon="🏋️‍", layout="wide")
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

# animasyon
def load_lottiefile(filepath: str):

    with open(filepath, "r") as f:
        return json.load(f)


curl_vid = "https://youtu.be/qVjrqN7cNJc?si=Hj_2cJv3kxe7Z8TV"
pushdown_vid = "https://www.youtube.com/watch?v=6Fzep104f0s&ab_channel=RenaissancePeriodization"
squat_vid = "https://youtu.be/RUfKDy9TjlU?si=1RGeCpdi3lhzvMR5"
situp_vid = "https://www.youtube.com/watch?v=UMaZGY6CbC4&ab_channel=FitnessForTransformation"
lateral_vid = "https://www.youtube.com/watch?v=YSv89mmI26Y&ab_channel=Ph%E1%BA%A1mD%C6%B0%C6%A1ng"
legpress_vid = "https://youtu.be/4PYXEYqgCqk?si=hZ5AbetEmZJU-4Ao"

pose_anim = load_lottiefile("animations/poseanimation.json")

counter = 0
state = None
feedback = ''
range_flag = False
halfway = False
left_angle = []
right_angle = []
body_angles = []
frames = []

# MediaPipe Pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils





# noktalar arasinda açıyı hesaplayan fonksiyon
def calc_angle(x, y, z):

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    radians = np.arctan2(z[1] - y[1], z[0] - y[0]) - np.arctan2(x[1] - y[1], x[0] - y[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle


# egzersiz functions

# 1.egzersiz
def recognise_curl(detection):
    global counter, state, feedback, range_flag, left_angle, right_angle

    try:
        landmarks = detection.pose_landmarks.landmark

        # Left arm
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        # Right arm
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

        left_elbow_angle = calc_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = calc_angle(right_shoulder, right_elbow, right_wrist)
        left_angle.append(int(left_elbow_angle))
        right_angle.append(int(right_elbow_angle))

        # Curl logic
        if left_elbow_angle > 160 and right_elbow_angle > 160:
            if not range_flag:
                feedback = 'Did not curl completely.'
            else:
                feedback = 'Good rep!'
            state = 'Down'

        elif (left_elbow_angle > 50 and right_elbow_angle > 50) and state == 'Down':
            range_flag = False
            feedback = ''

        elif (left_elbow_angle < 30 and right_elbow_angle < 30) and state == 'Down':
            state = 'Up'
            feedback = ''
            range_flag = True
            counter += 1

    except:
        left_angle.append(180)
        right_angle.append(180)

# 2.egzersiz
def recognise_pushdown(detection):
    global counter, state, feedback, range_flag, left_angle, right_angle
    global counter
    global state
    global feedback
    global range_flag
    global halfway


    try:
        landmarks = detection.pose_landmarks.landmark

        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

        left_elbow_angle1 = calc_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle1 = calc_angle(right_shoulder, right_elbow, right_wrist)
        left_angle.append(int(left_elbow_angle1))
        right_angle.append(int(right_elbow_angle1))

        if left_elbow_angle1 < 30 and right_elbow_angle1 < 30:
            if not range_flag:
                feedback = 'Did not curl completely.'
            else:
                feedback = 'Good rep!'
            state = 'up'

        elif (left_elbow_angle1 > 160 and right_elbow_angle1 > 160) and state == 'up':
            state = 'down'
            feedback = ''
            range_flag = True
            counter += 1

    except:
        left_angle.append(180)
        right_angle.append(180)

# 3.egzersiz
def recognise_latiralRaise(detection):
    global counter
    global state
    global feedback
    global range_flag
    global halfway


    try:
        landmarks = detection.pose_landmarks.landmark

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

        left_shoulder_angle = calc_angle(left_elbow, left_shoulder, left_hip)
        right_shoulder_angle = calc_angle(right_elbow, right_shoulder, right_hip)
        left_angle.append(int(left_shoulder_angle))
        right_angle.append(int(right_shoulder_angle))

        if (left_shoulder_angle > 90 and right_shoulder_angle > 90):
            if not range_flag:
                feedback = 'Did not raise completely.'
            else:
                feedback = 'Good rep!'
            state = 'up'

        elif (left_shoulder_angle < 30 and right_shoulder_angle < 30) and state == 'up':
            state = 'down'
            feedback = ''
            range_flag = True
            counter += 1

    except:
        left_angle.append(180)
        right_angle.append(180)

# 4.egzersiz
def recognise_squat(detection):
    global counter
    global state
    global feedback
    global range_flag
    global halfway
    global body_angles
    try:
        landmarks = detection.pose_landmarks.landmark

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]

        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        left_knee_angle = calc_angle(left_hip, left_knee, left_heel)
        right_knee_angle = calc_angle(right_hip, right_knee, right_heel)
        left_angle.append(int(left_knee_angle))
        right_angle.append(int(right_knee_angle))

        left_body_angle = calc_angle(left_shoulder, left_hip, left_knee)
        right_body_angle = calc_angle(right_shoulder, right_hip, right_knee)
        body_angles.append(int((left_body_angle + right_body_angle) / 2))

        if left_knee_angle > 160 and right_knee_angle > 160:
            if not halfway:
                feedback = 'Halfway.'
            else:
                feedback = 'Good rep!'
            state = 'up'

        if left_knee_angle <= 90 and right_knee_angle <= 90 and state == 'up':
            state = 'down'
            feedback = ''
            halfway = True
            counter += 1
    except:
        left_angle.append(180)
        right_angle.append(180)
        body_angles.append(180)

# 5.egzersiz
def recognise_situp(detection):

    global counter
    global state
    global feedback
    global range_flag
    global halfway
    global body_angles

    try:
        landmarks = detection.pose_landmarks.landmark

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

        # CALCULATE ANGLES
        angle_knee = calc_angle(left_hip, left_knee, left_heel)
        angle_body = calc_angle(left_shoulder, left_hip, left_knee)
        body_angles.append(int(angle_body))

        if (angle_body < 80 and angle_body > 50) and state == "Down":  # Half-way there (Used for checking bad situps)
            halfway = True

        if angle_body < 40 and state == "Down":  # Complete situp
            state = "Up"
            range_flag = True

        if angle_body > 90 and angle_knee < 60:  # Resting position;to check if situp was done properly
            state = "Down"

            if halfway:  # Check if a rep was attempted
                if range_flag:  # Check if a proper rep was performed
                    counter += 1
                    feedback = "İyi tekrar!"
                else:
                    feedback = "Did not perform sit up completely."
                range_flag = False  # Reset vars
                halfway = False

        if angle_knee > 70:  # Triggers anytime the legs are not tucked in
            feedback = "Keep legs tucked in closer"

    except:
        body_angles.append(180)

# 6.egzersiz
def recognise_legpress(detection):
    global counter
    global state
    global feedback
    global range_flag
    global halfway
    try:
        landmarks = detection.pose_landmarks.landmark

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]

        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]



        left_knee_angle = calc_angle(left_hip, left_knee, left_heel)
        right_knee_angle = calc_angle(right_hip, right_knee, right_heel)
        left_angle.append(int(left_knee_angle))
        right_angle.append(int(right_knee_angle))


        if left_knee_angle > 160 and right_knee_angle > 160:
            if not halfway:
                feedback = 'Halfway.'
            else:
                feedback = 'Good rep!'
            state = 'up'

        if left_knee_angle <= 90 and right_knee_angle <= 90 and state == 'up':
            state = 'down'
            feedback = ''
            halfway = True
            counter += 1
    except:
        left_angle.append(180)
        right_angle.append(180)

with st.container():
    # Streamlit app
    col11, col22, col33 = st.columns(3)
    with col11:
        st.title(':blue[exersise detector 🤖]')
        st.subheader("Bu modül, gerçek zamanlı web kamerası kullanarak eklemleri tespit"
                     " eder ve eklemler arasındaki mesafeleri ve açıları hesaplar. Bu sayede yapılan antrenmanın"
                     " formunu belirler ve tekrarları sayar.  Bu modül, egzersizlerinizi daha verimli ve güvenli "
                     "hale getirerek formunuzu iyileştirmenize yardımcı olur. ")


    with col33:
        st_lottie(
            pose_anim,
            speed=1,
            loop=True,
            quality="medium",
        )

st.write("---")
with st.container():
    # egzersiz seçimi
    st.subheader(":blue[egzersiz seçiniz]")
    exercise = st.selectbox('---', ('Curl', 'Pushdown', 'Lateral Raise', 'Squat', 'situp', 'legpress'))

    # WebRTC video streamer
    class VideoProcessor(VideoTransformerBase):

        def __init__(self):
            self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.exercise = exercise


        def recv(self, frame):
            global counter, state, feedback

            image = frame.to_ndarray(format="bgr24")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = self.pose.process(image)

            if result.pose_landmarks:
                if exercise == 'Curl':
                    recognise_curl(result)
                elif exercise == 'Pushdown':
                    recognise_pushdown(result)
                elif exercise == 'Lateral Raise':
                    recognise_latiralRaise(result)
                elif exercise == 'Squat':
                    recognise_squat(result)
                elif exercise == 'situp':
                    recognise_situp(result)
                elif exercise == 'legpress':
                    recognise_legpress(result)

                mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.putText(image, f'Counter: {counter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            image = cv2.putText(image, f'State: {state}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            image = cv2.putText(image, f'Feedback: {feedback}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            return av.VideoFrame.from_ndarray(image, format="bgr24")


    webrtc_streamer(key="example", video_processor_factory=VideoProcessor)



st.write("---")

with st.container():
    st.header(":red[egzersiz formları]")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(":blue[LATERAL RAISE]")
        st.video(lateral_vid)
        st.subheader(":blue[PUSHDOWN]")
        st.video(pushdown_vid)

    with col2:
        st.subheader(":blue[CURL]")
        st.video(curl_vid)
        st.subheader(":blue[SITUP]")
        st.video(situp_vid)

    with col3:
        st.subheader(":blue[SQUAT]")
        st.video(squat_vid)
        st.subheader(":blue[LEG PRESS]")
        st.video(legpress_vid)
