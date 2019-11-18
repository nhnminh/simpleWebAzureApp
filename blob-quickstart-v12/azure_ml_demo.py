import os
import requests
# pprint is used to format the JSON response
from pprint import pprint




# Replace with a valid key
ENDPOINT = "https://westeurope.api.cognitive.microsoft.com/"
prediction_key = "7a90d11ea95f459f90a036311e77c873"
prediction_resource_id = "/subscriptions/3e6e9dd4-8cdd-4597-ab81-eedb735ec18f/resourceGroups/machinelearning/providers/Microsoft.CognitiveServices/accounts/resource_cv"
projectid = "298ee833-267d-4feb-bfe0-d28fb07bec17"
publish_iteration_name = "CPU_GPU"
base_image_url = "https://productphotosml.blob.core.windows.net/"
# trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# # Create a new project
# print ("Creating project...")
# project = trainer.create_project("My New Project")

# Now there is a trained endpoint that can be used to make a prediction

# Build the header json for the request
headers = {
    "Prediction-key": prediction_key
}

# Build the data json for the request
data = {"Url": base_image_url + "uploads/514534.jpg" }
url = "https://westeurope.api.cognitive.microsoft.com/customvision/v3.0/Prediction/298ee833-267d-4feb-bfe0-d28fb07bec17/classify/iterations/CPU_GPU/url"
# Build and send a POST request
response = requests.post(url, headers=headers, data=data)
response = response.json()

if 'project' in response:
    for pred in response['predictions']:
        print("class: {}, probability: {}".format(pred['tagName'], pred['probability']))
else:
    print(response)