from flask import Flask, request, jsonify, send_from_directory
import os
import cv2
from ultralytics import YOLO

app = Flask(__name__)
UPLOAD_FOLDER = "public/uploads"
PROCESSED_FOLDER = "public/processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

model = YOLO("yolov8m.pt")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    output_filename = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}")

    # Process video with YOLO
    cap = cv2.VideoCapture(filename)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_filename, fourcc, 30, 
                          (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = model.names[int(box.cls[0])]

                if cls in ["car", "truck", "bus", "motorcycle"]:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{cls} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

    return jsonify({"videoUrl": f"/processed/{os.path.basename(output_filename)}"})


@app.route("/processed/<filename>")
def get_video(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
