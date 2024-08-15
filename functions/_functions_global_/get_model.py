import subprocess


def get_model_names():
    # Run 'ollama list' command and get the output
    output = subprocess.check_output("ollama list", shell=True).decode()

    # Split the output into lines and ignore the first line
    lines = output.split('\n')[2:]

    # Retrieve only model names
    model_names = [line.split()[0] for line in lines if line]

    return model_names