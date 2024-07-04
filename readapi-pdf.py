import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient

# use your `key` and `endpoint` environment variables
key = "a262df977e6a4f9cb5ed2fc2245b9fe8"
endpoint = "https://docintelweat.cognitiveservices.azure.com"
storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=nparksblob01;AccountKey=5EK82zklSZMrJ5f0L6aPduZhQ5M1U44NzWXQCHIqFQt8LHhGoB4lPuhBrDBsjOHTnj7GGck3Eq37+ASt2BKRRg==;EndpointSuffix=core.windows.net"
container_name = "file"
blob_name = "IVE_KINGFISHER.pdf"

# formatting function
def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])


def analyze_read():
    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

    # Get a reference to the container
    container_client = blob_service_client.get_container_client(container_name)

    # Read the file into a variable
    with open("IVE_KINGFISHER.pdf", "rb") as file:
        file_data = file.read()

    # Download the blob to a local file using the file variable
    local_file_path = "IVE_KINGFISHER.pdf"
    with open(local_file_path, "wb") as local_file:
        local_file.write(file_data)

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(local_file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", document=f, locale="en-US"
        )

    result = poller.result()

    print("Document contains content: ", result.content)

    print("----------------------------------------")


if __name__ == "__main__":
    analyze_read()
