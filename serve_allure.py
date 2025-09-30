import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

def serve_allure_report(report_dir, port=8080):
    """Serve the Allure report using Python's HTTP server."""
    if not os.path.exists(report_dir):
        print(f"Error: The directory '{report_dir}' does not exist.")
        return

    # Change the working directory to the Allure report directory
    os.chdir(report_dir)

    # Start the HTTP server
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving Allure report at http://localhost:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

# Example usage
if __name__ == "__main__":
    allure_report_dir = "/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/allure-report"
    serve_allure_report(allure_report_dir, port=8080)