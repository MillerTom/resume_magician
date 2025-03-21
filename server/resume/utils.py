from django.conf import settings
import openai
import json
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account

import logging
logger = logging.getLogger(__name__)

# OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# Google API credentials
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]
SERVICE_ACCOUNT_FILE = settings.CREDENTIALS_PATH

# Authenticate with Google APIs
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
docs_service = build("docs", "v1", credentials=creds)
NEW_DOC_TITLE = "Thomas Miller Resume"
FOLDER_ID = "1ugwOnYG7X2_9ombrhbx_0BdFohuwanU9"


def analyze_job(job_title, job_description):
    prompt = f"""
    You are an AI job filter that determines whether a job listing is technical.

    **Predefined Technical Roles**:
    Engineer, Developer, Scripter, Shell, Programmer, Analyst, DevOps, QA, Architect, Technical Manager, CTO, Load Tester, Cloud Architect, Entrepreneur, Coder, Guru.

    **Rules**:
    - The job **title** or **description** must contain relevant technical terms.
    - The job must be **technical**, avoiding recruiter, financial analyst, or insurance sales roles.

    **Job Listing**:
    - **Title**: {job_title}
    - **Description**: {job_description}

    **AI Response Format (JSON)**:
    {{
        "JobIsQualified": "QUALIFIED" or "NOT_QUALIFIED",
        "Analysis": "A brief reason for the classification."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )

    result = response.choices[0].message.content

    try:
        result = json.loads(result)
        is_qualified = result['JobIsQualified'] == "QUALIFIED"
        return is_qualified
    except Exception as err:
        logger.error(f"analyze_job error: {str(err)}")
        return False


def determine_base_resume(thread_id, job_title, job_description):
    prompt = f"""
    This system is designed for Thomas Miller, who has multiple targeted resumes. Each resume focuses on a specific primary skill, such as Java, Python, etc. Thomas has at least ten targeted resumes, known as "Base Resumes," and sometimes up to twenty. These resumes reflect 24 years of experience and are stored in the Vector Store.

    Given the job title and job description below, select the most appropriate "Base Resume" to use for the application.

    Job Title: {job_title}
    ==Job Description==
    {job_description}
    === end job description===

    Return JSON with the following elements:

    1) *BaseResumeFilename* – The filename in the Vector Store that best matches the provided job title and job description.

    2) *Confidence* – A "Confidence Score" indicating how well the selected resume aligns with the job description.

    3) *Keywords* – A concise list of relevant technical keywords, technologies, and industry jargon, separated by the | character.

    4) *KeywordsExtended* – Go beyond the initial keyword list! Extract all relevant technical terms, jargon, programming languages, frameworks, and concepts related to the job description. Prioritize "quantity over quality."

    5) *ExperienceGenerated* – Generate a brief paragraph summarizing relevant experience based on the technical and general requirements from the job description. Follow these guidelines:
    - Do *not* use bullet points.
    - Do *not* use the word "I."
    - Maintain an "extreme brevity" writing style to match the format of the Base Resumes.
    - Start the paragraph with: "Followed industry best practices to ensure high-quality project deliverables."
    - Incorporate all technical terms from the *Keywords* section.
    - Include at least three additional skills or capabilities that align with the job description but are not explicitly mentioned in it, to showcase added value.
    - The tone should reflect the expertise of a *senior developer, engineer, or architect*.
    - Do *not* state that Thomas has a computer science degree (he does not).
    - Certifications are not relevant for this section.
    - Ignore mentions of benefits in the job description.
    - Use logical reasoning to tailor the paragraph to highlight the strongest match for the job requirements.

    6) *JobTitle* – Generate a job title that closely resembles, but is *not an exact copy of*, the one provided in the job description. By default, include "Senior" unless the role specifically targets mid-level candidates.
    """
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=settings.ASSISTANT_ID
    )

    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(2)

    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            print("========================", msg.content[0].text.value)
            result = msg.content[0].text.value.replace('json', '').replace('`', '')
            result = json.loads(result)
            return result

    return None


def create_new_doc(template_doc_id, title, experience):
    logger.info(f"Start creating new Resume based on {template_doc_id}")
    copy = drive_service.files().copy(
        fileId=template_doc_id,
        body={
            "name": NEW_DOC_TITLE,
            "parents": [FOLDER_ID]
        }
    ).execute()
    new_doc_id = copy["id"]

    requests = [
        {"replaceAllText": {"containsText": {"text": "{{Title}}"}, "replaceText": title}},
        {"replaceAllText": {"containsText": {"text": "{{experience}}"}, "replaceText": experience}}
    ]
    
    docs_service.documents().batchUpdate(documentId=new_doc_id, body={"requests": requests}).execute()

    logger.info(f"New resume: https://docs.google.com/document/d/{new_doc_id}/edit")

    return f'https://docs.google.com/document/d/{new_doc_id}/edit'