import cv2
import threading
from camera import load_model, get_detections, assign_colors
from servo import perform_servo_action, cleanup

def main():
    model = load_model()
    names = model.names
    colors = assign_colors(names)

    cap = cv2.VideoCapture(1)
    print("🎥 Starting cacao variety detection. Press 'q' to quit.\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            detections = get_detections(model, frame)
            print("Detected beans in frame:")

            if len(detections) == 0:
                print("  None")

            for *box, conf, cls in detections:
                cls = int(cls)
                label = names[cls]
                confidence = float(conf)

                x1, y1, x2, y2 = map(int, box)
                color = colors[label]
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

                label_text = f"{label} ({confidence:.2f})"
                (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw, y1), color, -1)
                cv2.putText(frame, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                print(f"  - {label} (Confidence: {confidence:.2f})")
                threading.Thread(target=perform_servo_action, args=(label,), daemon=True).start()

            cv2.imshow("Cacao Variety Detection - Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        cleanup()
        print("🔌 Detection stopped and GPIO cleaned up.")

if __name__ == "__main__":
    main()
