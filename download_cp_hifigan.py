import zipfile
import requests

url = "https://huggingface.co/yl4579/HiFTNet/resolve/main/LJSpeech/cp_hifigan.zip"

output_file = "cp_hifigan.zip"

response = requests.get(url, timeout=50)

if response.status_code == 200:
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f"File successfully downloaded and saved to {output_file}")
else:
    print(f"Failed to download file. HTTP status code: {response.status_code}")

def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"File unzipped to {extract_to}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage
zip_file_path = 'cp_hifigan.zip'  # Replace with the path to your zip file
output_dir = '.'  # Replace with the directory you want to extract to (use '.' for the current directory)

unzip_file(zip_file_path, output_dir)
