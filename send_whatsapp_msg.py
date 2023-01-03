import pywhatkit
import pandas as pd

# Read the data from the csv file
df = pd.read_csv("python.csv")
numbers = df['number']
msg = """
Assalam o Alaikum

I'm Muhammad Sameer from Sam Tech.
Congratulations!! on registering for the Python Pro Course! This is a great opportunity to learn a valuable skill that will open up many doors in your career. I'm sure you will find the course enjoyable and challenging, and I'm confident that you will come out of it with a strong foundation in Python programming. I wish you the best of luck in your studies, and I hope you have a great learning experience. Keep up the hard work, and don't hesitate to reach out if you have any questions or need any help along the way. I'll confirm your class timings and other details soon. In the meantime submit your fee and get ready to learn Python!

EasyPaisa Account Name: Muhammad Sameer
EasyPaisa Account Number: 03166368782 
JazzCash Account Name: Muhammad Sameer
JazzCash Account Number: 03166368782

Regards
Sam Tech
"""
hour = 15
mint = 47
for number in numbers:
# Send the message
    user_number = "+92" +str(number)
    pywhatkit.sendwhatmsg(user_number, msg, hour, mint)
    mint += 2