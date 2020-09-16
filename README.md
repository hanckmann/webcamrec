# webcamrec
Python application to store timestamped webcam images.

The application aims at storing the images as quickly as possible. Therefore capturing the images from the webcam is performed in a separate thread.

The images are saved as quickly as possible. This might result in dropped frames in the image viewer.

All data is stored in the data folder.
For each recording session a new folder is created, with the data-time stamp as foldername.
A new recording session is started when at the applications startup, and when hitting the space-bar or enter key.
All images are stored with their recorded date-time stamp in the filename.
All images are stored as PNG files.

I hope it is useful for you.

Patrick