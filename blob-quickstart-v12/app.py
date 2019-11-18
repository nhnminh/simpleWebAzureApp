import os
from flask import Flask, render_template, request, redirect, send_file, url_for
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure_helper import upload_file
import requests
# pprint is used to format the JSON response
from pprint import pprint


# params for Azure Custom Vision
ENDPOINT = "https://westeurope.api.cognitive.microsoft.com/"
prediction_key = "7a90d11ea95f459f90a036311e77c873"
prediction_resource_id = "/subscriptions/3e6e9dd4-8cdd-4597-ab81-eedb735ec18f/resourceGroups/machinelearning/providers/Microsoft.CognitiveServices/accounts/resource_cv"
projectid = "298ee833-267d-4feb-bfe0-d28fb07bec17"
publish_iteration_name = "CPU_GPU"
base_image_url = "https://productphotosml.blob.core.windows.net/"
url_prediction_api = "https://westeurope.api.cognitive.microsoft.com/customvision/v3.0/Prediction/298ee833-267d-4feb-bfe0-d28fb07bec17/classify/iterations/CPU_GPU/url"

# params for Azure storage
app = Flask(__name__, template_folder='template')
UPLOAD_FOLDER = "uploads"
container_name = "photos"
url_pref = "https://productphotosml.blob.core.windows.net/"
FULL_URL = url_pref + container_name



# Retrieve the connection string for use with the application. The storage
# connection string is stored in an environment variable on the machine
# running the application called CONNECT_STR. If the environment variable is
# created after the application is launched in a console or with Visual Studio,
# the shell or application needs to be closed and reloaded to take the
# environment variable into account.

# Open cmd on windows, use this command to import connection_string on Windows :
# setx CONNECT_STR "<yourconnectionstring>"
connect_str = os.getenv('CONNECT_STR')
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


@app.route('/')
def entry_point():
    return redirect(url_for("storage"))

@app.route("/storage")
def storage():
    contents = "Hello World!"
    return render_template('storage.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", blob_service_client, container_name)
        output = sendAPI(f.filename, url_prediction_api)
        return render_template('storage.html', contents=output)


def showPref(filenae):
        filename = request.args.get('filename')
        output = sendAPI(filename, url_prediction_api)
        return render_template('storage.html', contents=output)


def sendAPI(filename, url_prediction_api):
    if request.method == 'GET':
        # Build the header json for the request
        headers = {
        "Prediction-key": prediction_key
        } 
        # Build the data json for the request
        data = {"Url": base_image_url + "uploads/" + filename }
        # Build and send a POST request
        response = requests.post(url_prediction_api, headers=headers, data=data)
        response = response.json()
        if 'project' in response:
            for pred in response['predictions']:
                result = "class: {}, probability: {}".format(pred['tagName'], pred['probability'])
                print("class: {}, probability: {}".format(pred['tagName'], pred['probability']))
        else:
            result = response
            print(response)

        return result


if __name__ == '__main__':
    app.run(debug=True)