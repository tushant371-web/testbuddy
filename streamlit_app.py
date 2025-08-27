import streamlit as st
import boto3
import json
from PyPDF2 import PdfReader
from docx import Document
import io

st.set_page_config(
    page_title="TestBuddy AI - Test Plan Generator",
    page_icon="🧪",
    layout="wide"
)

# Initialize AWS Bedrock client with error handling
@st.cache_resource
def get_bedrock_client():
    try:
        return boto3.client('bedrock-runtime', region_name='us-east-1')
    except Exception as e:
        st.error(f"AWS Credentials Error: {str(e)}")
        st.info("Please configure AWS credentials using one of these methods:")
        st.code("""1. AWS CLI: aws configure
                    2. Environment variables:
                    export AWS_ACCESS_KEY_ID=your_access_key
                    export AWS_SECRET_ACCESS_KEY=your_secret_key
                    3. IAM role (if running on EC2)"""
                )
        st.stop()
        return None

bedrock = get_bedrock_client()

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file based on file type"""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif uploaded_file.type == "text/plain":
            return str(uploaded_file.read(), "utf-8")
        
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        else:
            return "Unsupported file format"
    
    except Exception as e:
        return f"Error reading file: {str(e)}"

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
   - UAT Tests (User Acceptance Test cases for business requirements validation)
3. For each test type, provide specific test cases with technical implementation details
4. Include test frameworks, tools, and automation approaches
5. Consider edge cases, error scenarios, and boundary conditions

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
]
}}
"""

def log_debug(message, debug_container=None):
    """Log debug message to sidebar if debug mode is enabled"""
    if debug_container:
        debug_container.write(message)

def generate_test_plan(text_input="", document_texts=None, debug_container=None):
    log_debug("🔍 Starting test plan generation", debug_container)
    
    # Combine all inputs
    combined_input = []
    
    if text_input:
        combined_input.append(text_input)
        log_debug(f"🔍 Added text input ({len(text_input)} chars)", debug_container)
    
    if document_texts:
        combined_input.extend(document_texts)
        log_debug(f"🔍 Added {len(document_texts)} documents", debug_container)
    
    if not combined_input:
        log_debug("🔍 No input provided", debug_container)
        return {"error": "At least one input is required"}
    
    final_input = "\n\n".join(str(item) for item in combined_input)
    log_debug(f"🔍 Final input length: {len(final_input)} chars", debug_container)
    
    prompt = QA_PROMPT_TEMPLATE.format(input_document=final_input)
    log_debug(f"🔍 Prompt prepared ({len(prompt)} chars)", debug_container)
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": prompt}]
    }
    log_debug("🔍 Calling Bedrock API...", debug_container)
    
    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=json.dumps(body)
        )
        log_debug("🔍 Bedrock API call successful", debug_container)
        
        result = json.loads(response['body'].read())
        log_debug(f"🔍 Response parsed, content length: {len(result['content'][0]['text'])}", debug_container)
        return result['content'][0]['text']
    except Exception as e:
        log_debug(f"🔍 Bedrock API error: {str(e)}", debug_container)
        raise e

# Enhanced CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .test-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        transition: all 0.3s ease;
    }
    .test-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    .uat-card {
        background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%);
        border: 1px solid #d4edda;
        border-left: 5px solid #28a745;
    }
    .tech-card {
        background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);
        border: 1px solid #dee2e6;
        border-left: 5px solid #1f77b4;
    }
    .test-header {
        display: flex;
        align-items: center;
        border-bottom: 2px solid #f1f3f4;
    }
    .test-title {
        font-size: 18px;
        font-weight: 600;
        margin-left: 10px;
        color: #2c3e50;
    }
    .test-section {
        margin: 12px 0;
    }
    .test-section-title {
        font-weight: 600;
        color: #495057;
        margin-bottom: 8px;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .test-list {
        background-color: #f8f9fa;
        border-radius: 8px;
        margin: 8px 0;
    }
    .test-list-item {
        display: flex;
        align-items: flex-start;
        margin: 6px 0;
        padding: 4px 0;
    }
    .test-bullet {
        color: #6c757d;
        margin-right: 8px;
        margin-top: 2px;
    }
    .objective-text {
        background-color: #e3f2fd;
        border-radius: 6px;
        padding: 10px;
        margin: 8px 0;
        border-left: 3px solid #2196f3;
        font-style: italic;
        color: black;
    }
    .expected-result {
        background-color: #e8f5e8;
        border-radius: 6px;
        padding: 10px;
        margin: 8px 0;
        border-left: 3px solid #4caf50;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧪 TestBuddy AI - Test Plan Generator</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Generate comprehensive test plans with technical tests and UAT cases</p>', unsafe_allow_html=True)

# Sidebar for debug mode and logs
debug_mode = st.sidebar.checkbox("🐛 Debug Mode", help="Show detailed execution logs")
debug_container = None
if debug_mode:
    st.sidebar.markdown("### Debug Logs")
    debug_container = st.sidebar.container()

# Main input section
st.header("📝 Input Requirements")

# Single text input
text_input = st.text_area(
    "Text Requirements",
    placeholder="Enter your feature requirements, user stories, or specifications here...",
    height=150
)

# File upload section
st.subheader("📁 Upload Documents")
st.write("Upload PDF, TXT, DOC, or DOCX files containing requirements or specifications:")

uploaded_files = st.file_uploader(
    "Choose files",
    type=['pdf', 'txt', 'doc', 'docx'],
    accept_multiple_files=True,
    help="Supported formats: PDF, TXT, DOC, DOCX"
)

# Display uploaded files and extract text
document_texts = []
if uploaded_files:
    st.write(f"📄 {len(uploaded_files)} file(s) uploaded:")
    for uploaded_file in uploaded_files:
        with st.expander(f"📄 {uploaded_file.name}"):
            extracted_text = extract_text_from_file(uploaded_file)
            if extracted_text.startswith("Error") or extracted_text == "Unsupported file format":
                st.error(extracted_text)
            else:
                document_texts.append(extracted_text)
                st.text_area(
                    "Extracted Text Preview",
                    value=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                    height=100,
                    disabled=True
                )
                st.success(f"✅ Text extracted successfully ({len(extracted_text)} characters)")

# Initialize session state
if 'test_plan' not in st.session_state:
    st.session_state.test_plan = None
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = set()
if 'completed_tests' not in st.session_state:
    st.session_state.completed_tests = set()

# Callback function for checkbox changes
def on_checkbox_change(section_key, test_name, checkbox_key):
    st.session_state.expanded_sections.add(section_key)
    st.toast(f"✅ Test completed: {test_name}")

# Generate button
if st.button("🚀 Generate Test Plan", type="primary", use_container_width=True):
    # Prepare inputs
    text_input_clean = text_input.strip() if text_input.strip() else None
    
    if not text_input_clean and not document_texts:
        st.error("Please provide at least one input (text requirements or upload documents)")
    else:
        with st.spinner("Generating comprehensive test plan..."):
            try:
                test_plan_text = generate_test_plan(
                    text_input=text_input_clean or "",
                    document_texts=document_texts if document_texts else None,
                    debug_container=debug_container
                )
                
                if isinstance(test_plan_text, dict) and "error" in test_plan_text:
                    st.error(test_plan_text["error"])
                else:
                    try:
                        st.session_state.test_plan = json.loads(test_plan_text)
                    except json.JSONDecodeError:
                        st.session_state.test_plan = {"raw_text": test_plan_text}
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Display test plan if available
if st.session_state.test_plan:
    if "raw_text" in st.session_state.test_plan:
        st.header("📋 Generated Test Plan")
        st.text_area("Test Plan Output", st.session_state.test_plan["raw_text"], height=400)
    else:
        st.header("🎯 Test Plan Results")
        
        for test_type in st.session_state.test_plan.get("test_types", []):
            is_uat = test_type['type'].upper() == 'UAT TESTS' or 'UAT' in test_type['type'].upper()
            icon = "✅" if is_uat else "🔧"
            card_class = "uat-card" if is_uat else "tech-card"
            
            section_key = test_type['type']
            # Always expand if any test in this section is completed
            has_completed_tests = any(f"{section_key}_{j}" in st.session_state.completed_tests 
                                    for j in range(1, len(test_type.get('test_cases', [])) + 1))
            is_expanded = section_key in st.session_state.expanded_sections or has_completed_tests
            
            with st.expander(f"{icon} {test_type['type']}", expanded=is_expanded):
                st.markdown(f"**📋 Description:** {test_type['description']}")
                st.markdown("---")
                
                for i, test_case in enumerate(test_type.get('test_cases', []), 1):
                    col1, col2 = st.columns([0.05, 0.95])
                    
                    with col1:
                        checkbox_key = f"{test_type['type']}_{i}"
                        checkbox_value = st.checkbox(
                            "Complete", 
                            key=checkbox_key, 
                            label_visibility="collapsed",
                            on_change=on_checkbox_change,
                            args=(section_key, test_case['name'], checkbox_key)
                        )
                        
                        # Track completed tests
                        if checkbox_value:
                            st.session_state.completed_tests.add(checkbox_key)
                        elif checkbox_key in st.session_state.completed_tests:
                            st.session_state.completed_tests.remove(checkbox_key)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="test-card {card_class}">
                            <div class="test-header">
                                <span class="test-title">Test Case {i}: {test_case['name']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="objective-text">
                            <strong>🎯 Objective:</strong> {test_case['objective']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if test_case.get('prerequisites'):
                            st.markdown('<div class="test-section-title">📋 Prerequisites</div>', unsafe_allow_html=True)
                            st.markdown('<div class="test-list">', unsafe_allow_html=True)
                            for prereq in test_case['prerequisites']:
                                st.markdown(f"""
                                <div class="test-list-item">
                                    <span class="test-bullet">▶</span>
                                    <span>{prereq}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        if test_case.get('implementation_steps'):
                            st.markdown('<div class="test-section-title">⚙️ Implementation Steps</div>', unsafe_allow_html=True)
                            st.markdown('<div class="test-list">', unsafe_allow_html=True)
                            for step in test_case['implementation_steps']:
                                st.markdown(f"""
                                <div class="test-list-item">
                                    <span class="test-bullet">🔸</span>
                                    <span>{step}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="expected-result">
                            <strong>✅ Expected Results:</strong> {test_case['expected_results']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666; padding: 20px;'>TestBuddy AI - Powered by Claude Sonnet 4</div>", unsafe_allow_html=True)
