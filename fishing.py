import websocket
import json
import threading
import time
import keyboard

# Replace these with your actual login credentials and WebSocket URLs
username_or_email = 'lukaszs'
password = 'removed'
login_url = 'wss://2023.holidayhackchallenge.com/ws'

# Global variable to store dock_slip_id
dock_slip_id = None

# Step 1: Prepare login payload
login_payload = {
    'type': 'WS_LOGIN',
    'usernameOrEmail': username_or_email,
    'password': password
}

# Step 2: Define the WebSocket event handler
def on_message(ws, message):
    global dock_slip_id  # Use the global variable
    
    if "AUF_WIEDERSEHEN" in message:
        return  # Ignore messages of type "AUF_WIEDERSEHEN"
    
    print(f"Received message: {message}")
    
    try:
        data = json.loads(message)
        if 'dockSlip' in data:
            dock_slip_id = data['dockSlip']
            print(f"Retrieved dock_slip_id: {dock_slip_id}")
            
            # Call a function to handle the dock_slip_id (e.g., store it for future use)
            handle_dock_slip_id(dock_slip_id)
            
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # Your logic for handling other messages goes here

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with status code {close_status_code}: {close_msg}")

# Function to send {"type":"setSail"} command after login
def send_set_sail_command(ws):
    ws.send(json.dumps({"type": "setSail"}))
    print("Sent {'type':'setSail'} command after login")

# Function to send "cast" command every 10 seconds
def send_cast_periodically(ws):
    while ws.sock and ws.sock.connected:  # Check if the connection is still open
        ws.send("cast")  # Send the "cast" string directly
        print("Sent 'cast' command")
        time.sleep(10)

    print("WebSocket connection closed. Stopping 'send_cast_periodically' thread.")

# Function to handle the retrieved dock_slip_id
def handle_dock_slip_id(dock_slip_id):
    print(f"Handling dock_slip_id: {dock_slip_id}")
    # You can implement your logic to store or use the dock_slip_id as needed

# Register the 'F1' key event to stop the script
def stop_script(ws, thread, cast_thread):
    print("Stopping script gracefully...")
    ws.close()
    thread.join()
    cast_thread.join()
    exit()

# Register the 'F1' key event
keyboard.on_press_key("F1", lambda event: stop_script(ws, thread, cast_thread))

# Step 3: Connect to the WebSocket using the threading approach
ws = websocket.WebSocketApp(login_url, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = lambda ws: (ws.send(json.dumps(login_payload)), send_set_sail_command(ws))

# Start a separate thread for handling WebSocket events
thread = threading.Thread(target=ws.run_forever)
thread.daemon = True
thread.start()

# Start a separate thread for sending "cast" command every 10 seconds
cast_thread = threading.Thread(target=send_cast_periodically, args=(ws,))
cast_thread.daemon = True
cast_thread.start()

# Allow some time for the WebSocket connection to be established before interacting
time.sleep(5)

# Keep the script running
thread.join()
cast_thread.join()
