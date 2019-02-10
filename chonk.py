import json
import boto3
import base64
import ast
def detect_labels(imageData,max_labels=10, min_confidence=90, region="eu-west-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"Bytes" : imageData
			},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']
	
def lambda_handler(event, context):
    image = base64.b64decode(event['body'])
    labels = detect_labels(image)
    hasCat = False
    for label in labels:
        print(label["Name"])
        if label["Name"] == "Cat":
            hasCat = True
    if hasCat:
        endpoint_name = 'chonker'
        runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='us-east-1')
        response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/x-image', Body=image)
        probs = response['Body'].read().decode()
        probs = ast.literal_eval(probs)
        map(float, probs)
        print(probs)
        max_value = max(probs)
        max_index = probs.index(max_value)
        fat_classes = ["A Fine Boi", "He Chonk", "A Heckin Chonk", "HEFTY CHONK", "MEGA CHONKER", "OH LAWD HE COMIN"]
        output = ""
        if max_index != 0:
            output = fat_classes[max_index]
        elif probs[0] > 0.5 and probs[1] > 0.1 and probs[2] > 0.1 and probs[3] > 0.1 and probs[4] > 0.1 and probs[5] > 0.1:
            output = fat_classes[5]
        elif probs[0] > 0.5 and probs[1] > 0.1 and probs[2] > 0.1 and probs[3] > 0.1 and probs[4] > 0.1:
            output = fat_classes[4]
        elif probs[0] > 0.5 and probs[1] > 0.1 and probs[2] > 0.1 and probs[3] > 0.1:
            output = fat_classes[3]
        elif probs[0] > 0.5 and probs[1] > 0.1 and probs[2] > 0.2:
            output = fat_classes[2]
        elif probs[0] > 0.5 and probs[1] > 0.25:
            output = fat_classes[1]
        elif probs[0] > 0.5:
            output = fat_classes[0]
        else:
            output = "No Cat found"
        return {
            "statusCode": 200,
            "body": output
        }
    else:
        return {
            "statusCode": 200,
            "body":"No Cat Found"
        }
