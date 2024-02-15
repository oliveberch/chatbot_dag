from google.cloud import aiplatform
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

# prediction using model endpoint
def predict_text_classification_single_label_sample(
    project, location, endpoint, content, service_account_key_path
):
    try:
        aiplatform.init(
            project=project,
            location=location,
            credentials=ServiceAccountCredentials.from_json_keyfile_name(service_account_key_path),
        )

        endpoint = aiplatform.Endpoint(endpoint)

        response = endpoint.predict(instances=[{"content": content}], parameters={})

        for prediction_ in response.predictions:
            print(prediction_)

    except Exception as e:
        print(f"An error occurred: {e}")



def classifier(user_input):
    project = "theta-cell-406519"
    location = "us-central1"
    endpoint = "398667523068788736"
    content = user_input
    service_account_key_path = "main/theta-cell-406519-112ac0726a30.json"

    predictions = predict_text_classification_single_label_sample(project, location, endpoint, content, service_account_key_path)

    category = predictions[0].confidence, key=lambda x:x[1]
    return category

def test_classifier(user_input):
    return "service"