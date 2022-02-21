import os, csv, smtplib, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_error_email(error_message, error_description):


    addr_to   = ''
    addr_from = ''
    addr_to_list   = []

    smtp_server = ''

    msg = MIMEMultipart('alternative')
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = ''

    text = "There was an error with the script. \n\n" + str(error_description) + "\n\nERROR MESSAGE: " + str(error_message)

    part1 = MIMEText(text, 'plain')

    msg.attach(part1)

    s = smtplib.SMTP(smtp_server)
    s.sendmail(addr_from, addr_to_list, msg.as_string())
    s.quit()
    exit()



#Declare Variables
hostnames = []
ip_addresses = []
is_up = []
email_body = "DEVICES DOWN: \n\n"
count = 0
down_device_count = 0
logging.basicConfig(filename="UpChecker.log",format='%(asctime)s %(message)s',filemode='w')

try: 

    with open('IP_Address_List.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        for x in csv_reader:
            if x[0] == 'Hostname':
                pass
            else:
                hostnames.append(x[0])
                ip_addresses.append(x[1])

except Exception as e:
    
    error_message = "Error while opening CSV"
    logging.error(error_message)
    logging.error(e)
    send_error_email(e, error_message)

try: 
    for x in ip_addresses:
        response = os.system("ping " + x)
        print(response)
        
        if response == 0:
            is_up.append("TRUE")

        else:
            is_up.append("FALSE")

except Exception as e:
    
    error_message = "Error while pinging IP Addresses"
    logging.error(error_message)
    logging.error(e)
    send_error_email(e, error_message)

try: 

    for x in hostnames:
        if is_up[count] == "FALSE":
            email_body += "HOSTNAME: " + str(x) + "\nIS UP: " + str(is_up[count]) + "\n\n"
            down_device_count +=1
        count += 1

    if down_device_count == 0:
        email_body += "NO DEVICES DOWN"

except Exception as e:
    error_message = "Error while creating report string"
    logging.error(error_message)
    logging.error(e)
    send_error_email(e, error_message)


addr_to   = ''
addr_from = ''
addr_to_list   = []

smtp_server = ''

msg = MIMEMultipart('alternative')
msg['To'] = addr_to
msg['From'] = addr_from
msg['Subject'] = ''

part1 = MIMEText(email_body, 'plain')

msg.attach(part1)

s = smtplib.SMTP(smtp_server)
s.sendmail(addr_from, addr_to_list, msg.as_string())
s.quit()

logging.error("Script Ran")


















