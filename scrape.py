import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

#scrape the data
def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'html.parser')
            title = soup.title.text
            links = [link.get('href') for link in soup.find_all('a',href=True)]
            images = [image.get('src') for image in soup.find_all('img',src=True)]
            return {'Title':title,'Links':links,'Images':images}
        else:
            print("Failed to retrieve data from: ",url)
            return None
    except requests.exceptions.RequestException as e:
        print('Error',e)
        return None


#gets urls from excel and return of list named extracted_data
def scrape_from_excel(file_location):
    df = pd.read_excel(file_location)
    urls = df.iloc[:,0].tolist()
    extracted_data = []  
    for url in urls:
        data = scrape_data(url)
        if data:
            extracted_data.append(data)  
    return extracted_data  



#convert extracted_data to csv
def save_to_csv(data, csv_path):
    if data:
        with open(csv_path, 'w', newline="", encoding="utf-8") as csvfile:
            fieldnames = [ 'Title', 'Links','Images']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in data:
                writer.writerow(d)  


excel_file_path = "Scrapping Python Assigment- Flair Insights.xlsx"
csv_path = 'extracted_data.csv'


extracted_data = scrape_from_excel(excel_file_path)
save_to_csv(extracted_data, csv_path)
