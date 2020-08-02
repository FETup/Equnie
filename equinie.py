from bs4 import BeautifulSoup
import requests
import telepot
from datetime import datetime
import schedule
import time


symbol = ["Enter your stock list"]
price = ["Enter the price at which ypu bought"]
qty = ["Enter qty"]
prtfl = [symbol,price,qty]
news_message = ""
previous_news = []
latest_news = []






headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}

def portfolio(stck_symbol,stck_price,stck_qty):


    url = "https://uk.finance.yahoo.com/quote/%s.NS?p=%s.NS&.tsrc=fin-srch" %(stck_symbol,stck_symbol) 

    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'lxml')

    find = soup.find('div',attrs={'class':'D(ib) Mend(20px)'})


    live_val = find.find('span').text
    live_val = float(live_val.replace(',',''))

    retun = (live_val * stck_qty) - (stck_price * stck_qty)

    retun_percent = (retun / (stck_price * stck_qty) )* 100

    return str(stck_symbol),"{:.2f}".format(retun_percent),"{:.2f}".format(retun)



def get_HTML(url):
    link = url
    page = requests.get(link,headers=headers)
    soup = BeautifulSoup(page.content,'lxml')

    return soup

def get_time():
        
    date_now = datetime.now()
    if(len(str(date_now.month)) == 1):
        date_today = str(date_now.day) + '-0' + str(date_now.month) + '-' + str(date_now.year)

    else:
        date_today = str(date_now.day) + '-' + str(date_now.month) + '-' + str(date_now.year)

    return date_today    



def get_news(html,html1,html2,date_present):
    
    all_news = []
     
    date_today = get_time()
    
    news = html.find('div',attrs={'id':'main-company-content'})

    for point in range(0,20) :
        
        date = news.find_next('div',attrs={'class':'col-4 col-md-2'}).text.strip()

        if(date == date_today):

            news = news.find_next('div',attrs={'class':'col-8 col-md-10'})
            all_news += [news.text.strip()]

        else:
            break

    news = html1.find('div',attrs={'id':'main-company-content'})

    for point in range(0,20) :
        
        date = news.find_next('div',attrs={'class':'col-4 col-md-2'}).text.strip()

        if(date == date_today):

            news = news.find_next('div',attrs={'class':'col-8 col-md-10'})
            all_news += [news.text.strip()]

        else:
            break    
        
    news = html2.find('div',attrs={'id':'main-company-content'})

    for point in range(0,20) :
        
        date = news.find_next('div',attrs={'class':'col-4 col-md-2'}).text.strip()

        if(date == date_today):

            news = news.find_next('div',attrs={'class':'col-8 col-md-10'})
            all_news += [news.text.strip()]

        else:
            break    

    return all_news


def send_news():

    global previous_news,latest_news 
    
    print('Fetching..')
    date_today = get_time()     
   
    page_1 = get_HTML("https://www.moneyworks4me.com/indianstocks/company-news?page=1")

    page_2 = get_HTML("https://www.moneyworks4me.com/indianstocks/company-news?page=2")

    page_3 = get_HTML("https://www.moneyworks4me.com/indianstocks/company-news?page=3")

    #print(get_news(page_1,page_2,page_3,date_today))

    latest_news = get_news(page_1,page_2,page_3,date_today)

    if(len(previous_news) < len(latest_news)):

        news_range = len(latest_news) - len(previous_news)

        news_message = "__*" + date_today + "*__" + "\n"

        for i in range(len(previous_news) + 1,news_range):
            
            news_message += "\n\n" + str(i + 1) + ". " + latest_news[i]

        print(news_message)
        bot.sendMessage("enter chat id",news_message,parse_mode='Markdown')

        previous_news = latest_news

    if(len(latest_news) == 0):
        previous_news = latest_news    




def handle(msg):

    chat_id = msg['chat']['id']
    command = msg['text']

    print(chat_id,command)

    if (command == '/portfolio' and chat_id == "enter chat id"):
        
        for f in range(0,len(symbol)):
                
            symb,profit_percent,profit = portfolio(prtfl[0][f],prtfl[1][f],prtfl[2][f])

            bot.sendMessage(chat_id,"%s   %s%%   ₹%s" %(symb,profit_percent,profit))




bot = telepot.Bot('enter your token')



print("Listening...")
print("%s %s " %(str(prtfl[0][0]),str(prtfl[1][0])))
#schedule.every().day.at("14:00").do(send_news)
schedule.every(2).minutes.do(send_news)
print(get_time())

bot.message_loop(handle)

while 1:
        
    schedule.run_pending()

    time.sleep(10)



