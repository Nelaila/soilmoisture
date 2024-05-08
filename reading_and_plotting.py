import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    script1_thread = threading.Thread(target=run_script, args=("readSerialData.py",))
    script2_thread = threading.Thread(target=run_script, args=("plottingDash.py",))

    script1_thread.start()
    script2_thread.start()