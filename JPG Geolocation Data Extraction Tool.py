'''
Date: June 23, 2023
Description: This python program gathers geolocation data associated with JPG photos. 
The program will first ask for the examiner's for their email. Multiple emails can be inputted as well. 
It will then ask the user to provide the photo location to be analyzed. This can include the photo folder itself or just a singular photo.
When the program has gathered the metadata, it will output that information into a CSV file format. 
The program will then take information that was provided by the examiner and send an email with the CSV file attachment.'''

""""""

import smtplib, csv, exifread, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#Function name: get_geodata_from_photo
#Purpose: Extracts geolocation from JPG file
#Inputs: photo_path
#Returns: No return values

def get_geodata_from_photo(photo_path):
    try:
        with open(photo_path, 'rb') as f: #Opens photo path
            tags = exifread.process_file(f)
    except Exception as e:
        print(f"Error reading EXIF data from {photo_path}: {e}")
        return None

    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        #Extracts degrees, minutes, and seconds from image
        latitude = tags['GPS GPSLatitude'].values
        longitude = tags['GPS GPSLongitude'].values

        #Converts degrees, minutes, and seconds to decimal format
        latitude_decimal = float(latitude[0].num) + float(latitude[1].num) / 60 + float(latitude[2].num) / 3600
        longitude_decimal = float(longitude[0].num) + float(longitude[1].num) / 60 + float(longitude[2].num) / 3600

        #Rounds the decimal values to 6 decimal places
        latitude_decimal = round(latitude_decimal, 6)
        longitude_decimal = round(longitude_decimal, 6)

        #Adds a negative sign based on the direction 
        if 'GPS GPSLatitudeRef' in tags and tags['GPS GPSLatitudeRef'].printable == 'S':
            latitude_decimal *= -1
        if 'GPS GPSLongitudeRef' in tags and tags['GPS GPSLongitudeRef'].printable == 'W':
            longitude_decimal *= -1

        return latitude_decimal, longitude_decimal
    else:
        return None

#Function name: write_to_csv
#Purpose: Writes geolocation data to CSV file
#Inputs: filename, data
#Returns: No return values
def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Latitude', 'Longitude']) #Lists the different categories
        writer.writerows(data)


#Function name: analyze_photos_in_folder
#Purpose: Analyzes JPG files in a folder
#Inputs: folder_path
#Returns: geodata_list
def analyze_photos_in_folder(folder_path):
    photo_files = []
    for root, dirs, files in os.walk(folder_path): #Traverses the current directory and subdirectories
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')): #Checks for jpg extensions
                photo_files.append(os.path.join(root, file))

    geodata_list = []
    for photo_file in photo_files:
        geodata = get_geodata_from_photo(photo_file)
        #Checks geodata to see if it has a value or is empty
        if geodata:
            geodata_list.append((os.path.basename(photo_file),) + geodata)
        else:
            geodata_list.append((os.path.basename(photo_file), 'No GPS data', 'No GPS data'))

    return geodata_list

#Email configuration
smtp_port = 587  #Gmail secure SMTP port
smtp_server = "smtp.gmail.com" 
email_from = "email@example.com" #Use the email you want to send the results from
email_password = "password here" #Put the app password from the email here

email_list = []
user_email = input("Enter an email address to send the results to.\nIf there are multiple, separate them by a comma: ").split(',') 
#This statement is used if there is more than one email address
if user_email:
    email_list.extend(user_email)
email_list.append(email_from)  

#Automated email subject and message 
subject = "Automated Geolocation Data"
message = "Hi, \n\nAttached is the CSV file containing image geolocation data.\n\nThank you!"

#Asks user to input the path to the photo or folder
path = input("Enter the file path to the photo or folder: ")

#Analyzes the geolocation data
if os.path.isfile(path):  #Checks if it is a file
    geodata_list = []
    geodata = get_geodata_from_photo(path)
    if geodata:
        geodata_list.append((os.path.basename(path),) + geodata)
    else:
        geodata_list.append((os.path.basename(path), 'No GPS data', 'No GPS data'))
else:  # Checks if it is a folder
    geodata_list = analyze_photos_in_folder(path)

#Writes geolocation data to a CSV file
csv_filename = "image_geodata.csv"
write_to_csv(csv_filename, geodata_list)
print(f"Geolocation data written to {csv_filename}")


#Function name: send_email_with_attachment
#Purpose: Sends an email with CSV attachment
#Inputs: sender_email, sender_password, receiver_email, subject, message, attachment_filename
#Returns: No return value
def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, message, attachment_filename):
    #The following creates a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    #Attaches the message to the email
    msg.attach(MIMEText(message, 'plain'))

    #Defines the attachment file
    attachment = open(attachment_filename, 'rb')

    #Base54 encoding
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload(attachment.read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename=" + attachment_filename)
    msg.attach(attachment_package)

    #Converts the message to a string
    text = msg.as_string()

    #Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        #Sends the email
        server.sendmail(sender_email, receiver_email, text)

#Sends the email with the attachment
for email in email_list:
    send_email_with_attachment(email_from, email_password, email.strip(), subject, message, csv_filename)
    print(f"Successfully sent an email to {email}.")
