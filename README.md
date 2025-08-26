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

3. Run the Streamlit UI:
```bash
streamlit run streamlit_app.py
```

4. (Optional) Run the FastAPI backend for API access:
```bash
python main.py
```

## Usage

### Streamlit Web UI
Access the beautiful web interface at `http://localhost:8501` after running the Streamlit app:

- **Feature Document**: Enter your main feature document or requirement
- **Additional Text Requirements**: Add multiple text-based requirements using the ➕ button
- **Document Specifications**: Add multiple document specifications using the ➕ button
- **Generate Test Plan**: Click to generate comprehensive test plans with technical tests and UAT cases

The UI will display:
- **Technical Test Types**: Unit, Integration, UI, API, E2E, Performance, Security, Database, Contract, and Smoke tests
- **UAT Test Cases**: Business requirement validation test cases with detailed steps

### API Endpoints

#### General Chat
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