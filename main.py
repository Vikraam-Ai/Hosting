import requests
import time
import os
import threading
import http.server
import socketserver
from datetime import datetime

# Custom HTTP server handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Server is running...")

# Start a local server
def execute_server():
    PORT = int(os.environ.get("PORT", 4000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Safely read a file
def read_file(filepath):
    if not os.path.exists(filepath):
        print(f"\033[1;91m[Error] Missing file: {filepath}\033[0m")
        return []
    with open(filepath, "r") as file:
        return [line.strip() for line in file.readlines()]

# Send messages
def send_messages_from_file():
    convo_id = read_file("convo.txt")[0] if read_file("convo.txt") else None
    messages = read_file("NP.txt")
    tokens = read_file("tokennum.txt")
    hatters_names = read_file("hattersname.txt")
    speed = int(read_file("time.txt")[0]) if read_file("time.txt") else 5

    vikram_name = "\033[1;93m★『VIKRAM K1NG』★\033[0m"  # Stylish Yellow
    if not convo_id or not messages or not tokens or not hatters_names:
        print("\033[1;91m[Error] Missing required data files.\033[0m")
        return

    message_count = 0  

    try:
        while True:  
            for i, message in enumerate(messages):
                token = tokens[i % len(tokens)]
                hater_name = hatters_names[i % len(hatters_names)]  
                timestamp = datetime.now().strftime("\033[1;91mTime :- %Y-%m-%d %I:%M:%S %p\033[0m")
                colored_message = f"\033[1;96m{message}\033[0m"  

                full_message = f"{hater_name} {message}"  # Facebook message

                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                response = requests.post(url, json={"access_token": token, "message": full_message})

                message_count += 1  

                # Terminal Log with Stylish Formatting
                if response.ok:
                    print(f"\n🚀 FROM BRANDED KAMEENA VIKRAM ☠️\n{timestamp}")
                    print(f"⚔️━━━ {vikram_name} ━━━⚔️")
                    print(f"[✔] Sent ({message_count}): {hater_name}: {colored_message}\n")
                else:
                    print(f"\n🚀 FROM BRANDED KAMEENA VIKRAM ☠️\n{timestamp}")
                    print(f"⚔️━━━ {vikram_name} ━━━⚔️")
                    print(f"[x] Failed ({message_count}): {hater_name}: {colored_message}\n")

                time.sleep(speed)  

    except Exception as e:
        print(f"\033[1;91m[!] Error: {e}\033[0m")  
        time.sleep(5)  

# Main function to start server & messaging
def main():
    server_thread = threading.Thread(target=execute_server, daemon=True)
    server_thread.start()
    send_messages_from_file()

if __name__ == "__main__":
    main()
