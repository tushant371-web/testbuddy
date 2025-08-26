import boto3
import json

bedrock = boto3.client('bedrock', region_name='us-east-1')

try:
    response = bedrock.list_foundation_models()
    claude_models = [model for model in response['modelSummaries'] 
                    if 'claude' in model['modelId'].lower()]
    
    print("Available Claude models:")
    for model in claude_models:
        print(f"- {model['modelId']}")
        
except Exception as e:
    print(f"Error: {e}")
    print("\nTry these common Claude model IDs:")
    print("- anthropic.claude-3-sonnet-20240229-v1:0")
    print("- anthropic.claude-3-haiku-20240307-v1:0")
    print("- anthropic.claude-instant-v1")