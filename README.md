# Analytics-Event-Analyser

This project provides its users to functionality to automate
the testing of analytics events.

## Setting up

This project currently uses python 3.11 along with dependencies
mentioned in requirement.txt

You can set up this project on your local machine by using the
following steps:

1. Ensure that you have python 3.11 installed. You can use
a python installer to [install python](https://www.python.org/ftp/python/3.11.5/python-3.11.5-macos11.pkg).
Check the installation by testing the following command
```shell
python3 --version
```
2. Clone this project into your machine 
```shell
git clone 
```
3. Separate this project from global python environment.
This can be done by creating a virtual environment in the project
directory.
```shell
python3 -m venv venv
```
4. Start the virtual environment by the following command in the project
directory for macOS.
```shell
source myvenv/bin/activate
```
5. Install the dependencies by using the following command
```shell
pip3 install -r requirements.txt
```
6. Shutdown the virtual environment after completion by using
```shell
deactivate
```

## Executing the project

Once all the requirements have been met and virtual environment
is active you can simply run
```shell
python3 analytics-event-analyser/main.py
```

## References

1. https://www.python.org/
2. https://docs.mitmproxy.org/stable/
3. https://www.selenium.dev/

