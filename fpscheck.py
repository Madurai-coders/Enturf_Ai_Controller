import cv2

# Path to the video file
video_path = 'http://3.108.86.115:9000/media/output.m3u8'

# Open the video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
else:
    # Get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS of the video: {fps}")

# Release the video capture object
cap.release()
