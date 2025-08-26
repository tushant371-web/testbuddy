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

"""
Available Claude models:
- anthropic.claude-opus-4-1-20250805-v1:0
- anthropic.claude-instant-v1:2:100k
- anthropic.claude-instant-v1
- anthropic.claude-v2:0:18k
- anthropic.claude-v2:0:100k
- anthropic.claude-v2:1:18k
- anthropic.claude-v2:1:200k
- anthropic.claude-v2:1
- anthropic.claude-v2
- anthropic.claude-3-sonnet-20240229-v1:0:28k
- anthropic.claude-3-sonnet-20240229-v1:0:200k
- anthropic.claude-3-sonnet-20240229-v1:0
- anthropic.claude-3-haiku-20240307-v1:0:48k
- anthropic.claude-3-haiku-20240307-v1:0:200k
- anthropic.claude-3-haiku-20240307-v1:0
- anthropic.claude-3-opus-20240229-v1:0:12k
- anthropic.claude-3-opus-20240229-v1:0:28k
- anthropic.claude-3-opus-20240229-v1:0:200k
- anthropic.claude-3-opus-20240229-v1:0
- anthropic.claude-3-5-sonnet-20240620-v1:0
- anthropic.claude-3-5-sonnet-20241022-v2:0
- anthropic.claude-3-7-sonnet-20250219-v1:0
- anthropic.claude-3-5-haiku-20241022-v1:0
- anthropic.claude-opus-4-20250514-v1:0
- anthropic.claude-sonnet-4-20250514-v1:0
"""