email_template = '''
    <html>
    <head>
        <style>
            body {{
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
                font-family: "Poppins", sans-serif;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }}
            .otp {{
                color: #020000;
                font-size: 24px;
                text-align: center;
                margin: 0;
            }}
            .header {{
                text-align: center;
                font-size: 26px;
                font-weight: bold;
                color: #020000;;
                margin-bottom: 20px;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #020000;;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                ProductGPT OTP
            </div>
            <p class="otp">
                {otp} is your ProductGPT OTP
            </p>
            <div class="footer">
                &copy; {year} ProductGPT. All rights reserved.
            </div>
        </div>
    </body>
    </html>
'''
