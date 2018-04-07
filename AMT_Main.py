from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import webbrowser
import requests
import smtplib
import time
import sys


def cinema_name_filter(movie_name_list_items):
    arr = []
    for data in movie_name_list_items:
        data = str(data)
        l = len(data)
        arr.append(data[8:l-9])
    return arr


def cinema_fetch_link(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_name_list = soup.find(id="venuelist")
    movie_name_list_items = movie_name_list.find_all('strong')
    return movie_name_list_items


def letter_filter(input):
    return ''.join([c.lower() for c in input if c.isalpha()])


def name_filter(movie_name_list_items):
    arr = []
    for data in movie_name_list_items:
        data = str(data)
        l = len(data)
        for i in range((l-4), 0, -1):
            if data[i] == ">":
                arr.append(letter_filter(data[i+1:l-4]))
    return arr


def fetch_details():
    city_name = input("Choose the city you want details about:  ")
    movie_name = input("Enter movie name here about which you would like to know the details (With correct spelling): ")
    movie_name = letter_filter(movie_name)
    return city_name, movie_name


def fetch_link(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_name_list = soup.find(class_="mv-row")
    movie_name_list_items = movie_name_list.find_all('a', class_="__movie-name")
    return movie_name_list_items


def fetch_buy_link(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_name_list = soup.find(class_="more-showtimes")
    movie_name_list_items = movie_name_list.find_all('a', class_="showtimes btn _cuatro")
    return str(movie_name_list_items[0].get("href"))


def automated_mail(send):
    msg = MIMEMultipart()
    msg['From'] = 'From - Mail ID>'
    msg['To'] = '<To - Mail ID>'
    msg['Subject'] = 'BookMyShow ALERT !!!'
    message = 'Your movie is now available at BookMyShow. Follow this link to reach the page: \n'+send
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('From - Mail ID>', '<To - Mail ID>')
    mailserver.sendmail('From - Mail ID>', '<To - Mail ID>', msg.as_string())
    mailserver.quit()


def main():
    city_name, movie_name = fetch_details()
    link = "https://in.bookmyshow.com/"+city_name+"/movies"
    while True:
        movie_name_list_items = fetch_link(link)
        movie_name_list = name_filter(movie_name_list_items)
        if movie_name not in movie_name_list:
            print("Redirected")
            time.sleep(300)
        else:
            det = str(movie_name_list_items[movie_name_list.index(movie_name)].get("href"))
            send = "https://in.bookmyshow.com"+det
            copy = send
            buy_link = "https://in.bookmyshow.com"+fetch_buy_link(send)
            cinema_name_list_items = cinema_fetch_link(buy_link)
            cinema_name_list = cinema_name_filter(cinema_name_list_items)
            send = send+"\n\n"
            send = send+"The movie is available at the following cinemas: \n\n"
            for x in cinema_name_list:
                send = send+x+"\n"
            webbrowser.open((copy+"#trailer"))
            automated_mail(send)
            print(send)
            sys.exit()

if __name__ == "__main__":
    main()
