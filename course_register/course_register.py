import requests
import lxml.html
import smtplib
import getpass
import sys
from datetime import date, time, datetime


def parse_course_page(course_page_html):
    html = lxml.html.fromstring(course_page_html)
    sec_remain = html.xpath("//td[@class='dddefault']")

    try:
        can_register = (int(sec_remain[12].text_content().strip())) > 0
    except IndexError:
        raise IndexError("Index Error occurred when parsing HTML for remaining seats")

    return can_register


def check_course_cap(semester, subj, course, session, sess_id):
    """Sends a post request to minerva looking for the webpage corresponding to the course given."""
    courses_url = "https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse"
    data = "term_in=" + semester
    data += "&sel_subj=dummy&sel_subj=" + subj
    data += "&SEL_CRSE=" + course
    data += "&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View%20Sections"
    courses_cookies = {"SESSID": sess_id}
    resp = session.post(courses_url, data=data, cookies=courses_cookies)
    return parse_course_page(resp.content)


def attempt_register(semester, crn, session, sess_id):
    regis_url = "https://horizon.mcgill.ca/pban1/bwckcoms.P_AddFromSearch1"

    ##########################
    # CHANGE BELOW ACCORDINGLY
    if crn == "448":
        data = "term_in=201709&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&RSTS_IN=&assoc_term_in=201709&CRN_IN=443&start_date_in=09%2F05%2F2017&end_date_in=12%2F07%2F2017&SUBJ=MATH&CRSE=316&SEC=001&LEVL=Undergraduate&CRED=++++3.000&GMOD=Standard&TITLE=Complex+Variables.&MESG=DUMMY&RSTS_IN=&assoc_term_in=201709&CRN_IN=458&start_date_in=09%2F05%2F2017&end_date_in=12%2F07%2F2017&SUBJ=MATH&CRSE=423&SEC=001&LEVL=Undergraduate&CRED=++++3.000&GMOD=Standard&TITLE=Regression+and+Analysis+of+Variance.&MESG=DUMMY&RSTS_IN=&assoc_term_in=201709&CRN_IN=24015&start_date_in=09%2F05%2F2017&end_date_in=12%2F07%2F2017&SUBJ=MATH&CRSE=545&SEC=001&LEVL=Undergraduate&CRED=++++4.000&GMOD=Standard&TITLE=Introduction+to+Time+Series+Analysis.&RSTS_IN=RW&CRN_IN=448&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&RSTS_IN=RW&CRN_IN=&assoc_term_in=&start_date_in=&end_date_in=&regs_row=3&wait_row=0&add_row=10&REG_BTN=Submit+Changes"
    else:
        data = "assoc_term_in=dummy&crn=dummy&start_date_in=dummy&end_date_in=dummy&rsts=dummy&subj=dummy&crse=dummy&sec=dummy&levl=dummy&gmod=dummy&cred=dummy&title=dummy&mesg=dummy&regs_row=2&wait_row=0&add_row=10&rsts=&assoc_term_in=201801&crn=16181&start_date_in=01%2F08%2F2018&end_date_in=04%2F16%2F2018&subj=COMP&crse=535&sec=001&levl=Masters+%26+Grad+Dips+%26+Certs&gmod=Standard&cred=++++4.000&title=Computer+Networks+1.&mesg=DUMMY&rsts=&assoc_term_in=201801&crn=11797&start_date_in=01%2F08%2F2018&end_date_in=04%2F16%2F2018&subj=COMP&crse=547&sec=001&levl=Masters+%26+Grad+Dips+%26+Certs&gmod=Standard&cred=++++4.000&title=Cryptography+and+Data+Security.&mesg=DUMMY&TERM_IN=201801&sel_crn=dummy&assoc_term_in=dummy&ADD_BTN=dummy&sel_crn=17135+201801&assoc_term_in=201801&ADD_BTN=Register"
    ##########################

    courses_cookies = {"SESSID": sess_id}
    resp = session.post(regis_url, data=data, cookies=courses_cookies)

    # TODO Check if registration worked, raise error if it did not
    return True


def send_email(email, password, subject, message):
    smtp_obj = smtplib.SMTP("smtp.office365.com", 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()
    smtp_obj.login(email, password)
    smtp_obj.sendmail(email, email, "Subject: " + subject + "\n\n" + message)
    smtp_obj.quit()


def course_register(sem, subj, course, crn, email, password, session, sess_id):
    """Main function of the script. Checks if user can register for the course given, registers if possible and sends an appropriate email notification"""
    # TODO verify that user is not already registered for these courses
    script_date = date(2017, 2, 10)
    today = date.today()

    # Check if there is space in the course
    if check_course_cap(sem, subj, course, session, sess_id):
        # Register for the course
        if attempt_register(sem, crn, session, sess_id):
            send_email(email, password, "Successfully Registered For " + subj + " " + course,
                       "The script was able to register for " + subj + " " + course + "!!")
        else:
            send_email(email, password, "Unexpected Error for " + subj + " " + course + " Registration",
                       "There is a free spot in " + subj + " " + course + " but attempted registration was not successful. Go check it out manually!")
    else:
        # Send failure email if time is 2 days passed
        if (today - script_date).days % 2 == 0 and time(12, 00) <= datetime.now().time() <= time(12, 14):
            send_email(email, password, "Course Still Full",
                       "Could not register for " + subj + " " + course + " - the course is still full")

# NOTE: your McGill email/password and Minerva username/password must be the same in order for the script to work.
email = sys.argv[1]
password = sys.argv[2]

login = {
    "sid": email,
    "PIN": password
}

# Create Session object
session = requests.session()

# Attempt to log in
login_url = "https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin"
cookies = {"TESTID": "set"}
r1 = session.post(login_url, data=login, cookies=cookies)

# TODO Minerva returns 200 even if login fails, need to check better for failed login
if r1.status_code != 200:
    raise Exception("Could not login, got error code")

# Attempt to register for courses
sess_id = r1.cookies.get("SESSID")

# CHANGE FIRST FOUR PARAMETERS BELOW ACCORDINGLY, AND ADD OR REMOVE MORE LINES
course_register("201709", "COMP", "550", "24378", email, password, session, sess_id)
course_register("201801", "COMP", "551", "17135", email, password, session, sess_id)
