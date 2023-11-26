import requests

def send_label(label, confidence):
    # URL to which you want to send the POST request
    url = "http://localhost:3000/api/image_detector"

    # Data to be sent in the POST request as JSON
    data = {"label": label, "confidence": confidence}

    # Making the POST request with JSON data
    response = requests.post(url, json=data)

    # Checking the response
    if response.status_code == 200:
        print("POST request successful!")
        # Extracting 'id' from the JSON response
        json_response = response.json()
        if 'id' in json_response:
            extracted_id = json_response['id']
            print("Extracted ID:", extracted_id)
            send_image(extracted_id, "20220520_155306.jpg")
        else:
            print("No 'id' found in the response JSON.")
    else:
        print("POST request failed with status code:", response.status_code)

    print("Response text:", response.text)

def send_image(id, image_path):
    # URL to which you want to send the POST request
    url = f"http://localhost:3000/api/image_detector/image/{str(id)}"

    with open(image_path, 'rb') as image_file:
        # Adding the image file to the request
        files = {'image': image_file}

        # Making the POST request with only the image file
        response = requests.put(url, files=files)

    # Checking the response
    if response.status_code == 200:
        print("POST request successful!")
    else:
        print("POST request failed with status code:", response.status_code)

    print("Response text:", response.text)
# Example usage
send_label("high_smoke", 0.9)
