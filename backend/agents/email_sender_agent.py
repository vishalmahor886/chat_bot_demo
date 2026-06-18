from langchain_core.tools import tool
from backend.tools.email_sender_tool import send_email

@tool
def email_sender(to_mail:str, subject:str, body:str):
    """
    use this to send email to the user
    """
    try:
        return send_email(to_mail, subject, body)
    except Exception as e:
        return f"Error sending email: {str(e)}"