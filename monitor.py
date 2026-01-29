import cv2
from ultralytics import YOLO
from datetime import datetime
import time
import os

# =============================
# CONFIG
# =============================
STATE_STABLE_TIME = 2        # detik sebelum status benar-benar berubah
SLEEPY_TIME = 6              # diam ≥ 6 detik → mengantuk

POMODORO_FOCUS = 25 * 60
POMODORO_BREAK = 5 * 60

LOG_FILE = "activity_log.csv"

# =============================
# INIT
# =============================
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

current_state = "Fokus"
candidate_state = None
state_start_time = time.time()

pomodoro_mode = "Fokus"
pomodoro_start = time.time()

last_logged_state = None

prev_gray = None
still_start_time = None
MOVEMENT_THRESHOLD = 20000  # SANGAT PENTING

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,status\n")

# =============================
# FUNCTIONS
# =============================
def log_state(state):
    global last_logged_state
    if state != last_logged_state:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()},{state}\n")
        last_logged_state = state

def update_state(new_state):
    global current_state, candidate_state, state_start_time

    if new_state != current_state:
        if candidate_state != new_state:
            candidate_state = new_state
            state_start_time = time.time()
        else:
            if time.time() - state_start_time >= STATE_STABLE_TIME:
                current_state = new_state
                log_state(current_state)
    else:
        candidate_state = None
        state_start_time = time.time()

def draw_pomodoro(frame, remaining, total):
    center = (500, 100)
    radius = 40
    angle = int(360 * remaining / total)

    cv2.circle(frame, center, radius, (200, 200, 200), 2)
    cv2.ellipse(frame, center, (radius, radius),
                -90, 0, angle, (0, 255, 0), 4)

# =============================
# MAIN LOOP
# =============================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # =============================
    # YOLO DETECTION
    # =============================
    results = model(frame, verbose=False)[0]
    person = False
    phone = False

    for box in results.boxes:
        cls = int(box.cls[0])
        name = model.names[cls]
        if name == "person":
            person = True
        if name == "cell phone":
            phone = True

    # =============================
    # MOTION DETECTION
    # =============================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    motion_detected = True
    if prev_gray is not None:
        frame_delta = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_score = thresh.sum()
        motion_detected = motion_score > MOVEMENT_THRESHOLD

    prev_gray = gray

    # =============================
    # HUMAN-AWARE LOGIC (FIX)
    # =============================
    if not person:
        update_state("Tidak Ada Aktivitas")
        still_start_time = None

    elif phone:
        update_state("Terdistraksi")
        still_start_time = None

    else:
        if not motion_detected:
            if still_start_time is None:
                still_start_time = time.time()
            elif time.time() - still_start_time >= SLEEPY_TIME:
                update_state("Mengantuk")
        else:
            if current_state != "Mengantuk":
                still_start_time = None
                update_state("Fokus")

    # =============================
    # POMODORO LOGIC
    # =============================
    now = time.time()
    elapsed = now - pomodoro_start

    if pomodoro_mode == "Fokus":
        remaining = max(0, POMODORO_FOCUS - elapsed)
        if remaining == 0:
            pomodoro_mode = "Istirahat"
            pomodoro_start = time.time()
    else:
        remaining = max(0, POMODORO_BREAK - elapsed)
        if remaining == 0:
            pomodoro_mode = "Fokus"
            pomodoro_start = time.time()

    # =============================
    # DISPLAY
    # =============================
    cv2.putText(frame, f"STATUS: {current_state}",
                (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.putText(frame, f"POMODORO: {pomodoro_mode}",
                (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 0), 2)

    mins = int(remaining // 60)
    secs = int(remaining % 60)
    cv2.putText(frame, f"Sisa: {mins:02d}:{secs:02d}",
                (30, 120), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 255), 2)

    draw_pomodoro(frame, remaining,
                  POMODORO_FOCUS if pomodoro_mode == "Fokus" else POMODORO_BREAK)

    cv2.putText(frame, f"Motion: {motion_detected}",
                (30, 160), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    if current_state == "Mengantuk":
        cv2.putText(frame, "⚠️ TERDETEKSI MENGANTUK",
                    (30, 200), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 0, 255), 3)

    cv2.imshow("Student Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
