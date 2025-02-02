from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from module.line_notify import send_notify, check_internet_connection
import os, sys
import time

class FileCreateHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("Created: " + event.src_path)
        file_name = event.src_path.split("\\")[-1]
        while (not check_internet_connection()):
            pass
        if send_notify(event.src_path, file_name) != 200:
            send_notify("", f"Detect change in folder {event.src_path}.")
        time.sleep(5)


def file_monitoring(token, file_path):
    
    os.environ["line_token"] = token
    os.environ["file_path"] = file_path
    
    event_handler = FileCreateHandler()
    path = os.environ.get("file_path")
    print("Script monitor folder", path + "\\", "using token", os.environ["line_token"])
    # Create an observer.
    observer = Observer()

    # Attach the observer to the event handler.
    observer.schedule(event_handler, path, recursive=False)

    # Start the observer.
    observer.start()

    try:
        observer.run()
    finally:
        observer.stop()
        observer.join()
    return

if __name__ == "__main__":
   
    event_handler = FileCreateHandler()

    # Create an observer.
    observer = Observer()
    if len(sys.argv) == 3:
        os.environ["line_token"] = sys.argv[1]
        os.environ["file_path"] = sys.argv[2]
    else:
        print("Usage: python file_monitoring.py <line_token> <file_path>")
        sys.exit(1)

    linetoken = os.environ["line_token"]

    path = os.environ.get("file_path")
    print("Script monitor folder", path + "\\", "using token", os.environ["line_token"])
    # Attach the observer to the event handler.
    observer.schedule(event_handler, path, recursive=False)

    # Start the observer.
    observer.start()

    try:
        observer.run()
    finally:
        observer.stop()
        observer.join()