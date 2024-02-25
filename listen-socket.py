import asyncio
import websockets
import subprocess
import json
import threading
import time

python_executable = r"C:\Users\Kaamil\Documents\Enturf_Ai_Controller\venv\Scripts\python"
process = None  # Declare process as a global variable

def run_yolov8():
    global process  # Indicate that we are using the global process variable
    print("Trigger condition met. Running yolov8.py...")
    process = subprocess.Popen([python_executable, "yolov8.py"])  # Use Popen and assign to process

async def listen():
    global process  # Indicate that we are using the global process variable
    uri = "ws://192.168.0.6:8000/AIController/"  # WebSocket server URI

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            message_dict = json.loads(message)

            # Trigger the script
            if message_dict.get("value") == "on" and process is None:
                time.sleep(10)# Check if process is not already running
                yolov8_thread = threading.Thread(target=run_yolov8)
                yolov8_thread.start()

            # Terminate the script
            elif message_dict.get("value") == "off" and process is not None:
                print("Close command received. Terminating yolov8.py...")
                process.terminate()
                process = None

asyncio.run(listen())

