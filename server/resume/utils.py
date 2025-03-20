from django.conf import settings
import openai
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from resume.models import BaseResume

# OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# Google API credentials
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]
SERVICE_ACCOUNT_FILE = "/media/mon/Data/Upwork/ApplyJobForever/server/main/credentials.json"

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
        print(f"analyze_job error: {str(err)}")
        return False


def determine_keyword(job_title, job_description):
    keywords = BaseResume.objects.values_list('keyword', flat='True')
    keywords_str = "\n".join(keywords)

    prompt = f"""
    Given the job title and job description below, choose the most relevant programming language or technology keyword from the list. The options are: Python, JavaScript, PHP, C++, Java, Ruby, SQL, HTML, CSS, and Go. Consider the skills, responsibilities, and tasks mentioned in the job description. Provide the most suitable keyword that aligns best with the job requirements.
    Job Title: {job_title}
    Job Description: {job_description}
    Possible Keywords:
    {keywords_str}

    **AI Response Format (JSON)**:
    {{
        "BestMatchedKeyword": "[Keyword from the list of Possible Keywords]"
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
        keyword = result["BestMatchedKeyword"]
        base_resume = BaseResume.objects.filter(keyword=keyword).first()
        return base_resume.keyword, base_resume.google_doc_id
    except Exception as err:
        print(f"determin_keyword error: {str(err)}")
        return None


def create_new_doc(template_doc_id, title, experience):
    print(f"Start creating new Resume based on {template_doc_id}")
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

    print(f"New document created: https://docs.google.com/document/d/{new_doc_id}/edit")

    return new_doc_id


# def get_recommend_resume():
#     vs_ODZUV1b8PfCctGDcL9Izt7Cp