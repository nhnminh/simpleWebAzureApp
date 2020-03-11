import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, send_file, url_for
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure_helper import upload_file
import requests
# pprint is used to format the JSON response
from pprint import pprint

# all the API Keys are stored in a file named .env
load_dotenv()

# params for Azure Custom Vision
ENDPOINT = "https://westeurope.api.cognitive.microsoft.com/"
prediction_key = os.environ['AZURE_PREDICTION_KEY']
prediction_resource_id = os.environ['AZURE_PREDICTION_RESOURCE_ID']
projectid = os.environ['AZURE_PROJECT_ID']
publish_iteration_name = os.environ['AZURE_ITERATION_NAME']
url_prediction_api = os.environ['URL_PREDICTION_API']

# params for Azure storage
app = Flask(__name__, template_folder='template')
UPLOAD_FOLDER = "uploads"
container_name = "photos"
base_image_url = "https://assetsmanagementse.blob.core.windows.net"
connect_str = os.environ['AZURE_BLOB_CONNECTION_STR']

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


@app.route('/')
def entry_point():
    return redirect(url_for("storage"))

@app.route("/storage")
def storage():
    contents = "Hello World!"
    len = 0
    return render_template('storage.html', contents=contents, len = len, url_img = "https://www.educadictos.com/wp-content/uploads/2018/08/Sin-t%C3%ADtulo-1.jpg")

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", blob_service_client, container_name)
        result = sendAPI(f.filename, url_prediction_api)
        print(result)
        return render_template('storage.html', contents=result, len = len(result), url_img = base_image_url + "/" + container_name + "/" + UPLOAD_FOLDER + "/" + f.filename )


def showPref(filenae):
        filename = request.args.get('filename')
        output = sendAPI(filename, url_prediction_api)
        return render_template('storage.html', contents=output)


def sendAPI(filename, url_prediction_api):
        # Build the header json for the request
        headers = {
        "Prediction-key": prediction_key
        } 
        # Build the data json for the request
        data = {"Url": base_image_url + "/" + container_name + "/" + UPLOAD_FOLDER + "/" + filename }
        # Build and send a POST request
        response = requests.post(url_prediction_api, headers=headers, data=data)
        response = response.json()
        print(response)
        result = []
        if 'project' in response:    
            for pred in response['predictions']:
                result.append("class: {}, probability: {}".format(pred['tagName'], pred['probability']))
                print("class: {}, probability: {}".format(pred['tagName'], pred['probability']))
        else:
            result = response
            print(response)

        return result


if __name__ == '__main__':
    app.run(debug=True)