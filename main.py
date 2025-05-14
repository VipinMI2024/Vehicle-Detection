import cv2
import numpy as np
from config import COUNT_LINE_POSITION, MIN_WIDTH, MIN_HEIGHT, LINE_OFFSET
from config import LINE_COLOR, CROSS_LINE_COLOR, TEXT_COLOR, MOG_HISTORY, MOG_THRESHOLD
from utils import center_handle, draw_text, draw_count_line

# Load video
cap = cv2.VideoCapture('vehicles.mp4') 

# Initialize background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history=MOG_HISTORY, varThreshold=MOG_THRESHOLD, detectShadows=False)

# Store tracked vehicles
tracked_vehicles = {}
next_vehicle_id = 0
vehicle_count = 0

def assign_vehicle_id(center, existing_tracks, threshold=60):
    """Assign a unique ID to a new vehicle or match with an existing track."""
    min_distance = float('inf')
    matched_id = None
    for vehicle_id, data in existing_tracks.items():
        prev_center = data['center']
        distance = np.sqrt((center[0] - prev_center[0])**2 + (center[1] - prev_center[1])**2)
        if distance < min_distance and distance < threshold:
            min_distance = distance
            matched_id = vehicle_id
    return matched_id

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize and crop ROI
    frame = cv2.resize(frame, (1020, 600))
    roi = frame[200:600, :]  # ROI: y=200 to 600

    # Background subtraction
    mask = fgbg.apply(roi)
    _, mask = cv2.threshold(mask, 244, 255, cv2.THRESH_BINARY)
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)  # Reduce noise
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=3)  # Connect vehicle parts

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw counting line
    draw_count_line(roi, COUNT_LINE_POSITION, LINE_COLOR)

    current_frame_detections = []

    # Process contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        if w >= MIN_WIDTH and h >= MIN_HEIGHT and area > 300:
            cx, cy = center_handle(x, y, w, h)
            current_frame_detections.append((cx, cy, x, y, w, h))
            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.circle(roi, (cx, cy), 4, (0, 0, 255), -1)
            cv2.putText(roi, f"ID: {next_vehicle_id}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Update tracked vehicles
    new_tracked_vehicles = {}
    for detection in current_frame_detections:
        cx, cy, x, y, w, h = detection
        vehicle_id = assign_vehicle_id((cx, cy), tracked_vehicles)

        if vehicle_id is not None:
            # Update existing vehicle
            new_tracked_vehicles[vehicle_id] = {
                'center': (cx, cy),
                'crossed': tracked_vehicles[vehicle_id]['crossed'],
                'prev_y': tracked_vehicles[vehicle_id]['prev_y']
            }
        else:
            # New vehicle
            new_tracked_vehicles[next_vehicle_id] = {
                'center': (cx, cy), 
                'crossed': False, 
                'prev_y': cy
            }
            next_vehicle_id += 1

    # Counting logic
    for vehicle_id, data in new_tracked_vehicles.items():
        current_y = data['center'][1]
        prev_y = data['prev_y']

        # Count if vehicle crosses the line (moving downward)
        if not data['crossed'] and prev_y < COUNT_LINE_POSITION <= current_y:
            vehicle_count += 1
            new_tracked_vehicles[vehicle_id]['crossed'] = True
            cv2.line(roi, (0, COUNT_LINE_POSITION), (roi.shape[1], COUNT_LINE_POSITION), CROSS_LINE_COLOR, 3)
            print(f"Vehicle {vehicle_id} counted at y={current_y}, total count={vehicle_count}")

        # Update previous y for next frame
        new_tracked_vehicles[vehicle_id]['prev_y'] = current_y

    # Update tracked vehicles (remove if out of ROI)
    tracked_vehicles = {k: v for k, v in new_tracked_vehicles.items() if v['center'][1] < roi.shape[0] - 10}

    # Display total count
    draw_text(roi, f"Total Vehicles: {vehicle_count}", pos=(10, 50), color=TEXT_COLOR, size=1)

    # Debug: Show mask and frame
    cv2.imshow("Mask", mask)
    cv2.imshow("Vehicle Detection and Counting", roi)

    # Exit on ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()