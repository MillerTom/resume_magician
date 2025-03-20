from django.core.management.base import BaseCommand
from resume.utils import determine_keyword

job_title = "PICK /Universe Developer (GC & Citizens)"
job_description = """
*Job Description:*

*Role: Pick Database Developer*

*Location: Federal Way, WA (Remote)*

*Job Mode : Full Time *



*Key Responsibilities:*
* Ensure reliable system availability and performance including incident and problem management
* Administer system objects and files to achieve optimum utilization
* Define and implement event triggers that will alert on potential system performance or integrity issues
* Perform system housekeeping, such as tuning, archiving, indexing, etc.
* Monitor usage, transaction volumes, response times, concurrency levels, etc.
* Work with support team to facilitate root cause analysis and timely resolution of system issues
* Recommend new features or changes to functionality based on performance logs, incident resolution or user feedback
* Design, develop, test and install software solutions that meet defined requirements
* Participate in cross functional projects and assist team to ensure projects are completed on-time and in-scope
* Will perform other duties as assigned,

*Skills & Qualifications:*

*Education:*
* 5+ years of professional software development experience.
* Bachelor's in Computer Science, related technical discipline or equivalent work experience.
* Prior transportation experience is preferred, LTL trucking very nice to have.

Job Type: Full-time

Pay: $90,000.00 - $100,000.00 per year

Schedule:
* Monday to Friday



Application Question(s):
* How many years of experience do you have working as a Universe Administrator & Developer?
* How many years of experience developing in PICK MultiValue databases?
* Do you have Prior transportation experience is preferred, LTL trucking? very nice to have
* Do you have Basic understanding on the below skills?
•	modern programming languages like Java, Python, etc.?
* Are you willing to work remotely (Federal Way, WA)?
* Provide Valid Email ID? *MUST
* Are you US Citizen OR GC Holder?
* Expected Salary Range for Full-Time Opportunity?
* What is the best time to reach you?

Work Location: Remote
"""

class Command(BaseCommand):
    help = 'Run Resume Maker'

    def handle(self, *args, **kwargs):
        keyword, google_doc_id = determine_keyword(job_title, job_description)
        print(keyword, google_doc_id)