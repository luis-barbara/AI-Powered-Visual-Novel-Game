import requests

# Define the prompt
prompt = "Lighthouse on a cliff overlooking the ocean"

# Send a request to the Craiyon API
response = requests.post(
    "https://api.craiyon.com/v3",
    json={"prompt": prompt}
)

# Check the response
if response.status_code == 200:
    images = response.json().get("images", [])
    for i, img_url in enumerate(images):
        img_data = requests.get(img_url).content
        with open(f"lighthouse_{i}.png", "wb") as file:
            file.write(img_data)
    print("Images generated and saved successfully!")
else:
    print(f"Error {response.status_code}: {response.text}")