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
