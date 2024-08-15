import io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import config

# Initialize the Azure Computer Vision client
endpoint = config.MY_DOCUMENTINTELLIGENCE_ENDPOINT
subscription_key = config.MY_DOCUMENTINTELLIGENCE_API_KEY
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def analyze_receipts(image_data):
    # Analyze the image using Azure AI
    analysis = computervision_client.read_in_stream(image_data, raw=True)
    
    # Get the operation location (URL with an ID at the end)
    operation_location = analysis.headers["Operation-Location"]
    
    # Take the ID from the URL
    operation_id = operation_location.split("/")[-1]
    
    # Call the "GET" API and wait for the results
    while True:
        result = computervision_client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break

    if result.status == OperationStatusCodes.succeeded:
        receipt_text = ""
        for text_result in result.analyze_result.read_results:
            for line in text_result.lines:
                receipt_text += line.text + "\n"
        return receipt_text
    else:
        return "Error processing receipt image"