from google.cloud import aiplatform
from google.oauth2 import service_account

# prediction using model endpoint
import os

# os.environ['GOOGLE_APPLICATION_CREDENTIALS']='gopika.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='azaan.json'

# credentials=service_account.Credentials.from_service_account_file('gopika.json')
# credentials=service_account.Credentials.from_service_account_file('azaan.json')

def predict_text_classification_single_label_sample(
    project, location, endpoint, content
):
    try:
        aiplatform.init(
            project=project,
            location=location
        )

        predictor = aiplatform.Endpoint(endpoint)

        result = predictor.predict(instances=[{"content": content}], parameters={})

        names=result[0][0]['displayNames'].copy()
        values=result[0][0]['confidences'].copy()
        print(names,values)
        max_index=values.index(max(values))

        print(names[max_index])

        '''names=result['displayNames'].copy()
        values=result['confidences'].copy()

        print(names,values)'''

    except Exception as e:
        print(f"An error occurred: {e}")


def classifier_gopika(user_input):
    project = "theta-cell-406519"
    location = "us-central1"
    endpoint = "398667523068788736"
    content = user_input
    # service_account_key_path = "./gopika.json"

    return predict_text_classification_single_label_sample(project, location, endpoint, content)

def classifier_azaan(user_input):
# try:
    project = "spherical-list-412116"
    location = "us-central1"
    endpoint = "4741826413714210816"
    content = user_input

    return predict_text_classification_single_label_sample(project, location, endpoint, content)
# except:
#     return 'General'
