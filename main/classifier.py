from google.cloud import aiplatform
from google.oauth2 import service_account
#from oauth2client.service_account import ServiceAccountCredentials

# prediction using model endpoint
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='theta-cell-406519-112ac0726a30.json'
credentials=service_account.Credentials.from_service_account_file('theta-cell-406519-112ac0726a30.json')
def predict_text_classification_single_label_sample(
    project, location, endpoint, content, service_account_key_path
):
    try:
        aiplatform.init(
            project=project,
            location=location,
            #credentials=ServiceAccountCredentials.from_json_keyfile_name(service_account_key_path),
        )

        predictor = aiplatform.Endpoint(endpoint)

        result = predictor.predict(instances=[{"content": content}], parameters={})

        names=result[0][0]['displayNames'].copy()
        values=result[0][0]['confidences'].copy()
        print(names,values)
        max_index=values.index(max(values))

        print(names[max_index])



        #print(type(result))

        '''names=result['displayNames'].copy()
        values=result['confidences'].copy()

        print(names,values)'''

    except Exception as e:
        print(f"An error occurred: {e}")



def classifier(user_input):
    project = "theta-cell-406519"
    location = "us-central1"
    endpoint = "398667523068788736"
    content = user_input
    service_account_key_path = "./theta-cell-406519-112ac0726a30.json"

    predict_text_classification_single_label_sample(project, location, endpoint, content, service_account_key_path)

classifier('hi. im having issue with login to my wifi device')