import subprocess

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error in {script_name}:\n{result.stderr}")

def main():
    scripts = ['script1.py', 'script2.py', 'script3.py']
    
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
