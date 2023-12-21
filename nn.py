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

out = cv2.VideoWriter('annotated_frame.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280, 900))
out_map = cv2.VideoWriter('Map.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 1, (731, 708))

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_time = 1 / fps

# Store the previous positions of each car
previous_positions = {}

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
        dst = cv2.imread('map.png', -1)
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

            # Calculate the speed of the car

            if track_id in previous_positions:
                dx, dy = x - previous_positions[track_id][0], y - previous_positions[track_id][1]
                distance = np.sqrt(dx**2 + dy**2)  # in pixels
                speed = distance / frame_time  # pixels/second

                # Convert speed to km/hour
                km_per_pixel = 0.000021  # scale from GIS
                speed_kmh = speed * km_per_pixel * 3600  # km/hour

                # Convert speed to string and write it on the frame
                speed_text = f"Speed: {speed_kmh:.2f} km/hour"
                cv2.putText(annotated_frame, speed_text, (int(x - 25), int(y - 45)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            previous_positions[track_id] = (x, y)
        
        # Display the annotated frame
        out.write(annotated_frame)
        out_map.write(dst)
        #cv2.imshow("YOLOv8 Tracking", annotated_frame)
        #cv2.imshow("Map", dst)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
# Release the video capture object and close the display window
cap.release()
out.release()
out_map.release()
cv2.destroyAllWindows()