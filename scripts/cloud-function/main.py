import os
import functions_framework
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

@functions_framework.http
def send_build_notification(request):
    """HTTP Cloud Function to send build notifications via email.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    
    if not request_json or 'to' not in request_json or 'message' not in request_json:
        return 'Invalid request', 400

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        
        from_email = Email("cloud-build@yourl.cloud")
        to_email = To(request_json['to'])
        subject = request_json['message']['subject']
        content = Content("text/plain", request_json['message']['body']['text'])
        
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        
        return f'Email sent successfully, status code: {response.status_code}', 200
    except Exception as e:
        return f'Error sending email: {str(e)}', 500
