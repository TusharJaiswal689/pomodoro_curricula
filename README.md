# Pomodoro Curricula

A simple desktop Pomodoro timer built with Python and Tkinter.

## What it does

This app helps you stay focused by cycling through:

- 25 minutes of work
- 5 minutes of short break
- 20 minutes of long break after every 4 work sessions

It also shows progress with check marks and can send a push notification using ntfy when a long break ends.

## Features

- Clean timer interface
- Work and break cycle tracking
- Centered window layout
- Visual tomato countdown
- Notifications through ntfy

## Project files

- `main.py` - starts the app
- `pomodoro.py` - contains the timer logic and Tkinter UI
- `tomato.png` - image used for the timer display
- `.env` - optional environment variables such as your ntfy topic

## Requirements

- Python 3.8 or later
- Tkinter (usually included with Python)
- `python-dotenv`

Install the dependency:

```bash
pip install python-dotenv
```

## Setup

1. Open the project folder.
2. Make sure `tomato.png` is present in the root directory.
3. Create a `.env` file if you want push notifications:

```env
NTFY_TOPIC=your_topic_name
```

## Run the app

```bash
python main.py
```

## Notes

- If the `.env` file is missing or `NTFY_TOPIC` is not set, the app will still run normally without push notifications.
- The timer is designed as a lightweight personal productivity tool rather than a full-featured productivity dashboard.
