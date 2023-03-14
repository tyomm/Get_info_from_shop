import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from distutils import command
import telebot
from constants import API_KEY
import sqlite3

# URL of the product page
url = "https://www.ebay.com/itm/134477794112?_trkparms=amclksrc%3DITM%26aid%3D1110006%26algo%3DHOMESPLICE.SIM%26ao%3D1%26asc%3D20200818143230%26meid%3Dbeca54992801434488292c2a49c1844d%26pid%3D101224%26rk%3D2%26rkt%3D5%26sd%3D204269092890%26itm%3D134477794112%26pmt%3D0%26noa%3D1%26pg%3D2047675%26algv%3DDefaultOrganicWeb%26brand%3DApple&_trksid=p2047675.c101224.m-1"

# Price threshold for notification
current_price = 42.73

def check_price():
    # Send request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        price = soup.find("div", class_="x-price-primary")
        final_price = price.find("span", class_="ux-textspans")
        final_price_txt = final_price.text  # get snap's content in string format
    except:
        print("Did not find price!")

    i = 0
    price = ""
    while (i < len(final_price_txt)):
        if (final_price_txt[i] != "$"):
            i += 1
        else:
            i += 1
            while (i < len(final_price_txt)):
                price += final_price_txt[i]
                i += 1

    price = float(price)

#========================Telegram Bot Part====================================
    if (price > current_price):
        bot = telebot.TeleBot(API_KEY, parse_mode = None)

        #===================START COMMAND====================
        start = "Hi, i'm created by Tyom\n"
        changed_price = price

        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id, start)
            bot.send_message(message.chat.id, changed_price)
            bot.send_message(1159606389, "Opened the DataBase //")
            bot.forward_message(1159606389, message.chat.id, message.message_id) # Forward message to me ('/start' command)
        #====================END COMMAND=========================


        #=============START Save Telegram DataBase================
        closed = False
        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):

            global closed
            if message.text.lower() == '/':  # '/finish' 
                print(message.text)
                closed = True
                bot.send_message(1159606389, "Closed the DataBase   /")
                with open("File_DataBase.txt", "rb") as file1:
                    bot.send_document(1159606389, file1)
                with open("File_DataBase.txt", "w") as file: # for delete file content
                    file.truncate() # for delete file content

            elif message.text.lower() == '//':  # '/continue'
                bot.send_message(1159606389, "Opened the DataBase //")
                closed = False

            elif message.text.lower() != '' and not closed:
                print(message.text)
                with open("File_DataBase.txt", "a", encoding="utf-8") as file:
                    file.write(message.text)
                    file.write("\n\n")
        #=============END Save Telegram DataBase================

        bot.polling(none_stop = True)


# Check the price every 5 seconds
while True:
    check_price()
    time.sleep(5)
