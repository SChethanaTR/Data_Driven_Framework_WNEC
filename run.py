#!/bin/python3
# pylint: skip-file
import click
import urwid
import urwid.raw_display
from plugins.aws_secrets import pytest_configure
import pkg_resources
import configparser
import subprocess
import socket
import os
from pathlib import Path
from shutil import which
from time import sleep

root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"

# Change to the correct source directory
os.chdir(root_dir)

with open("requirements.txt", "r") as requirements_txt:
    requirements = requirements_txt.readlines()

# IP of host
ping = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ping.connect(("reuters.com", 80))
ip = ping.getsockname()[0]
ping.close()

# Save in an environment variable for later use
os.environ["IP"] = ip

# Are the python requirements installed?
try:
    pkg_resources.require(requirements)
except pkg_resources.DistributionNotFound:
    # A requirement is missing, proceed to install them
    print("Detected missing Python dependencies")
    print("Installing Python dependencies")

    # Installs the progress display library first
    subprocess.run(["pip3", "install", "tqdm", "-qqq"])

    # tqdm can only be imported after about one second
    sleep(1.5)

    from tqdm import tqdm

    for requirement in tqdm(requirements):
        subprocess.run(["pip3", "install", requirement, "-qqq"])

    print("Python dependencies installed")
except pkg_resources.VersionConflict:
    pass

# Only import after they were installed

if not which("aws"):
    print("Amazon CLI was not detected in the system")
    print("Downloading Amazon CLI")
    subprocess.run(
        [
            "curl",
            "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip",
            "-o",
            "awscliv2.zip",
        ]
    )
    print("Installing Amazon CLI")
    subprocess.run(["unzip", "awscliv2.zip"])
    subprocess.run(["sudo", "./aws/install"])
    subprocess.run(["rm", "-f", "awscliv2.zip"])
    subprocess.run(["rm", "-rf", "aws"])

# Check for boto and AWS configuration
if not (Path.home() / ".aws/credentials").exists():
    print("AWS Credentials are not set, please set them now")
    subprocess.run(["aws", "configure"])

# Load AWS Secrets values
pytest_configure()

# Gets all registered tags
pytest_config = configparser.ConfigParser()
pytest_config.read("pytest.ini")
tags = [tag for tag in pytest_config.get("pytest", "markers").strip().split("\n")]
# A list with only with tag names
tag_names = [tag.split(":")[0] for tag in tags]

tag_names.sort()


@click.command()
@click.option("--ui/--cli", default=True, show_default=True, help="Use Terminal UI or CLI")
@click.option(
    "--reportportal",
    "-r",
    show_default=True,
    is_flag=True,
    help="Send [or not] result to ReportPortal",
)
@click.option(
    "--verbose",
    "-v",
    show_default=False,
    is_flag=True,
    help="Show more of the fails stacktrace",
)
@click.option(
    "--tag",
    "-t",
    "only_tags",
    type=click.Choice([tag.split(":")[0] for tag in tags]),
    multiple=True,
    help="Tags to be executed (use one -t for each tag)",
)
@click.option(
    "--ignore-tag",
    "-i",
    "ignore_tags",
    type=click.Choice([tag.split(":")[0] for tag in tags]),
    multiple=True,
    help="Tags to be ignored (use one -i for each tag)",
)
@click.option(
    "--path",
    "-p",
    "path",
    default="tests/",
    show_default=True,
    type=click.Path(exists=True),
    help="Path of test(s)",
)
def main(ui, reportportal, verbose, only_tags, ignore_tags, path="tests/"):
    """WNE Client Backend automated tests run script"""
    command = ["python3", "-m", "pytest"]
    run = True

    if ui:
        # Default values
        reportportal = True
        verbose = False
        ignore_tags = []
        # Defaults with all tags enabled
        only_tags = tag_names

        blank = urwid.Divider()
        divider = urwid.AttrWrap(urwid.Divider("-", 1), "body")

        checkboxes = {
            "reportportal": "Send to Report Portal",
            "verbose": "Verbose/Show stacktrace (terminal output only, doesn't affect Report Portal)",
        }

        def changed_input(widget, new_value):
            """Handles an widget input from the interface (checkbox)

            Args:
                widget (obj): The urwid object changed
                new_value (any): The new value inputted
            """
            nonlocal reportportal, only_tags, ignore_tags, verbose, path

            if widget.label == checkboxes["reportportal"]:
                reportportal = new_value
            elif widget.label == checkboxes["verbose"]:
                verbose = new_value
            elif widget.label in tags:
                # Include or exclude a tag from the tests
                tag = widget.label.split(":")[0]

                if new_value and tag not in only_tags:
                    only_tags.append(tag)

                    if tag in ignore_tags:
                        ignore_tags.remove(tag)
                elif tag not in ignore_tags:
                    ignore_tags.append(tag)

                    if tag in only_tags:
                        only_tags.remove(tag)
            elif widget.label == "Path: ":
                path = new_value

        def unhandled_input(key):
            if key == "f8" or key == "q" or key == "esc":
                raise urwid.ExitMainLoop()

        def button_press(button):
            """Handles a button press

            Args:
                button (obj): The button that was pressed
            """
            label = button.get_label()
            frame.footer = urwid.AttrWrap(urwid.Text(["Pressed: ", label]), "header")

            if label == "Cancel" or label == "Run tests":
                nonlocal run

                run = label == "Run tests"

                raise urwid.ExitMainLoop()

        text_header = "[QA] WNE Client Backend Tests.  F8 or q exits."

        with open("assets/logo.txt", "r") as logo_file:
            logo = logo_file.read()

        instructions = [
            ("logo", "Thomson Reuters - Backend Tests"),
            " Edit options below to run tests.\n",
        ]
        buttons = ["Run tests", "Cancel"]

        # Main display, this is what is show to the user as "UI"
        listbox_content = [
            blank,
            urwid.Columns(
                [
                    urwid.Padding(urwid.Text(("logo", logo)), left=2, right=0, min_width=30),
                    urwid.Pile(
                        [
                            urwid.Text(instructions),
                            divider,
                            urwid.Text("Select/Unselect tags to be executed", "center"),
                        ]
                        + [
                            urwid.AttrWrap(
                                urwid.CheckBox(tag, True, on_state_change=changed_input),
                                "body",
                                "buttn",
                            )
                            for tag in tags
                        ]
                        + [
                            divider,
                            urwid.Text("Output options", "center"),
                            urwid.CheckBox(
                                checkboxes["reportportal"],
                                True,
                                on_state_change=changed_input,
                            ),
                            urwid.CheckBox(
                                checkboxes["verbose"],
                                False,
                                on_state_change=changed_input,
                            ),
                            divider,
                            urwid.Text(
                                "Where to search for tests (.py file or folder)",
                                "center",
                            ),
                            urwid.AttrWrap(urwid.Edit("Path: ", "tests/"), "body", "buttn"),
                        ]
                    ),
                ],
                3,
            ),
            blank,
            blank,
            urwid.Padding(
                urwid.GridFlow(
                    [
                        urwid.AttrWrap(urwid.Button(label, button_press), "buttn", "buttnf")
                        for label in buttons
                    ],
                    15,
                    3,
                    1,
                    "center",
                ),
                left=4,
                right=3,
                min_width=13,
            ),
            blank,
        ]

        header = urwid.AttrWrap(urwid.Text(text_header), "header")
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, "body"), header=header)

        palette = [
            ("body", "black", "light gray", "standout"),
            ("header", "", "", "", "black", "#f80"),
            ("important", "dark blue", "light gray", ("standout", "underline")),
            ("buttn", "", "", "", "black", "#fa0"),
            ("buttnf", "", "", "", "", "#a80"),
            ("logo", "", "", "", "#f80", "light gray"),
            # class, nil, nil, nil, fore, back
        ]

        screen = urwid.raw_display.Screen()

        loop = urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled_input)

        loop.screen.set_terminal_properties(colors=256)

        loop.run()

    # Format run command (from either UI or CLI)
    if run:
        if reportportal:
            command.append("--reportportal")

        if only_tags:
            if not ui:
                # Terminal sends these tags as a tuple, so a cast to list is necessary
                only_tags = list(only_tags)

            only_tags.sort()

            # If all tags were selected, don't need to add them to the command
            if tag_names != only_tags:
                # Combine all tags into one argument (tag-1 and tag-2 and tag-n)
                command.append(f'-m {" and ".join(only_tags)}')

        if ignore_tags:
            # Combine all tags into one argument (tag-1 and tag-2 and tag-n)
            ignore_tags = " and not ".join(ignore_tags)

            command.append(f"-m not {ignore_tags}")

        if verbose:
            command.append("-vv")
            command.append("-s")

        if path and len(path) > 1:
            command.append(path)

            if verbose:
                print(f'Command executed: > {" ".join(command)}')

        # Execute final compiled run command
        subprocess.run(command)


if "__main__" == __name__:
    main()
