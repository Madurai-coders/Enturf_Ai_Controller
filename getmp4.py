

# import asyncio
# import datetime
# import os
# import subprocess
# import time
# import signal

# import cv2
# import numpy as np
# from ultralytics import YOLO
# import sys

# from scriptTest import send_message, update_database




# import asyncio
# import threading


# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()

# new_loop = asyncio.new_event_loop()
# t = threading.Thread(target=start_loop, args=(new_loop,))
# t.start()



# def clear_directory(directory):
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
#         try:
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#         except Exception as e:
#             print(f"Error deleting {file_path}: {e}")





# fps = 25
# width = 1920
# height = 1080

# # Get current date and time
# current_datetime = datetime.datetime.now()
# folder_name = current_datetime.strftime("%Y%m%d_%H%M%S")

# # Folder path (modify the base path as needed)
# base_path = r'C:\Users\Kaamil\Documents\ENTURF_AI_CONTROLLER\media\rec'
# new_folder_path = os.path.join(base_path, folder_name)
# new_folder_name = '/media/rec/'+folder_name

# # Create the folder
# if not os.path.exists(new_folder_path):
#     os.makedirs(new_folder_path)

# # Update the ffmpeg command
# command1 = [
#     'ffmpeg', '-y', '-re', '-f', 'rawvideo', '-vcodec', 'rawvideo',
#     '-pix_fmt', 'bgr24', '-s', "{}x{}".format(width, height),
#     '-r', str(fps), '-i', '-', '-pix_fmt', 'yuv420p', '-g', '50',
#     '-crf', '21', '-c:v', 'libx264', '-b:v', '2M', '-bufsize', '64M',
#     '-maxrate', "4M", '-preset', 'veryfast', '-sc_threshold', '0',
#     '-start_number', '0', '-hls_time', '2', '-hls_list_size', '0',
#     '-hls_flags', '+program_date_time', '-hls_playlist_type', 'event',
#     '-f', 'hls', os.path.join(new_folder_path, 'hsl.m3u8')
# ]


# p = subprocess.Popen(command1, stdin=subprocess.PIPE)
# model = YOLO('best-n.pt')
# names = model.names

# m3u8_url = "rtsp://admin:user@123@3.108.86.115:5931/Streaming/Channels/101"
# # m3u8_url = "media/cam3/hsl.m3u8"
# cap = cv2.VideoCapture(m3u8_url)

# if not cap.isOpened():
#     print("Error: Could not open video stream.")
#     exit()

# frame_rate = cap.get(cv2.CAP_PROP_FPS)
# delay = 1 / frame_rate


# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(f"Start of x-axis: 0, End of x-axis: {frame_width - 1}")
# frame_counter = 0
# previous_center_x=0

   



# def signal_handler(sig, frame):
#     print("Termination signal received")
#     cleanup()
#     sys.exit(0)
    
    
# def cleanup():
#     global cleanup_done
#     if cleanup_done:
#         return  # Prevent cleanup from running multiple times

#     print("Cleaning up...")
#     cap.release()
#     cv2.destroyAllWindows()
#     if p.poll() is None:  # Check if the subprocess is still running
#         p.stdin.write(b'q')  # Sending 'q' to ffmpeg process
#         p.stdin.close()
#     p.wait()
#     # Append '#EXT-X-ENDLIST' to the m3u8 file
#     with open(os.path.join(new_folder_path, 'hsl.m3u8'), 'a') as f:
#         f.write('#EXT-X-ENDLIST\n')
#     print("Cleanup completed")
#     cleanup_done = True

# cleanup_done = False 

# if __name__ == "__main__":
#     CAM4_DIR = r"C:\Users\Kaamil\Documents\enturf-compression\media\cam4"
#     clear_directory(CAM4_DIR)

#     try:
#         while cap.isOpened():
#             success, frame = cap.read()
   
#             if frame_counter % 25 == 0:
#                 results = model.track(frame, persist=True)

#                 if results[0].boxes:
#                     boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
#                     cls = results[0].boxes.cls
#                     for box, cls_id in zip(boxes, cls):
#                         cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
#                         cv2.putText(
#                             frame,
#                             f"Id {names[int(cls_id)]}",
#                             (box[0], box[1]),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,
#                             (0, 0, 255),
#                             2,
#                         )
            
#                     center_x = (box[0] + box[2]) // 2
#                     center_y = (box[1] + box[3]) // 2

        
#             cv2.imshow("YOLOv8 Tracking", frame)

#             if frame_counter % 25 == 0:
#                 if results[0].boxes:
#                     previous_center_x=center_x
#                     asyncio.run_coroutine_threadsafe(send_message('chat_iot', str(center_x)), new_loop)
#                     update_database(new_folder_name, str(center_x))
#                 else:
#                     asyncio.run_coroutine_threadsafe(send_message('chat_iot', str(previous_center_x)), new_loop)
#                     update_database(new_folder_name, str(previous_center_x))

#             frame_counter += 1
            
#             p.stdin.write(frame.tobytes())

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             time.sleep(delay)

#         cap.release()
#         cv2.destroyAllWindows()

#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         cleanup()







import asyncio
import datetime
import os
import subprocess
import time
import signal
import sys
import threading
import requests
import numpy as np

import cv2
from ultralytics import YOLO

from scriptTest import send_message, update_database

def start_loop(loop):
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    except Exception as e:
        print(f"Error in asyncio loop: {e}")

new_loop = asyncio.new_event_loop()
t = threading.Thread(target=start_loop, args=(new_loop,))
t.start()

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

fps = 25
width = 1920
height = 1080

# Get current date and time
current_datetime = datetime.datetime.now()
folder_name = current_datetime.strftime("%Y%m%d_%H%M%S")

# Folder path (modify the base path as needed)
base_path = r'C:\Users\Kaamil\Documents\ENTURF_AI_CONTROLLER\media\rec'
new_folder_path = os.path.join(base_path, folder_name)
new_folder_name = folder_name

# Create the folder
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

# Update the ffmpeg command
# command1 = [
#     'ffmpeg', '-y', '-re', '-f', 'rawvideo', '-vcodec', 'rawvideo',
#     '-pix_fmt', 'bgr24', '-s', "{}x{}".format(width, height),
#     '-r', str(fps), '-i', '-', '-pix_fmt', 'yuv420p', '-g', '50',
#     '-crf', '23', '-c:v', 'libx264', '-b:v', '2M', '-bufsize', '64M',
#     '-maxrate', "4M", '-preset', 'ultrafast', '-sc_threshold', '0',
#     '-start_number', '0', '-hls_time', '6', '-hls_list_size', '0',
#     '-hls_flags', '+program_date_time', '-hls_playlist_type', 'event',
#      os.path.join(new_folder_path, 'hsl.m3u8')
# ]

command1 = [
    'ffmpeg', '-y', '-re', '-f', 'rawvideo', '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24', '-s', "{}x{}".format(width, height),
    '-r', str(fps), '-i', '-', '-pix_fmt', 'yuv420p', '-g', '50',
    '-crf', '23', '-c:v', 'libx264', '-b:v', '2M', '-bufsize', '64M',
    '-maxrate', "4M", '-preset', 'ultrafast', '-sc_threshold', '0',
    os.path.join(new_folder_path, 'output.mp4')  # Specify MP4 output here
]

p = subprocess.Popen(command1, stdin=subprocess.PIPE)
model = YOLO('best-n.pt')
names = model.names

# m3u8_url = "rtsp://admin:user@123@3.108.86.115:5931/Streaming/Channels/101"
m3u8_url = "media/rec/20240205_174033/output.mp4"
# m3u8_url='http://3.108.86.115:9000/media/output.m3u8'
cap = cv2.VideoCapture(m3u8_url)
cap1 = cv2.VideoCapture(m3u8_url)
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"FPS of the video: {fps}")
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

frame_rate = cap.get(cv2.CAP_PROP_FPS)
delay = 1 / frame_rate

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(f"Start of x-axis: 0, End of x-axis: {frame_width - 1}")
frame_counter = 0
previous_center_x = 0

def signal_handler(sig, frame):
    print("Termination signal received")
    cleanup()
    sys.exit(0)

def cleanup():
    global cleanup_done
    if cleanup_done:
        return  # Prevent cleanup from running multiple times

    print("Cleaning up...")
    cap.release()
    cv2.destroyAllWindows()
    if p.poll() is None:  # Check if the subprocess is still running
        p.stdin.write(b'q')  # Sending 'q' to ffmpeg process
        p.stdin.close()
    p.wait()
    # Append '#EXT-X-ENDLIST' to the m3u8 file
    with open(os.path.join(new_folder_path, 'hsl.m3u8'), 'a') as f:
        f.write('#EXT-X-ENDLIST\n')
    print("Cleanup completed")
    cleanup_done = True

cleanup_done = False 
max_retries = 5
retry_delay = 5  # Initial delay in seconds, will increase progressively
max_delay = 60   # Maximum delay time

def is_stream_available(url):
    # Attempt to open the stream with OpenCV
    test_cap = cv2.VideoCapture(url)
    success, _ = test_cap.read()
    test_cap.release()
    return success
    
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    CAM4_DIR = r"C:\Users\Kaamil\Documents\enturf-compression\media\cam4"
    clear_directory(CAM4_DIR)
   
    try:
        while cap.isOpened():
            success, frame = cap.read()
            # success2, frame2 = cap1.read()
            
            # if success2 and success1:
            #     # Calculate the new width for each frame to fit them side by side within the specified width
            #     new_width_per_frame = width // 2
                
            #     # Specify how much to crop from the right of both frames (in pixels)
            #     crop_right_pixels =175  # Adjust this value as needed
                
            #     # Crop both frames on the right before any other processing
            #     cropped_frame1 = frame1[:, crop_right_pixels:]
            #     cropped_frame2 = frame2[:, crop_right_pixels:]
                
            #     # Calculate aspect ratio for each frame after cropping
            #     aspect_ratio_frame1 = cropped_frame1.shape[0] / cropped_frame1.shape[1]
            #     aspect_ratio_frame2 = cropped_frame2.shape[0] / cropped_frame2.shape[1]
                
            #     # Calculate the new height for each frame based on the new width and maintaining aspect ratio
            #     new_height_frame1 = int(new_width_per_frame * aspect_ratio_frame1)
            #     new_height_frame2 = int(new_width_per_frame * aspect_ratio_frame2)
                
            #     # Mirror the cropped first frame horizontally before resizing
            #     mirrored_frame1 = cv2.flip(cropped_frame1, 1)
            #     resized_frame1 = cv2.resize(mirrored_frame1, (new_width_per_frame, min(new_height_frame1, height)))
                
            #     # Resize the cropped second frame to fit within the specified dimensions without mirroring
            #     resized_frame2 = cv2.resize(cropped_frame2, (new_width_per_frame, min(new_height_frame2, height)))
                
            #     # Create a new image for the output frame with the specified dimensions
            #     frame = np.zeros((height, width, 3), dtype=cropped_frame1.dtype)
                
            #     # Calculate vertical offsets to center each frame vertically
            #     offset_frame1 = (height - resized_frame1.shape[0]) // 2
            #     offset_frame2 = (height - resized_frame2.shape[0]) // 2
                
            #     # Place each resized frame into the output frame, centered vertically
            #     frame[offset_frame1:offset_frame1+resized_frame1.shape[0], :new_width_per_frame] = resized_frame1
            #     frame[offset_frame2:offset_frame2+resized_frame2.shape[0], new_width_per_frame:new_width_per_frame+resized_frame2.shape[1]] = resized_frame2
            # else:
            #     print("One of the frames was not read successfully.")

            
            # if not success or frame is None:
            #     print("Failed to read frame or frame is None.")
            #     retry_attempts += 1

            #     if retry_attempts > max_retries:
            #         print("Max retries reached. Checking stream availability.")
            #         if is_stream_available(m3u8_url):
            #             print("Reinitializing capture.")
            #             cap.release()
            #             time.sleep(min(retry_delay, max_delay))
            #             cap = cv2.VideoCapture(m3u8_url)
            #             retry_attempts = 0
            #             retry_delay = min(retry_delay * 2, max_delay)  # Increase delay for next time
            #         else:
            #             print("Stream not available. Retrying after delay.")
            #             time.sleep(min(retry_delay, max_delay))
            #             retry_attempts = 0  # Reset attempts as we are waiting for stream availability
            #     continue  # Skip this iteration

            retry_attempts = 0
            retry_delay = 5

            if frame_counter % 25 == 0:
                results = model.track(frame, persist=True)

                if results[0].boxes:
                    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                    cls = results[0].boxes.cls
                    for box, cls_id in zip(boxes, cls):
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                        cv2.putText(
                            frame,
                            f"Id {names[int(cls_id)]}",
                            (box[0], box[1]),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2,
                        )
            
                    center_x = (box[0] + box[2]) // 2
                    center_y = (box[1] + box[3]) // 2

            cv2.imshow("YOLOv8 Tracking", frame)

            if frame_counter % 25 == 0:
                if results[0].boxes:
                    previous_center_x = center_x
                    asyncio.run_coroutine_threadsafe(send_message('chat_iot', str(center_x)), new_loop)
                    update_database(new_folder_name, str(center_x))
                else:
                    asyncio.run_coroutine_threadsafe(send_message('chat_iot', str(previous_center_x)), new_loop)
                    update_database(new_folder_name, str(previous_center_x))

            frame_counter += 1

            try:
                p.stdin.write(frame.tobytes())
            except BrokenPipeError:
                print("Broken pipe error, possibly due to ffmpeg process ending.")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # time.sleep(delay)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cleanup()

















