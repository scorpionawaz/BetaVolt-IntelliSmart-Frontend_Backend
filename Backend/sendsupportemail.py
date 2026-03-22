import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_order_email(order_id, customer, address, items, pricing):
    
    # 1. Generate the HTML loop for items dynamically
    items_html_rows = ""
    for item in items:
        items_html_rows += f"""
        <tr>
            <td style="padding: 15px 0; border-bottom: 1px solid #f0f0f0; color: #333333; font-weight: 500;">
                {item['name']}
            </td>
            <td align="center" style="padding: 15px 0; border-bottom: 1px solid #f0f0f0; color: #666666;">
                {item['qty']}
            </td>
            <td align="right" style="padding: 15px 0; border-bottom: 1px solid #f0f0f0; color: #333333; font-weight: 600;">
                ₹{item['price']}
            </td>
        </tr>
        """

    # 2. The HTML Body (using f-strings)
    body = f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
    <meta name="x-apple-disable-message-reformatting"> 
    <title>Order Confirmation - LoveLocal</title>
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
            .step-text {{ font-size: 10px !important; }}
        }}
    </style>
</head>
<body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #fce4ec;">
    <center style="width: 100%; background: linear-gradient(180deg, #fce4ec 0%, #fff0f5 100%); background-color: #fce4ec;">
        
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
            LoveLocal Simulation: Order details (Internship Project By Nawaz Sayyad).
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
                            <td class="pad-mobile" style="padding: 10px 40px 30px;">
                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td align="center" width="33%">
                                            <div style="height: 12px; width: 12px; background-color: #e91e63; border-radius: 50%; margin-bottom: 5px; box-shadow: 0 0 10px #e91e63;"></div>
                                            <div style="height: 4px; width: 100%; background-color: #e91e63;"></div>
                                            <p class="step-text" style="margin: 5px 0 0; font-size: 12px; color: #e91e63; font-weight: 700;">Placed</p>
                                        </td>
                                        <td align="center" width="33%">
                                            <div style="height: 12px; width: 12px; background-color: #ff80ab; border-radius: 50%; margin-bottom: 5px; box-shadow: 0 0 10px #ff80ab;"></div>
                                            <div style="height: 4px; width: 100%; background-color: #ff80ab;"></div>
                                            <p class="step-text" style="margin: 5px 0 0; font-size: 12px; color: #ff80ab; font-weight: 600;">Packing</p>
                                        </td>
                                        <td align="center" width="33%">
                                            <div style="height: 12px; width: 12px; background-color: #eeeeee; border-radius: 50%; margin-bottom: 5px;"></div>
                                            <div style="height: 4px; width: 100%; background-color: #eeeeee;"></div>
                                            <p class="step-text" style="margin: 5px 0 0; font-size: 12px; color: #bbbbbb; font-weight: 400;">Delivered</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td class="pad-mobile" style="padding: 0 40px 10px 40px; text-align: center;">
                                <h2 class="h1-mobile" style="margin: 0 0 10px; font-size: 26px; font-weight: 700; color: #1a1a1a;">Order Confirmed!</h2>
                                <p style="margin: 0 0 20px; font-size: 15px; line-height: 24px; color: #666666;">
                                    Hey <strong>{customer['name']}</strong>! The shopkeeper has received your order.
                                </p>
                                <div style="background-color: #fff0f5; border-radius: 12px; padding: 15px; display: inline-block; border: 1px dashed #e91e63; margin-bottom: 15px;">
                                    <span style="font-weight: 600; color: #e91e63;">{order_id}</span>
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td class="pad-mobile" style="padding: 0 40px 20px 40px;">
                                <table width="100%" bgcolor="#f9f9f9" style="border-radius: 8px; padding: 15px;">
                                    <tr>
                                        <td align="center" style="color: #666666; font-size: 13px;">
                                            Delivering to:<br>
                                            <strong style="color: #333333; font-size: 14px;">{address['street']}, {address['city']}</strong>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td class="pad-mobile" style="padding: 10px 40px;">
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <th align="left" style="padding-bottom: 10px; font-size: 12px; text-transform: uppercase; color: #999999; border-bottom: 2px solid #fce4ec;">Item</th>
                                        <th align="center" style="padding-bottom: 10px; font-size: 12px; text-transform: uppercase; color: #999999; border-bottom: 2px solid #fce4ec;">Qty</th>
                                        <th align="right" style="padding-bottom: 10px; font-size: 12px; text-transform: uppercase; color: #999999; border-bottom: 2px solid #fce4ec;">Price</th>
                                    </tr>
                                    {items_html_rows}
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td class="pad-mobile" style="padding: 20px 40px 30px;">
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td width="40%"></td>
                                        <td width="60%">
                                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                                <tr>
                                                    <td style="padding-bottom: 5px; color: #888888; font-size: 14px;">Subtotal</td>
                                                    <td align="right" style="padding-bottom: 5px; color: #333333;">₹{pricing['subtotal']}</td>
                                                </tr>
                                                <tr>
                                                    <td style="padding-bottom: 15px; color: #888888; font-size: 14px;">Delivery</td>
                                                    <td align="right" style="padding-bottom: 15px; color: #333333;">₹{pricing['delivery']}</td>
                                                </tr>
                                                <tr>
                                                    <td style="border-top: 1px solid #eee; padding-top: 10px; font-weight: 700; color: #e91e63; font-size: 20px;">Total</td>
                                                    <td align="right" style="border-top: 1px solid #eee; padding-top: 10px; font-weight: 700; color: #e91e63; font-size: 20px;">₹{pricing['total']}</td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="padding: 0 40px 50px;">
                                <a href="https://lovelocal.adroitsdvc.in" class="button-hover" style="background: linear-gradient(135deg, #ec407a 0%, #c2185b 100%); border-radius: 50px; color: #ffffff; display: inline-block; font-family: 'Poppins', sans-serif; font-size: 16px; font-weight: 600; line-height: 54px; text-align: center; text-decoration: none; width: 240px; box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);">
                                    Track Order
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
                                                Sending to: {customer['email']}
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
    
    # Credentials
    sender_email = 'adroituniversal@gmail.com'
    app_password = 'cslp clhh rtci ecbw'
    
    # ---------------------------------------------------------
    # UPDATED: Receiver email is now the actual customer email
    # ---------------------------------------------------------
    receiver_email = customer['email']

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Order Confirmation - LoveLocal (Simulation)"

    message.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"LoveLocal Order Simulation email sent successfully to {receiver_email}!")
        return {'emailserver':f"LoveLocal Order Simulation email sent successfully to {receiver_email}!"}
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

def send_support_email(ticket_id, customer_email, customer_name, issue_category, priority_level, portal_url="https://betavolt.intellismart.com/support"):
    body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
    <title>Support Ticket Raised - Intellismart</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        html, body {{ margin: 0 auto !important; padding: 0 !important; height: 100% !important; width: 100% !important; font-family: 'Poppins', sans-serif; background-color: #f4f7f9; }}
        * {{ -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt !important; mso-table-rspace: 0pt !important; }}
        table {{ border-spacing: 0 !important; border-collapse: collapse !important; table-layout: fixed !important; margin: 0 auto !important; }}
        .button-hover:hover {{ opacity: 0.9 !important; transform: scale(1.02); box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3) !important; }}
        @media screen and (max-width: 600px) {{
            .email-container {{ width: 100% !important; }}
            .pad-mobile {{ padding-left: 20px !important; padding-right: 20px !important; }}
            .h1-mobile {{ font-size: 22px !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0 !important; background-color: #f4f7f9;">
    <center style="width: 100%; background-color: #f4f7f9; padding-bottom: 40px;">
        
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="margin: auto;" class="email-container">
            <tr><td style="padding: 30px 0;"></td></tr>
            <tr>
                <td style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e1e8ed; overflow: hidden;">
                    
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 40px 20px 20px; text-align: center;">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOntt7gB-X6tyznlvd8CkTc8L-jxzFsQum7Q&s" alt="Intellismart Logo" width="200" style="display: block; margin: 0 auto; height: auto;">
                            </td>
                        </tr>
                    </table>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td class="pad-mobile" style="padding: 10px 60px 30px;">
                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td align="center" width="33%">
                                            <div style="height: 12px; width: 12px; background-color: #0066cc; border-radius: 50%; margin-bottom: 5px;"></div>
                                            <div style="height: 4px; width: 100%; background-color: #0066cc;"></div>
                                            <p style="margin: 5px 0 0; font-size: 11px; color: #0066cc; font-weight: 700;">Ticket Raised</p>
                                        </td>
                                        <td align="center" width="33%">
                                            <div style="height: 12px; width: 12px; background-color: #d1d9e0; border-radius: 50%; margin-bottom: 5px;"></div>
                                            <div style="height: 4px; width: 100%; background-color: #d1d9e0;"></div>
                                            <p style="margin: 5px 0 0; font-size: 11px; color: #7f8c8d; font-weight: 600;">Processing</p>
                                        </td>
                                        <td align="center" width="33%">
                                            <div style="height: 12px; width: 12px; background-color: #d1d9e0; border-radius: 50%; margin-bottom: 5px;"></div>
                                            <div style="height: 4px; width: 100%; background-color: #d1d9e0;"></div>
                                            <p style="margin: 5px 0 0; font-size: 11px; color: #7f8c8d; font-weight: 400;">Resolved</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td class="pad-mobile" style="padding: 0 40px 20px; text-align: center;">
                                <h2 class="h1-mobile" style="margin: 0 0 10px; font-size: 24px; color: #2c3e50;">Support Ticket Received</h2>
                                <p style="margin: 0 0 20px; font-size: 15px; color: #576574; line-height: 1.6;">
                                    Hello <strong>{customer_name}</strong>, your request has been successfully logged. Our technical team is reviewing the details.
                                </p>
                                <div style="background-color: #f8f9fa; border-radius: 8px; padding: 12px 25px; display: inline-block; border: 1px solid #d1d9e0; margin-bottom: 20px;">
                                    <span style="font-weight: 700; color: #2c3e50; font-family: monospace; font-size: 18px;">#{ticket_id}</span>
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td class="pad-mobile" style="padding: 0 40px 30px;">
                                <table width="100%" style="border-top: 1px solid #eee;">
                                    <tr>
                                        <td style="padding: 15px 0; font-size: 14px; color: #7f8c8d;">Category</td>
                                        <td align="right" style="padding: 15px 0; font-size: 14px; color: #2c3e50; font-weight: 600;">{issue_category}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 10px 0; font-size: 14px; color: #7f8c8d;">Priority</td>
                                        <td align="right" style="padding: 10px 0; font-size: 14px; color: #e67e22; font-weight: 600;">{priority_level}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 10px 0; font-size: 14px; color: #7f8c8d;">Est. Response</td>
                                        <td align="right" style="padding: 10px 0; font-size: 14px; color: #2c3e50;">Within 24 Hours</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="padding: 0 40px 40px;">
                                <a href="{portal_url}" class="button-hover" style="background: #0066cc; border-radius: 6px; color: #ffffff; display: inline-block; font-size: 15px; font-weight: 600; line-height: 50px; text-align: center; text-decoration: none; width: 220px;">
                                    View Ticket Status
                                </a>
                            </td>
                        </tr>

                        <tr>
                            <td style="background-color: #f1f2f6; border-top: 1px solid #d1d9e0; padding: 20px 30px; text-align: center;">
                                <p style="margin: 0; font-size: 12px; color: #7f8c8d; line-height: 1.5;">
                                    <strong>PROJECT NOTE:</strong> This is a simulation created by <strong>Nawaz Sayyad</strong> for an internship project. This is not a formal communication from Intellismart.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px 20px; text-align: center; color: #95a5a6; font-size: 12px;">
                    <p style="margin: 0;">&copy; 2026 Intellismart Infrastructure Pvt Ltd.</p>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>
"""

    sender_email = 'adroituniversal@gmail.com'
    app_password = 'cslp clhh rtci ecbw'
    receiver_email = customer_email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f"Support Ticket Received - #{ticket_id}"
    message.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Support ticket email sent successfully to {receiver_email} (Ticket: {ticket_id})")
        return {'status': 'success', 'message': f'Email sent successfully to {receiver_email}'}
    except Exception as e:
        print(f"An error occurred while sending the support email: {e}")
        return {'status': 'failed', 'error': str(e)}

