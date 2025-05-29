import os
import subprocess
import sys

def run_test(file_path):
    print(f"\n{'='*50}")
    print(f"Running test: {os.path.basename(file_path)}")
    print(f"{'='*50}\n")
    
    try:
        # Run the test with -ast flag
        result = subprocess.run(['python', 'rpal.py', file_path, '-ast'], 
                              capture_output=True, 
                              text=True)
        
        # Print the output
        print(result.stdout)
        
        # Print any errors
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error running {file_path}: {str(e)}")

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the Inputs directory
    inputs_dir = os.path.join(script_dir, 'Inputs')
    
    # Get all .txt files in the Inputs directory
    test_files = [f for f in os.listdir(inputs_dir) if f.endswith('.txt')]
    
    # Sort the files to run them in order
    test_files.sort()
    
    # Run each test file
    for test_file in test_files:
        file_path = os.path.join(inputs_dir, test_file)
        run_test(file_path)

if __name__ == "__main__":
    main() 