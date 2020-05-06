
# install python3
#install pip for python3

# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python3 get-pip.py

# pip3 install pipenv

#macosx :
# sudo brew install python pipenv

# create a project environment with python3
pipenv install --three
# activate project's environment 
pipenv shell
# install dependencies:
# - flask: http server
# - boto3: 
# - azure-storage-blob: azure blob service
# - azure-cognitiveservices-vision-customvision: 
pipenv install flask
pipenv install boto3
pipenv install python-dotenv

pipenv install azure-storage-blob
pipenv install azure-cognitiveservices-vision-customvision