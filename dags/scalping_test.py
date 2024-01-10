from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import WebDriverException
import time
def mongo_connect():
    username='admin'
    password='admin'
    database_name='test'
    connection_string = f"mongodb://{username}:{password}@172.21.0.11:27017/"
    client = MongoClient(connection_string)
    db = client['Data']
    try: 
        db.command("serverStatus")
    except Exception as e:
        return False, db
    
    else: 
        return True , db

def dump_mongodb(collection,document):
    result=collection.insert_one(document)
    return result

from datetime import datetime



def dump_database(db,single_event,betting_dic,event_type):
        
    document_signle_event={'id_event':single_event[2],
                      'name_event':single_event[1],
                      'time_event':single_event[0]
                      
                      }
    document_betting=betting_dic
    document_betting['id_event']=single_event[2]
    document_betting['name_event']=single_event[1]

    document_betting['datetime']=datetime.now()
    events=db['Events'] # we get the collection pub where we will dumb our document_pub
    print('\n',betting_dic)
    print('\n ',document_betting)
    print('/n ')
    print(dump_mongodb(events[event_type],document_signle_event))
    print(dump_mongodb(events['Bettings'],document_betting))





def get_sport_page(url,sport_name):
    return url+'/'+sport_name




def get_sports_name(browser):
    name_liste=[]
    sport_divs=browser.find_elements(By.XPATH, '//div[@class="NomeSport"]')
    for sport_div in sport_divs:
        sport_name=sport_div.find_element(By.XPATH,'a').find_element(By.XPATH,'span').get_attribute('data-title')
        name_liste.append(sport_name)
    return name_liste






def authentification():
    pass
def count_children(element):
    return len(element.find_elements(By.XPATH,'./*'))

def get_events_ids(browser):
    inputs_checkboxs=browser.find_elements(By.XPATH,'//input[@class="chkLeague"]')
    return [inputs_value.get_attribute('value') for inputs_value in inputs_checkboxs]

def get_primary_data(element):
    date=element.get_attribute("data-datainizio")
    game_name=element.get_attribute("data-sottoevento-name")
    game_id=element.get_attribute("data-codpubblicazione")
    return date,game_name,game_id


def slice_liste(liste,max_number=2):
    string=''
    statue=False
    sliced_liste=[]
    if len(liste)<max_number:
        max_number=len(liste)
        sliced_liste.append(liste)
        return sliced_liste
    diviseur=len(liste)/max_number
    mod =len(liste)%max_number
    i=0
    while (statue==False):
        if i+1<=diviseur:
            sliced_liste.append(liste[i*max_number:(i+1)*max_number])
            i=i+1
        elif i+1>= diviseur and mod==0:
            statue =True
            
        else:
            final_slice=(i)*max_number
            print(final_slice)
            sliced_liste.append(liste[final_slice:])
            statue =True
    return sliced_liste






# lsite must have int values as a string
def create_string_from_list(liste):
    string=''
    
    number=len(liste)
    for i in range(number):
        string=string+str(liste[i])
        if i !=number-1:
            string=string+','
    return string



def get_odds_data(element):
    dic={}
    odds_details=element.find_element(By.XPATH,'td[@class="OddsDetailsQuote"]').find_element(By.XPATH,'table[@class="dgQuote"]').find_element(By.XPATH,'tbody').find_element(By.XPATH,'tr[@class="OddsQuotaItemStyle"]').find_elements(By.XPATH,'td')
    
    for odds_detail in odds_details:
        
        key=odds_detail.get_attribute('data-tipoquota')
        value=odds_detail.get_attribute('data-quota')
        if key !=None:
            dic[key]=value
    return  dic   



def get_data_per_event(db,event,sport_name):
    print('ime here')
    clear_events=event.find_element(By.XPATH,'div[@class="divQta"]').find_element(By.XPATH,'div[@class="divQt"]')
    


    tables = clear_events.find_elements(By.XPATH,'table')

    for single_game in tables:
        tbody = single_game.find_element(By.XPATH, "tbody")
        rows = tbody.find_elements(By.XPATH, "tr[@class='dgAItem']")
        

        for row in rows :
            primary_data=get_primary_data(row)
            betting_data= get_odds_data(row)
            dump_database(db,primary_data,betting_data,sport_name)
    try :
        return primary_data,betting_data
    except:
        pass





def start_scraping():
    print('Hello and Welcome')

    options = Options()
    options.add_argument('--disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('--disable-extensions')

    url='https://www.betplanet365.com/en/sports-betting'
    events_url='https://www.betplanet365.com/en/sports-betting/events/'
    browser = webdriver.Remote(
        command_executor='http://172.21.0.10:4444/wd/hub',
        options=webdriver.ChromeOptions())
    browser.get(url)
    browser.maximize_window()
    wait = WebDriverWait(browser, 30) # wait for 30sec until the page fully load

    time.sleep(5)
    sport_liste=get_sports_name(browser)
    print(sport_liste)

    connection,db=mongo_connect()


    for sport_name in sport_liste:
        if connection==False:
            print('Fic database , connection refused')
            break
        
        try:
            browser.get(get_sport_page(url,sport_name))
            time.sleep(5)

            events_value_liste=get_events_ids(browser)
            events_value_sliced_s=slice_liste(events_value_liste,30)
            for events_value_sliced in events_value_sliced_s:
                new_url=events_url+(create_string_from_list(events_value_sliced))


                print('the new url',new_url)
                browser.get(new_url)
                time.sleep(10)


                MainEvents = browser.find_element(By.XPATH, '//div[@id="divMainEvents"]')
                events=MainEvents.find_elements(By.XPATH,'./*')

                #loop on the childs :
                
                for event in events:
                    try :
                        print(event.get_attribute('id'))

                        info_liste=get_data_per_event(db,event,sport_name)
                    except:
                        print('excpetion when not dealing with Main Event')
                        pass    

        except:
            print('where the exeption happen',sport_name)    
            pass             



    browser.quit()