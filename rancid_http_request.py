from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import subprocess
import time
from urllib.parse import urlparse, unquote

class ConfigHandler(BaseHTTPRequestHandler):
    def add_cors_headers(self):
        """Adds CORS headers to the response."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_DELETE(self):
        if self.path.startswith("/delog/"):
            log_file = self.path.split("/delog/")[1]
            logs_dir = "/var/lib/rancid/logs"
            file_path = os.path.join(logs_dir, log_file)

            print(f"Attempting to delete file: {file_path}")

            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    response = {
                        "status": "success",
                        "response": f"File deleted: {file_path}"
                    }
                    self.send_response(200)
                else:
                    response = {
                        "status": "error",
                        "response": f"File not found: {file_path}"
                    }
                    self.send_response(404)

            except Exception as e:
                response = {
                    "status": "error",
                    "response": f"An error occurred: {str(e)}"
                }
                self.send_response(500)

            self.send_header("Content-Type", "application/json")
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))


    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith("/diff/"):
            try:
                router_name = unquote(self.path.split("/diff/")[1])
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length)
                request_body = json.loads(post_data)

                r1 = request_body.get("r1")
                r2 = request_body.get("r2")

                if not r1 or not r2:
                    raise ValueError("Both 'r1' and 'r2' must be provided.")

                config_dir = "/var/lib/rancid/newRouters/configs"
                file_path = os.path.join(config_dir, router_name)

                if not os.path.isfile(file_path):
                    response = {"status": "error", "response": "Router config not found"}
                    self.send_response(404)
                else:
                    command = ["cvs", "diff", "-r", str(r1), "-r", str(r2), file_path]
                    result = subprocess.run(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )

                    response = {
                        "status": "success",
                        "output": result.stdout.strip(),
                        "error": result.stderr.strip(),
                    }
                    self.send_response(200)

                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()

            except ValueError as ve:
                response = {"status": "error", "response": str(ve)}
                self.send_response(400)

            except Exception as e:
                response = {"status": "error", "response": f"Internal Server Error: {str(e)}"}
                self.send_response(500)

            finally:
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))


    def do_GET(self):
        if self.path == "/getconfigs":
            config_dir = "/var/lib/rancid/newRouters/configs"
            hostname_file = "/var/lib/rancid/newRouters/router_hostname.txt"  # Moved outside configs

            try:
                # Load hostname mappings
                hostname_map = {}
                if os.path.exists(hostname_file):
                    with open(hostname_file, "r") as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) == 2:
                                hostname_map[parts[0]] = parts[1]

                # Get config file list
                files = os.listdir(config_dir)

                file_data = [
                    {
                        "name": file,
                        "date": time.ctime(os.path.getmtime(os.path.join(config_dir, file))),
                        "hostname": hostname_map.get(file, file)  # Use alias if available
                    }
                    for file in files
                ]

                response = {
                    "status": "success",
                    "response": {"data": file_data}
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

                return  # ✅ Ensure function exits after response

            except Exception as e:
                error_response = {
                    "status": "error",
                    "message": str(e)
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode("utf-8"))

                return  # ✅ Ensure function exits after error response

        elif self.path == "/getrouter":
            config_dir = "/var/lib/rancid/newRouters/configs"
            hostname_file = "/var/lib/rancid/newRouters/router_hostname.txt"  # Persistent location

            try:
                # Load hostname mappings
                hostname_map = {}
                if os.path.exists(hostname_file):
                    with open(hostname_file, "r") as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) == 2:
                                hostname_map[parts[0]] = parts[1]

                # Get router files
                files = os.listdir(config_dir)

                # Attach hostname if available
                router_data = [
                    {"name": file, "hostname": hostname_map.get(file, file)} for file in files
                ]

                response = {
                    "status": "success",
                    "response": router_data
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return

            except Exception as e:
                error_response = {
                    "status": "error",
                    "message": str(e)
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode("utf-8"))
                return

        elif self.path.startswith("/get/"):
            param = self.path.split("/get/")[1]

            config_dir = "/var/lib/rancid/newRouters/configs"
            file_path = os.path.join(config_dir, param)

            try:
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        content = file.read()

                    response = {"status": "success", "response": content}
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                    return
                else:
                    response = {"status": "error", "response": "File not found"}
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                    return
            except Exception as e:
                response = {"status": "error", "response": str(e)}
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return

        
        elif self.path == "/checklogs":
            logs_dir = "/var/lib/rancid/logs"

            try:
                if os.path.isdir(logs_dir):
                    files = os.listdir(logs_dir)
                    log_details = []

                    for file in files:
                        file_path = os.path.join(logs_dir, file)
                        if os.path.isfile(file_path):
                            file_time = os.path.getmtime(file_path)  # Get last modified time
                            formatted_time = time.ctime(file_time)  # Format as "Tue Feb 25 16:10:05 2025"

                            log_details.append({"name": file, "date": formatted_time})

                    response = {"status": "success", "response": log_details}
                    self.send_response(200)
                    return
                
                else:
                    response = {"status": "error", "response": "Logs directory not found"}
                    self.send_response(404)
                    return

            except Exception as e:
                response = {"status": "error", "response": str(e)}
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return


        elif self.path.startswith("/log/"):
            log_file = self.path.split("/log/")[1]
            logs_dir = "/var/lib/rancid/logs"
            file_path = os.path.join(logs_dir, log_file)

            print(f"Attempting to read file: {file_path}")

            try:
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        content = file.read()

                    response = {
                        "status": "success",
                        "response": content
                    }

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                    return

                else:
                    response = {
                        "status": "error",
                        "response": f"File not found: {file_path}"
                    }
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                    return

            except Exception as e:
                response = {
                    "status": "error",
                    "response": f"An error occurred: {str(e)}"
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return
        
        elif self.path.startswith("/rlog/"):
            param = self.path.split("/rlog/")[1]

            config_dir = "/var/lib/rancid/newRouters/configs"
            file_path = os.path.join(config_dir, param)

            try:
                if os.path.isfile(file_path):
                    result = subprocess.run(
                        ["cvs", "log", file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )

                    if result.returncode == 0:
                        response = {"status": "success", "response": result.stdout}
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.add_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode("utf-8"))
                        return
                    else:
                        response = {"status": "error", "response": result.stderr}
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.add_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode("utf-8"))
                        return
                else:
                    response = {"status": "error", "response": "File not found"}
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                    return
                
            except Exception as e:
                response = {"status": "error", "response": str(e)}
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return

        else:
            self.send_response(404)
            self.add_cors_headers()
            self.end_headers()
            return

    def do_OPTIONS(self):
        """Handle CORS preflight request"""
        self.send_response(200)
        self.add_cors_headers()
        self.end_headers()


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, ConfigHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()
