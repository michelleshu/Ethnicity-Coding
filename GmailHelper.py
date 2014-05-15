import smtplib

def sendEmail():
    fromaddr = 'methlstudent@gmail.com'
    toaddr = 'shu.michelle.w@gmail.com'
    msg = 'Ethnicity-Coding process finished'

    username = 'methlstudent@gmail.com'
    password = 'hell0w0rld'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()