from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('best.pt')

# Open the video file
video_path = "1.mp4"
cap = cv2.VideoCapture(video_path)
H = np.load("h.npy")


# Store the track history
track_history = defaultdict(lambda: [])

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    frame = cv2.resize(frame, (1280, 900))

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        dst = cv2.imread('map_g.png', -1)
        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point

            # Draw the tracking lines

            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            h_points = cv2.perspectiveTransform(points.astype(np.float32), H, (dst.shape[1], dst.shape[0]))

            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255), thickness=2)
            cv2.circle(dst, (h_points[-1][0].astype(int)), color=(0, 255, 255), thickness=3, radius=2)

        # Display the annotated frame

        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        cv2.imshow("Map", dst)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()