# JPG-Geolocation-Data-Extraction-Tool

## Major Features
The major feature of this python program is to gather geolocation data associated with photos. This data is included in the EXIF metadata within an image. The python program will ask for the examiner’s email information. It will then ask the examiner to provide either an individual photo or photo folder to be analyzed. When the program has gathered the metadata, it will output that information into a CSV file format. The program will then take the previous general information that was provided by the examiner and send an email containing the CSV file attachment.  


## Network Functionality
The program’s main networking functionality is the email sending function with attachment handling. The script uses the Gmail SMTP server on port 587 with the Transport Layer Security (TLS) for security. It uses the ‘smtp’ library to connect to the Gmail SMTP server, which is “smtp.gmail.com.” 

In order for this program to work, a Gmail "App Password" will need to be setup within your account. To note, 2-step verification will need to be enabled on your Gmail account for this option to show. Additionally, this program only sends the outputs from a Gmail account. This app password is separate from the account password and allows outside applications to sign into the account without 2-Step verification.

## Program Functions
![image](https://github.com/goldrosecoder/JPG-Geolocation-Data-Extraction-Tool/assets/41834404/f5726cf3-fe73-41bc-ad8c-c92d3592e53f)

# Data, data types, and transformations
![image](https://github.com/goldrosecoder/JPG-Geolocation-Data-Extraction-Tool/assets/41834404/e2013798-202b-4235-9dff-9be746a8319a)

Happy photo analysis!
