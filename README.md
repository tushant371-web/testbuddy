# FastAPI Claude Sonnet 4 Application

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials (one of):
   - AWS CLI: `aws configure`
   - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - IAM role (if running on EC2)

3. Run the application:
```bash
python main.py
```

## Usage

### General Chat
Send POST request to `http://localhost:8000/chat`:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?"}'
```

### QA Test Plan Generation
Send POST request to `http://localhost:8000/test-plan`:

**Single document:**
```bash
curl -X POST "http://localhost:8000/test-plan" \
     -H "Content-Type: application/json" \
     -d '{"feature_document": "User login feature with email and password authentication"}'
```

**Multiple texts:**
```bash
curl -X POST "http://localhost:8000/test-plan" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Login functionality", "Password reset feature"]}'
```

**Multiple documents:**
```bash
curl -X POST "http://localhost:8000/test-plan" \
     -H "Content-Type: application/json" \
     -d '{"documents": ["API spec document", "UI requirements document"]}'
```

**Mixed inputs:**
```bash
curl -X POST "http://localhost:8000/test-plan" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Additional requirements"], "documents": ["Main spec"], "feature_document": "Core feature"}'
```