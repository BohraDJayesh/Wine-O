import os
import time
import docker
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

UPLOAD_DIR = "/uploads"
LOG_DIR = "/logs"

client = docker.from_env()

class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        if not filename.lower().endswith((".exe", ".bin")):
            print(f" Skipping non-executable: {filename}")
            return

        print(f" New malware uploaded: {filename}")
        run_container(filename)

def run_container(filename):
    container_name = f"runner-{filename.replace('.', '-')}"
    malware_path = os.path.join(UPLOAD_DIR, filename)
    log_path = os.path.join(LOG_DIR, f"{filename}.log")

    try:
        print(f" Launching disposable container: {container_name}")
        logs = client.containers.run(
            image="wineo-runner",
            name=container_name,
            volumes={
                UPLOAD_DIR: {"bind": "/malware", "mode": "ro"},
                LOG_DIR: {"bind": "/logs", "mode": "rw"},
            },
            command=[f"/malware/{filename}"],
            remove=True,
            stderr=True,
            stdout=True,
            detach=False
        )

        with open(log_path, "wb") as f:
            f.write(logs)
        print(f"Logs saved to: {log_path}")

    except Exception as e:
        print(f"Error running container: {e}")

def main():
    print("📡 Job Manager watching for malware...")
    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, UPLOAD_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

