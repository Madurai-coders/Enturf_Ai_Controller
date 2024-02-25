# from collections import defaultdict
# import cv2
# import numpy as np
# from ultralytics import YOLO

# # Load the YOLOv8 model
# try:
#     model = YOLO('yolov8n.pt')
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading model: {e}")

# # Open the video file
# video_path = r'media\sample\output.mp4'  # Use a raw string for paths
# cap = cv2.VideoCapture(video_path)

# if not cap.isOpened():
#     print(f"Failed to open video: {video_path}")

# # Store the track history
# track_history = defaultdict(lambda: [])

# # Loop through the video frames
# while cap.isOpened():
#     # Read a frame from the video
#     success, frame = cap.read()

#     if not success:
#         print("Failed to read frame. Ending loop.")
#         break

#     try:
#         # Run YOLOv8 tracking on the frame, persisting tracks between frames
#         results = model.track(frame, persist=True)
#         print("Tracking successful.")

#         # Get the boxes and track IDs
#         boxes = results[0].boxes.xywh.cpu()
#         track_ids = results[0].boxes.id.int().cpu().tolist()

#         # Visualize the results on the frame
#         annotated_frame = np.array(results[0].plot())  # Ensure it's an array

#         # Plot the tracks
#         for box, track_id in zip(boxes, track_ids):
#             x, y, w, h = box
#             track = track_history[track_id]
#             track.append((float(x), float(y)))  # x, y center point
#             if len(track) > 30:  # retain 90 tracks for 90 frames
#                 track.pop(0)

#             # Draw the tracking lines
#             if len(track) > 1:  # Need at least 2 points to draw lines
#                 points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
#                 cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)

#         # Display the annotated frame
#         cv2.imshow("YOLOv8 Tracking", annotated_frame)

#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             print("Exiting loop by user request.")
#             break
#     except Exception as e:
#         print(f"Error during processing frame: {e}")

# # Release the video capture object and close the display window
# cap.release()
# cv2.destroyAllWindows()


from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort import DeepSort

# Load the YOLOv8 model
try:
    model = YOLO('yolov8n.pt')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Initialize DeepSORT tracker
deepsort = DeepSort(max_dist=0.2, min_confidence=0.3, nms_max_overlap=0.5, max_iou_distance=0.7, max_age=70, n_init=3, nn_budget=100)

# Open the video file
video_path = r'media\sample\output.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Failed to open video: {video_path}")

# Store the track history
track_history = defaultdict(lambda: [])

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Failed to read frame. Ending loop.")
        break

    try:
        # Run YOLOv8 detection on the frame
        results = model.detect(frame)
        print("Detection successful.")

        # Extract detections
        xywhs = results[0].boxes.xywh.cpu()  # Bounding boxes
        confs = results[0].boxes.conf.cpu()  # Confidence scores
        clss = results[0].boxes.cls.cpu()    # Class IDs

        # Pass detections to DeepSORT for tracking
        outputs = deepsort.update(xywhs, confs, clss, frame)

        # Visualize the tracking
        annotated_frame = frame.copy()
        for output in outputs:
            x1, y1, x2, y2, track_id = output
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, str(track_id), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 + DeepSORT Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exiting loop by user request.")
            break
    except Exception as e:
        print(f"Error during processing frame: {e}")

cap.release()
cv2.destroyAllWindows()

