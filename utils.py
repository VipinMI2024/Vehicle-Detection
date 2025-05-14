# utils.py
import cv2

def center_handle(x, y, w, h):
    return int(x + w / 2), int(y + h / 2)

def draw_text(frame, text, pos=(10, 30), color=(0, 0, 255), size=1, thickness=2):
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)

def draw_count_line(frame, y_pos, color, width=3):
    cv2.line(frame, (0, y_pos), (frame.shape[1], y_pos), color, width)