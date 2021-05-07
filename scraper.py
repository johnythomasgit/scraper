# web scraping functions for checking stock availability
import requests
from bs4 import BeautifulSoup
import email
import smtplib
import datetime
from pytz import timezone
import urllib
import json


def send_mail(subject, message):

    # create message object instance
    msg = email.message.Message()

    # setup the parameters of the message
    password = "jgmanjbbv"
    msg['From'] = "johnythomas.online@gmail.com"
    msg['To'] = "johnyvtk@gmail.com"
    msg['Subject'] = subject + " " + datetime.datetime.now(timezone('Asia/Kolkata')).strftime("%b,%d %I:%M %p")

    # add in the message body
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("mail send successfully")


def covid_center_search():

    available_centers = []
    for period in range(32):
        new_date = datetime.datetime.today() + datetime.timedelta(days=period)
        new_date_str = new_date.strftime("%d-%m-%Y")
        covin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=304" \
                    "&date=" + new_date_str
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Host': 'cdn-api.co-vin.in',
                   'Connection': 'keep-alive'
                   }
        # req = urllib.request.Request(url=covin_url, headers=headers)
        # response = urllib.request.urlopen(req).read().decode('utf-8')
        response = requests.get(covin_url, headers=headers)
        print(response.status_code)
        print(response.json())
        response_json = response.json()

        for center in response_json.get("centers"):
            for session in center.get("sessions"):
                if int(session.get("min_age_limit")) < 45:
                    available_centers.append(center.get("name") + " on " + new_date_str)

    print("total-" + str(len(available_centers)))
    if len(available_centers) > 0:
        print(available_centers)
        send_mail("Covid Vaccine available", ",<br/>".join(available_centers))
    else:
        print("Not available")


def product_availability_search():
    # URL = "https://www.casioindiashop.com/Watches/AD249/Casio-Youth-Series-WS-1200H-3AVDF-(AD249)-Digital-Watch.html"
    URL = "https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series-AE-1500WH-1AVDF-(D218)-Digital-Watch.html"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,
                         'html5lib')
    divTag = soup.find("div", attrs={"class": "price"}).find(attrs={"class": "flbuts"})
    print(divTag)
    if divTag.find("a", attrs={"class": "cart-buy"}) or divTag.find("a", "Buy Now"):
        print("Available")
        send_mail("Your watch is now available",
                  "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
                  "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")
    else:
        print("Not Available")
        # send_mail("Out of stock", "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
        #                           "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")


if __name__ == "__main__":
    product_availability_search()
    covid_center_search()
