import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_general_email(email: str, message_text: str):
    
    # Credentials
    sender_email = 'adroituniversal@gmail.com'
    app_password = 'cslp clhh rtci ecbw'
    
    # ---------------------------------------------------------
    # HTML BODY
    # Note: In f-strings, CSS braces { } must be doubled {{ }} 
    # so Python knows they are text, not variables.
    # ---------------------------------------------------------
    body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Message from INTELLISMART</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        html, body {{ margin: 0 auto !important; padding: 0 !important; height: 100% !important; width: 100% !important; font-family: 'Poppins', sans-serif; background: linear-gradient(180deg, #fce4ec 0%, #fff0f5 100%); background-color: #fce4ec; }}
        * {{ -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; }}
        div[style*="margin: 16px 0"] {{ margin: 0 !important; }}
        table, td {{ mso-table-lspace: 0pt !important; mso-table-rspace: 0pt !important; }}
        table {{ border-spacing: 0 !important; border-collapse: collapse !important; table-layout: fixed !important; margin: 0 auto !important; }}
        .button-hover:hover {{ opacity: 0.9 !important; transform: scale(1.02); box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4) !important; }}
        @media screen and (max-width: 600px) {{
            .email-container {{ width: 100% !important; margin: auto !important; }}
            .pad-mobile {{ padding-left: 20px !important; padding-right: 20px !important; }}
            .h1-mobile {{ font-size: 22px !important; }}
        }}
    </style>
</head>
<body width="100%" style="margin: 0; padding: 0 !important; background-color: #fce4ec;">
    <center style="width: 100%; background: linear-gradient(180deg, #fce4ec 0%, #fff0f5 100%); background-color: #fce4ec;">
        
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
            Update from INTELLISMART  (Internship Project By Nawaz Sayyad).
        </div>

        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="margin: auto;" class="email-container">
            <tr>
                <td style="padding: 30px 0;"></td>
            </tr>
            <tr>
                <td style="background-color: #ffffff; border-radius: 20px; box-shadow: 0 15px 35px rgba(233, 30, 99, 0.15), 0 5px 15px rgba(0,0,0,0.05); border: 1px solid #fce4ec; overflow: hidden;">
                    
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 40px 20px 20px; text-align: center;">
                                <img src="https://cdn.blume.vc/blume/media/images/startups/lovelocal/logo/LoveLocal-B2C-01.f1670267319.png" alt="LoveLocal Logo" width="180" style="display: block; margin: 0 auto; max-width: 80%; height: auto;">
                            </td>
                        </tr>
                    </table>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td class="pad-mobile" style="padding: 10px 40px 30px 40px; text-align: center;">
                                <h2 class="h1-mobile" style="margin: 0 0 20px; font-size: 26px; font-weight: 700; color: #1a1a1a;">Hello!</h2>
                                
                                <p style="margin: 0 0 20px; font-size: 16px; line-height: 28px; color: #555555; text-align: left;">
                                    {message_text}
                                </p>

                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="padding: 0 40px 40px;">
                                <a href="https://lovelocal.adroitsdvc.in" class="button-hover" style="background: linear-gradient(135deg, #ec407a 0%, #c2185b 100%); border-radius: 50px; color: #ffffff; display: inline-block; font-family: 'Poppins', sans-serif; font-size: 16px; font-weight: 600; line-height: 54px; text-align: center; text-decoration: none; width: 240px; box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);">
                                    Visit LoveLocal
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #ffebee; border-top: 2px dashed #e57373; padding: 25px 30px; text-align: center;">
                                <p style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 13px; color: #b71c1c; line-height: 1.6;">
                                    <strong>⚠️ PROJECT DISCLAIMER:</strong><br>
                                    This is <strong>NOT A REAL ORDER</strong>. This is a simulation created as an <strong>Internship Project by Nawaz Sayyad</strong> (Student).<br><br>
                                    This design is a demonstration proposed for LoveLocal to showcase how an order confirmation could look if developed. Nawaz Sayyad does not claim any rights on the LoveLocal brand or assets. This is strictly a demonstration to impress the LoveLocal team.
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #263238; color: #ffffff; padding: 30px;">
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td style="padding-left: 15px;">
                                            <p style="margin: 0 0 5px; font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; color: #80cbc4;">
                                                &lt;DEVELOPER_MODE&gt;
                                            </p>
                                            <p style="margin: 0 0 10px; font-family: sans-serif; font-size: 13px; line-height: 1.5; color: #cfd8dc;">
                                                Sending to: {email}
                                            </p>
                                             <p style="margin: 10px 0 0; font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; color: #80cbc4;">
                                                &lt;/DEVELOPER_MODE&gt;
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px 20px; text-align: center; color: #880e4f; font-size: 12px;">
                    <p style="margin: 0;">&copy; 2026 LoveLocal. All rights reserved.</p>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>
    """
    
    # ---------------------------------------------------------
    # EMAIL CONFIGURATION
    # ---------------------------------------------------------
    
    # We rename this to 'msg' so it doesn't conflict with the 'message_text' string
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Update from LoveLocal" # General Subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        print(f"General email sent successfully!")
        return {'emailserver':f"General email sent!"}
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

