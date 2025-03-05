import subprocess

def run_shell_scripts_and_python():
    # Run the first shell script using ./ 
    print("Running script 1...")
    subprocess.run(["./run_translate.sh"], check=True, shell=True)

    # Run the second shell script using ./ 
    print("Running script 2...")
    subprocess.run(["./run_hift.sh"], check=True, shell=True)

    # Run the Python script
    print("Running Python script...")
    subprocess.run(["python", "replace_audio.py"], check=True)

if __name__ == "__main__":
    run_shell_scripts_and_python()

