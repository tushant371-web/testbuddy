from fastapi import FastAPI
import boto3
import json

app = FastAPI()

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

QA_PROMPT_TEMPLATE = """
    You are a QA specialist and test automation expert responsible for comprehensive test planning.

    A new feature/requirement or document has been provided that needs thorough testing coverage across multiple technical test types and UAT test cases.

    Feature Document:
    {input_document}

    Instructions:
    1. Analyze the provided feature document thoroughly
    2. Generate a comprehensive test plan focusing on technical test types including:
    - Unit Tests (individual component/function testing)
    - Integration Tests (component interaction testing)
    - UI Tests (user interface testing)
    - API Tests (endpoint and service testing)
    - End-to-End Tests (complete user workflow testing)
    - Performance Tests (load, stress, scalability testing)
    - Security Tests (vulnerability and penetration testing)
    - Database Tests (data integrity and CRUD operations)
    - Contract Tests (API contract validation)
    - Smoke Tests (basic functionality verification)
    3. Generate UAT (User Acceptance Test) cases that focus on business requirements validation
    4. For each test type, provide specific test cases with technical implementation details
    5. Include test frameworks, tools, and automation approaches
    6. Consider edge cases, error scenarios, and boundary conditions

    Return the response in this JSON format:
    {{
    "test_types": [
    {{
    "type": "string",
    "description": "string", 
    "test_cases": [
    {{
    "name": "string",
    "objective": "string",
    "prerequisites": ["string"],
    "implementation_steps": ["string"],
    "expected_results": "string"
    }}
    ]
    }}
    ],
    "uat_test_cases": [
    {{
    "test_case_id": "string",
    "test_case_name": "string",
    "test_objective": "string",
    "preconditions": "string",
    "test_steps": ["string"],
    "expected_result": "string",
    "actual_result": "string",
    "status": "string"
    }}
    ]
    }}
"""

@app.post("/chat")
async def chat(message: dict):
    prompt = message.get("prompt", "").strip()
    
    if not prompt:
        return {"error": "Prompt cannot be empty"}
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    return {"response": result['content'][0]['text']}

@app.post("/test-plan")
async def generate_test_plan(request: dict):
    # Handle multiple input types
    texts = request.get("texts", [])
    documents = request.get("documents", [])
    feature_document = request.get("feature_document", "")
    
    # Combine all inputs
    combined_input = []
    
    if feature_document:
        combined_input.append(feature_document)
    
    if texts:
        if isinstance(texts, list):
            combined_input.extend(texts)
        else:
            combined_input.append(texts)
    
    if documents:
        if isinstance(documents, list):
            combined_input.extend(documents)
        else:
            combined_input.append(documents)
    
    if not combined_input:
        return {"error": "At least one input (texts, documents, or feature_document) is required"}
    
    final_input = "\n\n".join(str(item) for item in combined_input)
    prompt = QA_PROMPT_TEMPLATE.format(input_document=final_input)
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    return {"test_plan": result['content'][0]['text']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)