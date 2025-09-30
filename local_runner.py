# # # import shutil
# # # import subprocess
# # # import os
# # # import sys
# # # from helpers import ubuntu
# # # from plugins.aws_secrets import pytest_configure
# # #
# # # # Set up environment
# # # root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
# # # os.chdir(root_dir)
# # # pytest_configure()
# # #
# # # import env
# # #
# # # os.environ["IP"] = env.ip
# # # ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
# # # ubuntu.setup_aws_cli(ssh, env.password)
# # # ssh.close()
# # #
# # # # Create temp Directory to save temporary files
# # # if not os.path.exists(env.temp_dir):
# # #     os.mkdir(env.temp_dir)
# # #
# # #
# # # def main():
# # #     """WNE Client Backend automated tests run script"""
# # #     # Update the path to the specific test function
# # #     path = "tests/Automation_tests/test_VFD.py::test_distribute_with_Service_code"
# # #
# # #     # Define the Allure results directory
# # #     allure_results_dir = os.path.join(env.temp_dir, 'allure-results')
# # #     allure_report_dir = os.path.join(env.temp_dir, 'allure-report')
# # #
# # #     # Ensure the Allure results directory exists
# # #     os.makedirs(allure_results_dir, exist_ok=True)
# # #
# # #     # Define the pytest command
# # #     command = [
# # #         sys.executable,
# # #         "-m",
# # #         "pytest",
# # #         "--headed",
# # #         "--browser-channel",
# # #         "chrome",
# # #         path,
# # #         "--reportportal",
# # #         "--alluredir", allure_results_dir  # Generate Allure results
# # #     ]
# # #     print(f'Command executed: > {" ".join(command)}')
# # #
# # #     # Execute the pytest command
# # #     result = subprocess.run(command)
# # #     if result.returncode != 0:
# # #         print("Pytest execution failed. Check the test script or configuration.")
# # #         return
# # #
# # #     # Generate the Allure report
# # #     generate_command = [
# # #         "allure",
# # #         "generate",
# # #         allure_results_dir,
# # #         "--clean",
# # #         "-o",
# # #         allure_report_dir
# # #     ]
# # #     print(f'Generating Allure report: > {" ".join(generate_command)}')
# # #     result = subprocess.run(generate_command)
# # #     if result.returncode != 0:
# # #         print("Allure report generation failed. Check the Allure installation or results directory.")
# # #         return
# # #
# # #     # Serve the Allure report and open it in the browser
# # #     serve_command = [
# # #         "allure",
# # #         "open",
# # #         allure_report_dir
# # #     ]
# # #     print(f'Serving Allure report: > {" ".join(serve_command)}')
# # #     subprocess.run(serve_command)
# # #
# # #
# # # if "__main__" == __name__:
# # #     main()
# #
# # # import shutil
# # # import subprocess
# # # import os
# # # import sys
# # # from datetime import datetime
# # # from helpers import ubuntu
# # # from plugins.aws_secrets import pytest_configure
# # #
# # # # Set up environment
# # # root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
# # # os.chdir(root_dir)
# # # pytest_configure()
# # #
# # # import env
# # #
# # # os.environ["IP"] = env.ip
# # # ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
# # # ubuntu.setup_aws_cli(ssh, env.password)
# # # ssh.close()
# # #
# # # # Create temp Directory to save temporary files
# # # if not os.path.exists(env.temp_dir):
# # #     os.mkdir(env.temp_dir)
# # #
# # #
# # # def main():
# # #     """WNE Client Backend automated tests run script"""
# # #     # Update the path to the specific test function
# # #     path = "tests/Automation_tests/test_VFD.py::test_distribute_with_Service_code"
# # #
# # #     # Get the current date
# # #     current_date = datetime.now().strftime("%Y-%m-%d")
# # #
# # #     # Define the date-based directory
# # #     date_based_dir = os.path.join(env.temp_dir, current_date)
# # #     os.makedirs(date_based_dir, exist_ok=True)
# # #
# # #     # Define the Allure results and report directories
# # #     allure_results_dir = os.path.join(date_based_dir, 'allure-results')
# # #     allure_report_dir = os.path.join(date_based_dir, 'allure-report')
# # #
# # #     # Ensure the Allure results directory exists
# # #     os.makedirs(allure_results_dir, exist_ok=True)
# # #
# # #     # Define the pytest command
# # #     command = [
# # #         sys.executable,
# # #         "-m",
# # #         "pytest",
# # #         "--headed",
# # #         "--browser-channel",
# # #         "chrome",
# # #         path,
# # #         "--reportportal",
# # #         "--alluredir", allure_results_dir  # Generate Allure results
# # #     ]
# # #     print(f'Command executed: > {" ".join(command)}')
# # #
# # #     # Execute the pytest command
# # #     result = subprocess.run(command)
# # #     if result.returncode != 0:
# # #         print("Pytest execution failed. Check the test script or configuration.")
# # #         return
# # #
# # #     # Generate the Allure report
# # #     generate_command = [
# # #         "allure",
# # #         "generate",
# # #         allure_results_dir,
# # #         "--clean",
# # #         "-o",
# # #         allure_report_dir
# # #     ]
# # #     print(f'Generating Allure report: > {" ".join(generate_command)}')
# # #     result = subprocess.run(generate_command)
# # #     if result.returncode != 0:
# # #         print("Allure report generation failed. Check the Allure installation or results directory.")
# # #         return
# # #
# # #     # Serve the Allure report and open it in the browser
# # #     serve_command = [
# # #         "allure",
# # #         "open",
# # #         allure_report_dir
# # #     ]
# # #     print(f'Serving Allure report: > {" ".join(serve_command)}')
# # #     subprocess.run(serve_command)
# # #
# # #
# # # if "__main__" == __name__:
# # #     main()
# #
# #
# # import shutil
# # import subprocess
# # import os
# # import sys
# # from datetime import datetime
# # from helpers import ubuntu
# # from plugins.aws_secrets import pytest_configure
# #
# # # Set up environment
# # root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
# # os.chdir(root_dir)
# # pytest_configure()
# #
# # import env
# #
# # os.environ["IP"] = env.ip
# # ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
# # ubuntu.setup_aws_cli(ssh, env.password)
# # ssh.close()
# #
# # # Create temp Directory to save temporary files
# # if not os.path.exists(env.temp_dir):
# #     os.mkdir(env.temp_dir)
# #
# #
# # def main():
# #     """WNE Client Backend automated tests run script"""
# #     # Update the path to the root directory of your test scripts
# #     path = "tests/Automation_tests/test_User_management.py"
# #
# #     # Get the current date
# #     current_date = datetime.now().strftime("%Y-%m-%d")
# #
# #     # Define the date-based directory
# #     date_based_dir = os.path.join(env.temp_dir, current_date)
# #     os.makedirs(date_based_dir, exist_ok=True)
# #
# #     # Define the Allure results and report directories
# #     allure_results_dir = os.path.join(date_based_dir, 'allure-results')
# #     allure_report_dir = os.path.join(date_based_dir, 'allure-report')
# #
# #     # Ensure the Allure results directory exists
# #     os.makedirs(allure_results_dir, exist_ok=True)
# #
# #     # Define the pytest command to run all tests
# #     command = [
# #         sys.executable,
# #         "-m",
# #         "pytest",
# #         "--headed",
# #         "--browser-channel",
# #         "chrome",
# #         path,
# #         "--reportportal",
# #         "--alluredir", allure_results_dir,  # Generate Allure results
# #         "-v"  # Verbose output for debugging
# #     ]
# #     print(f'Command executed: > {" ".join(command)}')
# #
# #     # Execute the pytest command
# #     result = subprocess.run(command)
# #     if result.returncode != 0:
# #         print("Some tests failed. Proceeding to generate the Allure report.")
# #
# #     # Generate the Allure report
# #     generate_command = [
# #         "allure",
# #         "generate",
# #         allure_results_dir,
# #         "--clean",
# #         "-o",
# #         allure_report_dir
# #     ]
# #     print(f'Generating Allure report: > {" ".join(generate_command)}')
# #     result = subprocess.run(generate_command)
# #     if result.returncode != 0:
# #         print("Allure report generation failed. Check the Allure installation or results directory.")
# #         return
# #
# #     # Serve the Allure report and open it in the browser
# #     serve_command = [
# #         "allure",
# #         "open",
# #         allure_report_dir
# #     ]
# #     print(f'Serving Allure report: > {" ".join(serve_command)}')
# #     subprocess.run(serve_command)
# #
# #
# # if "__main__" == __name__:
# #     main()
#
# import shutil
# import subprocess
# import os
# import sys
# from datetime import datetime
# from helpers import ubuntu
# from plugins.aws_secrets import pytest_configure
#
# # Set up environment
# root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
# os.chdir(root_dir)
# pytest_configure()
#
# import env
#
# os.environ["IP"] = env.ip
# ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
# ubuntu.setup_aws_cli(ssh, env.password)
# ssh.close()
#
# # Create temp Directory to save temporary files
# if not os.path.exists(env.temp_dir):
#     os.mkdir(env.temp_dir)
#
#
# def main():
#     """WNE Client Backend automated tests run script"""
#     # Update the path to the root directory of your test scripts
#     path = "tests/Automation_tests"
#
#     # Get the current date and time
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     current_time = datetime.now().strftime("%H-%M-%S")
#
#     # Define the date-based directory with a timestamp
#     timestamped_dir = os.path.join(env.temp_dir, current_date, current_time)
#     os.makedirs(timestamped_dir, exist_ok=True)
#
#     # Define the Allure results and report directories
#     allure_results_dir = os.path.join(timestamped_dir, 'allure-results')
#     allure_report_dir = os.path.join(timestamped_dir, 'allure-report')
#
#     # Ensure the Allure results directory exists
#     os.makedirs(allure_results_dir, exist_ok=True)
#
#     # Define the pytest command to run all tests
#     command = [
#         sys.executable,
#         "-m",
#         "pytest",
#         "--headed",
#         "--browser-channel",
#         "chrome",
#         path,
#         "--reportportal",
#         "--alluredir", allure_results_dir,  # Generate Allure results
#         "-v"  # Verbose output for debugging
#     ]
#     print(f'Command executed: > {" ".join(command)}')
#
#     # Execute the pytest command
#     result = subprocess.run(command)
#     if result.returncode != 0:
#         print("Some tests failed. Proceeding to generate the Allure report.")
#
#     # Generate the Allure report
#     generate_command = [
#         "allure",
#         "generate",
#         allure_results_dir,
#         "--clean",
#         "-o",
#         allure_report_dir
#     ]
#     print(f'Generating Allure report: > {" ".join(generate_command)}')
#     result = subprocess.run(generate_command)
#     if result.returncode != 0:
#         print("Allure report generation failed. Check the Allure installation or results directory.")
#         return
#
#     # Serve the Allure report and open it in the browser
#     serve_command = [
#         "allure",
#         "open",
#         allure_report_dir
#     ]
#     print(f'Serving Allure report: > {" ".join(serve_command)}')
#     subprocess.run(serve_command)
#
#
# if "__main__" == __name__:
#     main()

#having the previous executed results
import shutil
import subprocess
import os
import sys
from datetime import datetime
from helpers import ubuntu
from plugins.aws_secrets import pytest_configure
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import argparse
import webbrowser
import threading


# Set up environment
root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
os.chdir(root_dir)
pytest_configure()

import env

os.environ["IP"] = env.ip
ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
ubuntu.setup_aws_cli(ssh, env.password)
ssh.close()

# Create temp Directory to save temporary files
if not os.path.exists(env.temp_dir):
    os.mkdir(env.temp_dir)

# Create a directory to store all test results
history_dir = os.path.join(env.temp_dir, "test_history")
if not os.path.exists(history_dir):
    os.mkdir(history_dir)

# Create a directory for the consolidated report
consolidated_dir = os.path.join(env.temp_dir, "consolidated_report")
if not os.path.exists(consolidated_dir):
    os.mkdir(consolidated_dir)

# Directory to store Allure history data
allure_history_dir = os.path.join(env.temp_dir, "allure-history")
if not os.path.exists(allure_history_dir):
    os.mkdir(allure_history_dir)

# File to store metadata about test runs
history_index_file = os.path.join(history_dir, "history_index.json")


def save_test_metadata(timestamp_dir, test_path, result_code):
    """Save metadata about the test run to the history index automatically"""
    # Extract meaningful information from the test path
    test_name = os.path.basename(test_path.split("::")[0])
    if "::" in test_path:
        test_function = test_path.split("::")[-1]
        description = f"Test: {test_name} - Function: {test_function}"
    else:
        description = f"Test: {test_name}"

    if result_code == 0:
        status = "PASSED"
    else:
        status = "FAILED"

    metadata = {
        "timestamp": datetime.now().isoformat(),
        "directory": timestamp_dir,
        "description": description,
        "test_path": test_path,
        "status": status,
        "result_code": result_code
    }

    # Load existing history or create new
    if os.path.exists(history_index_file):
        with open(history_index_file, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    # Add new entry
    history.append(metadata)

    # Save updated history
    with open(history_index_file, 'w') as f:
        json.dump(history, f, indent=2)

    return metadata


def get_test_history():
    """Get all available test runs"""
    if os.path.exists(history_index_file):
        with open(history_index_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []


def copy_history_for_allure(allure_results_dir):
    """Copy history data to the new results directory to enable Allure trends"""
    # Create history directory in allure results if it doesn't exist
    target_history_dir = os.path.join(allure_results_dir, "history")
    if not os.path.exists(target_history_dir):
        os.makedirs(target_history_dir)

    # Copy existing history files to the new results directory
    if os.path.exists(allure_history_dir) and os.path.isdir(allure_history_dir):
        for history_file in os.listdir(allure_history_dir):
            src_file = os.path.join(allure_history_dir, history_file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, target_history_dir)

    return allure_history_dir


def update_allure_history(allure_report_dir, history_dir):
    """Update the Allure history directory with the latest report history"""
    report_history_dir = os.path.join(allure_report_dir, "history")
    if os.path.exists(report_history_dir) and os.path.isdir(report_history_dir):
        # Create history directory if it doesn't exist
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

        # Copy all history files from the report to our history directory
        for history_file in os.listdir(report_history_dir):
            src_file = os.path.join(report_history_dir, history_file)
            dst_file = os.path.join(history_dir, history_file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)


def create_history_html(history, current_run):
    """Create an HTML page that shows test history and links to reports"""
    html_path = os.path.join(consolidated_dir, "index.html")

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Execution History</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .current { background-color: #e6f7ff; padding: 15px; border-left: 5px solid #1890ff; margin-bottom: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .passed { color: green; }
            .failed { color: red; }
            .unknown { color: gray; }
            .view-btn {
                background-color: #4CAF50;
                color: white;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                border-radius: 4px;
                cursor: pointer;
            }
            iframe { width: 100%; height: 800px; border: none; }
        </style>
    </head>
    <body>
        <h1>Test Execution History</h1>
    """

    # Add current run section
    if current_run:
        timestamp = datetime.fromisoformat(current_run.get("timestamp", datetime.now().isoformat())).strftime(
            "%Y-%m-%d %H:%M:%S")
        status = current_run.get("status", "UNKNOWN")
        status_class = "passed" if status == "PASSED" else "failed" if status == "FAILED" else "unknown"
        description = current_run.get("description", "Test execution")

        html_content += f"""
        <div class="current">
            <h2>Current Test Run</h2>
            <p><strong>Timestamp:</strong> {timestamp}</p>
            <p><strong>Test:</strong> {description}</p>
            <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
            <p><a class="view-btn" href="current/index.html" target="_blank">View Report</a></p>
        </div>
        <h2>Previous Test Runs</h2>
        """

    # Add history table
    html_content += """
    <table>
        <tr>
            <th>Date & Time</th>
            <th>Test</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
    """

    # Add rows for each test run (excluding current)
    for i, entry in enumerate(history):
        if current_run and entry.get("directory") == current_run.get("directory"):
            continue  # Skip current run in the history table

        # Handle missing fields with safe defaults
        try:
            timestamp = datetime.fromisoformat(entry.get("timestamp", "")).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            timestamp = "Unknown date"

        description = entry.get("description", "Test execution")
        status = entry.get("status", "UNKNOWN")
        status_class = "passed" if status == "PASSED" else "failed" if status == "FAILED" else "unknown"

        html_content += f"""
        <tr>
            <td>{timestamp}</td>
            <td>{description}</td>
            <td class="{status_class}">{status}</td>
            <td><a class="view-btn" href="history/{i}/index.html" target="_blank">View Report</a></td>
        </tr>
        """

    html_content += """
    </table>
    </body>
    </html>
    """

    with open(html_path, "w") as f:
        f.write(html_content)

    return html_path


def prepare_consolidated_report(current_run_dir):
    """Prepare a consolidated report with current and historical results"""
    # Clear the consolidated directory except for the history folder
    history_folder = os.path.join(consolidated_dir, "history")
    if os.path.exists(history_folder):
        for item in os.listdir(consolidated_dir):
            item_path = os.path.join(consolidated_dir, item)
            if item != "history" and os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif item != "history" and os.path.isfile(item_path):
                os.remove(item_path)
    else:
        os.makedirs(history_folder)

    # Create current report directory
    current_dir = os.path.join(consolidated_dir, "current")
    if os.path.exists(current_dir):
        shutil.rmtree(current_dir)

    # Copy the current report
    current_report = os.path.join(current_run_dir, "allure-report")
    shutil.copytree(current_report, current_dir)

    # Get test history
    history = get_test_history()

    # Find current run in history
    current_run = None
    for entry in history:
        if entry.get("directory") == current_run_dir:
            current_run = entry
            break

    # Copy historical reports to the history folder
    for i, entry in enumerate(history):
        if entry.get("directory") == current_run_dir:
            continue  # Skip current run

        report_dir = os.path.join(entry.get("directory", ""), "allure-report")
        if os.path.exists(report_dir):
            dest_dir = os.path.join(history_folder, str(i))
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(report_dir, dest_dir)

    # Create the HTML index page
    return create_history_html(history, current_run)


def serve_consolidated_report():
    """Serve the consolidated report with history"""
    os.chdir(consolidated_dir)
    port = 8080# Change the port if needed
    ip_address = "10.121.50.139"  # Hardcoded IP address

    print(f"Hosting consolidated report on http://{ip_address}:{port}")
    print("Press Ctrl+C to stop the server")

    # Open the report automatically in the browser
    url = f"http://{ip_address}:{port}"
    threading.Thread(target=lambda: webbrowser.open(url)).start()

    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")


def main():
    """WNE Client Backend automated tests run script"""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Run automated tests and manage Allure reports")
    parser.add_argument("--test-path",
                        default="tests/Automation_tests/test_admin_playout.py",
                        help="Path to the test file or function to run")

    args = parser.parse_args()

    # Get the test path from arguments
    test_path = args.test_path

    # Get the current date and time
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")

    # Define the date-based directory with a timestamp
    timestamped_dir = os.path.join(history_dir, f"{current_date}_{current_time}")
    os.makedirs(timestamped_dir, exist_ok=True)

    # Define the Allure results and report directories
    allure_results_dir = os.path.join(timestamped_dir, 'allure-results')
    allure_report_dir = os.path.join(timestamped_dir, 'allure-report')

    # Ensure the Allure results directory exists
    os.makedirs(allure_results_dir, exist_ok=True)

    # Copy history for Allure trend
    copy_history_for_allure(allure_results_dir)

    # Define the pytest command to run all tests
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--headed",
        "--browser-channel",
        "chrome",
        test_path,
        "--reportportal",
        "--alluredir", allure_results_dir,  # Generate Allure results
        "-v"  # Verbose output for debugging
    ]
    print(f'Command executed: > {" ".join(command)}')

    # Execute the pytest command
    result = subprocess.run(command)
    result_code = result.returncode

    if result_code != 0:
        print("Some tests failed. Proceeding to generate the Allure report.")

    # Generate the Allure report
    generate_command = [
        "allure",
        "generate",
        allure_results_dir,
        # "--clean",
        "-o",
        allure_report_dir
    ]
    print(f'Generating Allure report: > {" ".join(generate_command)}')
    result = subprocess.run(generate_command)
    if result.returncode != 0:
        print("Allure report generation failed. Check the Allure installation or results directory.")
        return

    # Update Allure history with the latest report data
    update_allure_history(allure_report_dir, allure_history_dir)

    # Save metadata about this test run automatically
    save_test_metadata(timestamped_dir, test_path, result_code)

    # Prepare the consolidated report with history
    print("Preparing consolidated report with history...")
    prepare_consolidated_report(timestamped_dir)

    # Host the consolidated report
    serve_consolidated_report()


if __name__ == "__main__":
    main()

