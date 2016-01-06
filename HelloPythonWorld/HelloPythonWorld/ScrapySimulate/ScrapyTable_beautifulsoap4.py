'''
Created on Aug 24, 2015

@author: tguo
'''

# coding=UTF-8

from bs4 import BeautifulSoup

def get_all_contact_urls(self):
    base_url = 'http://www.irit.fr/Personnel,197?lang=fr'
    try:
        response = requests.get(base_url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return
    
    soup = BeautifulSoup(response.text)

    ## retrieve links like: http://www.irit.fr/spip.php?page=annuaire&code=8292 
    for anchor in soup.find_all("a") :
        if anchor.has_attr('href') :
            link = anchor['href']
            if 'annuaire&code' in link :
                self.set_urls.add(link)

def crawler_contact_infos(self):
    self.get_all_contact_urls()
    
    header = ['Name', 'Statut', 'Service/Equipe', 'Contact', 'Localisation', 'Téléphone']
    self.contact_infos.append(header)
    
    for url in self.set_urls :
        #url = 'http://www.irit.fr/spip.php?page=annuaire&code=8955&lang=fr'
        record = self.crawler_contact_info(url)
        self.contact_infos.append(record)

def crawler_contact_info(self, url):
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        return list()
    
    record = list()

    soup = BeautifulSoup(response.text)
    
    ## Step 1: get the name
    tags_name = soup.find_all("p", {"class" : "titre"})  #<p class="titre">  Su Qiankun</p>
    if not tags_name: #deal with tags_name=[]
        return record
    name = tags_name[0].contents[0].strip() #strip() remove whitespace
    record.append(name)

    ## Step 2: get other infos
    table = soup.find('table')
    #table_body = table.find('tbody')
    for row in table.find_all('tr') :
        rep = {ord(':'): ''}  #remove ':' at the end of string, such as 'Statut : '
        columns = [col.get_text().translate(rep).replace(' at ', '@').strip() for col in row.find_all('td')]
        record.append(columns[1]) #store value
        
    return record