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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

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
                    # ✅ Execute `cvs diff` and return raw output
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
            # Directory containing RANCID configs
            config_dir = "/var/lib/rancid/newRouters/configs"

            try:
                # List all files in the directory with their modification time
                files = os.listdir(config_dir)

                # Prepare the response with file names and modification dates
                file_data = [
                    {
                        "name": file,
                        "date": time.ctime(os.path.getmtime(os.path.join(config_dir, file)))
                    }
                    for file in files
                ]

                response = {
                    "status": "success",
                    "response": {"data": file_data}
                }

                # Send response
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

            except Exception as e:
                # Handle errors
                error_response = {
                    "status": "error",
                    "message": str(e)
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode("utf-8"))

        elif self.path == "/getrouter":
            # Directory containing RANCID configs
            config_dir = "/var/lib/rancid/newRouters/configs"

            try:
                # List all files in the directory
                files = os.listdir(config_dir)

                # Prepare a JSON response
                response = {
                    "status": "success",
                    "response": files
                }

                # Send response
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                # Handle errors
                error_response = {
                    "status": "error",
                    "message": str(e)
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode("utf-8"))

        elif self.path.startswith("/get/"):
            # Extract the parameter (e.g., "10.10.0.2")
            param = self.path.split("/get/")[1]

            # Construct the file path
            config_dir = "/var/lib/rancid/newRouters/configs"
            file_path = os.path.join(config_dir, param)

            try:
                # Read the file if it exists
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        content = file.read()

                    # Send file content as JSON response
                    response = {"status": "success", "response": content}
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                else:
                    # File not found
                    response = {"status": "error", "response": "File not found"}
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                # Handle errors
                response = {"status": "error", "response": str(e)}
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

        
        elif self.path == "/checklogs":
            # Directory containing RANCID logs
            logs_dir = "/var/lib/rancid/logs"

            try:
                # List all files in the logs directory
                if os.path.isdir(logs_dir):
                    files = os.listdir(logs_dir)

                    # Prepare a successful response
                    response = {"status": "success", "response": files}
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                else:
                    # Directory not found
                    response = {"status": "error", "response": "Logs directory not found"}
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                # Handle errors
                response = {"status": "error", "response": str(e)}
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path.startswith("/log/"):
            log_file = self.path.split("/log/")[1]
            logs_dir = "/var/lib/rancid/logs"
            file_path = os.path.join(logs_dir, log_file)

            print(f"Attempting to read file: {file_path}")

            try:
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        content = file.read()

                    # Send the file content as a JSON response
                    response = {
                        "status": "success",
                        "response": content
                    }

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))

                else:
                    # File not found, include the file path in the response
                    response = {
                        "status": "error",
                        "response": f"File not found: {file_path}"
                    }
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))

            except Exception as e:
                # Handle other errors
                response = {
                    "status": "error",
                    "response": f"An error occurred: {str(e)}"
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
        
        elif self.path.startswith("/rlog/"):
            # Extract the parameter (e.g., "10.10.0.2")
            param = self.path.split("/rlog/")[1]

            # Construct the full file path
            config_dir = "/var/lib/rancid/newRouters/configs"
            file_path = os.path.join(config_dir, param)

            try:
                # Check if the file exists
                if os.path.isfile(file_path):
                    # Execute `cvs log` on the file
                    result = subprocess.run(
                        ["cvs", "log", file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )

                    if result.returncode == 0:
                        # Successfully retrieved the CVS log
                        response = {"status": "success", "response": result.stdout}
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.add_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode("utf-8"))
                    else:
                        # Error in `cvs log`
                        response = {"status": "error", "response": result.stderr}
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.add_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode("utf-8"))
                else:
                    # File not found
                    response = {"status": "error", "response": "File not found"}
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.add_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                # Handle any unexpected errors
                response = {"status": "error", "response": str(e)}
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.add_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

        else:
            # Return 404 for any other path
            self.send_response(404)
            self.add_cors_headers()
            self.end_headers()

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
