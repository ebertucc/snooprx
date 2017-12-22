from bs4 import BeautifulSoup as bf
import requests
import re
import pickle
from collections import defaultdict
from cleaning_refs import med_dur_conversion as med_dur_conversion
import pandas as pd
from drug_objects import drug, review



#utility methods
def load_soup(url):
    html = requests.get(url).text
    soup = bf(html, 'html5lib')
    return soup

# takes url list, scrapes, returns pages of soup for a particular drug
def scrape_parse_reviews(url, drug, parser, tag):
    page = load_soup(url)
    rev_stew = page.find_all('div' ,{'class' : tag})
    for ik, item in enumerate(rev_stew):
        new_review = review(drug, item, parser, ik)
        drug.reviews.append(new_review)
    return drug 
            
                                
# ************ Drugs.com ************  Parser

class DrugsDotCom:
    
        def __init__(self, name, abbrev):
            self.name = name
            self.abbrev = abbrev
            
        def Drugslist_url_list(self, condition, pg_init, pg_n):
            url_c = ['https://www.drugs.com/condition/', '.html?page_number=']
            url_list = [url_c[0] + condition + url_c[1] +str(ik) for ik in range(pg_init, pg_n+1)]
            return url_list
        
        # function to process soups to extract drug metadata (mix of site specific and standardized) for drugs.com
        def process_drug(self, _drug_summary, _drug_condition, site, _new_drug):
            name_soup = _drug_summary.find('td', {'class':'condition-table__drug-name' })
            _new_drug.name = name_soup.text.strip().split('\n')[0]
            _new_drug.generic = _drug_condition.find('p', {'class': 'condition-table__generic-name'}).text.strip().split('Generic name:\xa0')[1].strip()
            _new_drug.url_drug = 'https://www.drugs.com'+str(name_soup).split('href="')[1].split('" onclick')[0] 
            _new_drug.num_rev = _drug_summary.find('td', {'class':'condition-table__reviews'}).text.replace('reviews', '').strip()
            try:
                _new_drug.num_rev= int(_new_drug.num_rev)
            except:
                _new_drug.num_rev = 0
            _new_drug.num_rev_pages = _new_drug.num_rev//25 + 1
            _new_drug.score = _drug_summary.find('td', {'class': 'condition-table__rating'}).text.strip()
            pop_soup = _drug_summary.find('td', {'class': 'condition-table__popularity'})
            popularity = str(pop_soup.find('div', {'class': 'meter'})).split('width:')[1].split('%')[0]
            _new_drug.url_drug_revs= 'https://www.drugs.com'+ str(_drug_summary.find('td', {'class': 'condition-table__reviews'})).split('href="')[1].split('"')[0]
            _new_drug.site_abbrev = site#self.abbrev
            return _new_drug
            
        def get_drug_metadata(self, condition, pg_init, pg_n):
            # all drugs for a condition
            # call function to build list of all drugs used to treat depression
            abbrev = self.abbrev
            drugslist_list = self.Drugslist_url_list(condition, pg_init, pg_n)
            if abbrev ==  'ddc':
                # initialize lists for two kinds of soup needed to fill drug metadata fields for ddc
                druglistsummary_soups = []
                druglistprofile_soups = []

                #for each of the drugs in the list of drugs used to treat the condition (in this case depression), get the two kinds of soup
                for url in drugslist_list:
                    soup = load_soup(url)
                    drug_summary = soup.find_all('tr', {'class': 'condition-table__summary'})
                    druglistsummary_soups= druglistsummary_soups+drug_summary
                    drug_profile = soup.find_all('tr', {'class': 'condition-profile'})
                    druglistprofile_soups = druglistprofile_soups + drug_profile

                _drug_list_ds = []
                for ik in range(len(druglistsummary_soups)):
                    new_drug = drug()
                    drug_meta = self.process_drug(druglistsummary_soups[ik], druglistprofile_soups[ik], abbrev, new_drug)
                    _drug_list_ds.append(drug_meta)
            return _drug_list_ds
        

        def get_revs_url_list(self, _new_drug):
            cond_soup = load_soup(_new_drug.url_drug_revs)
            mega = str(((cond_soup.find('div', {'id': 'contentWrap'})).find('div', {'class': 'contentBox'})))
            options = mega.split('gotoArr[')[2:-1]
            options = [(str(option).split("= '")[1]).split("';\n")[0] for option in options]
            numbers_soup = ((cond_soup.find('div', {'id': 'contentWrap'})).find('div', {'class': 'contentBox'})).find('div', {'class':'data-list-filter'}).find_all('option')[1:]
            rev_cts = [ (str(each).split('(')[1]).split(')<')[0] for each in numbers_soup]

            revs_urls = []
            cond_codes_pgs = []
            total_revs = 0
            for ik in range(len(options)):
                if 'epressi' in options[ik]:
                    cond_codes_pgs.append((options[ik], int(rev_cts[ik])))
            for cond_pg in cond_codes_pgs:
                cond = cond_pg[0]
                pg_n = int(cond_pg[1])//25
                revs_urls = revs_urls+["http://www.drugs.com"+ cond + '/?page='+ str(ik) for ik in range(1, pg_n+1)]
                total_revs +=int(cond_pg[1])
            _new_drug.num_rev_pages = total_revs
            return _new_drug, revs_urls
        
        
        # fetch information about author;
        def set_reviewerMeta (self, _rev_soup, ik):
            return _rev_soup.find('div', {'class': 'user-comment'})

            
        def set_userName (self, _reviewerMeta):
                try:
                    return _reviewerMeta.contents[0].strip()
                except:
                    return 'Anonymous'

                
        #need to fix this        
        def set_ageRange (self, _reviewerMeta):
                try:
                    temp_ar = re.search('\s\w+[-]\w+\s', _reviewerMeta).group().strip()
                    temp_ar = temp_ar.split('-')
                    return str([int(temp_ar[0]), int(temp_ar[1])]), [int(temp_ar[0]), int(temp_ar[1])]
                except:
                    return None, None
                    
                    
        #gender not specified on drugs.com
        def set_gender (self, _reviewerMeta):
                return None
            
        #role not specified on drugs.com
        def set_role(self, _rev_soup):
            return None
            
        def set_medDuration (self, _reviewerMeta):
                try: 
                    dates =  _reviewerMeta.find('span', {'class': 'tiny light'}).get_text()
                    dur = ((dates.split('taken for ')[1]).split(')')[0]).strip()
                    try:
                        return str(med_dur_conversion[dur]), med_dur_conversion[dur]
                    except:
                        return None, None
                except:
                    return None, None

                
        def set_reviewDate (self, _reviewerMeta):
                try:
                    dates =_reviewerMeta.find_all('span', {'class':"tiny light comment-date"})
                    if len(dates)>1:
                        return str(dates[1]).split('<span class="tiny light comment-date">')[1].split('</span>')[0]
                    else:
                        return str(dates[0]).split('<span class="tiny light comment-date">')[1].split('</span>')[0]
                except:
                    return None
                
                
        def set_condition (self, _reviewerMeta):
                try:
                    return 'depression'
                except:
                    return None
                
                
        #from WebMD.com
        def set_effectiveness (self, _rev_soup):
                return None
            
            
        #from WebMD.com
        def set_ease_of_use (self, _rev_soup):
                return None
            
            
        #from WebMD.com
        def set_satisfaction (self, _rev_soup):
                return None

            
        def set_genRating (self, _rev_soup):        
                try:
                    return float(_rev_soup.find('div',{'class': 'rating-score'}).get_text())
                except:
                    return None


        def set_comment (self, _rev_soup, ik):
                try:
                    return _rev_soup.find('div', {'class':'user-comment'}).span.get_text()
                except:
                    return None


        def set_upVotes (self, _rev_soup):
                try: 
                    return int(_rev_soup.find_all('p', {'class':"tiny light"})[0].b.get_text().split(' users')[0])
                except:
                    return None


                
                
# ************ webMD.com ************ Parser


class WebMD:
    
        def __init__(self, name, abbrev):
            self.name = name
            self.abbrev = abbrev
            
        #only one     
        def Drugslist_url_list(self, condition, pg_init, pg_n):
            url_list = ['https://www.webmd.com/drugs/2/condition-952/major%20depressive%20disorder']#, 
                        #'https://www.webmd.com/drugs/2/condition-1022/depression', 
                        #'https://www.webmd.com/drugs/2/condition-13493/depression%20treatment%20adjunct']
            return url_list
        
        # function to process soups to extract drug metadata
        def process_drug(self, _drug_summary, site, _new_drug):
            drug_data = _drug_summary.find_all('td')
            _new_drug.name = drug_data[0].get_text()
            _new_drug.url_drug = 'http://www.webmd.com'+str(drug_data[0]).split('a href="')[1].split('">')[0]
            name_soup = load_soup(_new_drug.url_drug)
            _new_drug.generic = str(name_soup.find('section', {'class':'generic-name'}).find('p')).split('</span>')[1].split('</p>')[0]
            _new_drug.num_rev = int((drug_data[3].get_text().split(' Reviews')[0]))
            _new_drug.num_rev_pages = _new_drug.num_rev//5 + 1
            _new_drug.url_drug_revs=  'http://www.webmd.com'+str(drug_data[3]).split('a href="')[1].split('">')[0]
            _new_drug.site_abbrev = self.abbrev
            return _new_drug
            
        def get_drug_metadata(self, condition, pg_init, pg_n):
            # all drugs for a condition
            # call function to build list of all drugs used to treat depression
            abbrev = self.abbrev
            drugslist_list = self.Drugslist_url_list(condition, pg_init, pg_n)
            # initialize lists for two kinds of soup needed to fill drug metadata fields for ddc
            druglistsummary_soups = []


            #for each of the drugs in the list of drugs used to treat the condition (in this case depression), get the two kinds of soup
            for url in drugslist_list:
                soup = load_soup(url)
                drug_summary = ((soup.find('table', {'class':'drugs-treatments-table'})).find('tbody')).find_all('tr')
                druglistsummary_soups= druglistsummary_soups+drug_summary

            _drug_list_ds = []
            for ik in range(len(druglistsummary_soups)):
                new_drug = drug()
                drug_meta = self.process_drug(druglistsummary_soups[ik], abbrev, new_drug)
                _drug_list_ds.append(drug_meta)
            return _drug_list_ds

        def get_revs_url_list(self, _new_drug):
            cond_soup = load_soup(_new_drug.url_drug_revs)
            cond_codes_pgs= []
            options = (cond_soup.find('select', {'id':'conditionFilter'})).find_all('option')
            for option in options:
                if 'epressi' in option.text:
                    cond_codes_pgs.append((str(option).split('value="')[1].split('"')[0], option.text.split('(')[1].split(' reviews')[0]))
            revs_urls = []
            total_revs = 0
            for cond_pg in cond_codes_pgs:
                cond = cond_pg[0]
                pg_n = int(cond_pg[1])//5
                revs_urls = revs_urls+ [ _new_drug.url_drug_revs+ '&pageIndex=' +str(ik) + '&sortby=3'+'&conditionFilter='+str(cond) for ik in range(0, pg_n+1)]
                total_revs +=int(cond_pg[1])
            _new_drug.num_rev = total_revs
            return _new_drug, revs_urls
        
            
        def set_reviewerMeta (self, _rev_soup, ik):
            try:
                return _rev_soup.find('p', {'class':'reviewerInfo'}).text.strip('Reviewer: ')
            except:
                return None
            

        def set_userName (self, _reviewerMeta):
            try:
                splits = _reviewerMeta.split(',')
                if len(splits)>1:
                    return splits[0]
                else:
                    return 'Anonymous'
            except:
                return 'Anonymous'

            
        def set_ageRange (self, _reviewerMeta):
            try:
                temp_ar = re.search('\s\w+[-]\w+\s', _reviewerMeta).group().strip()
                temp_ar = temp_ar.split('-')
                return str([int(temp_ar[0]), int(temp_ar[1])]), [int(temp_ar[0]), int(temp_ar[1])]
            except:
                return None, None

            
        def set_gender (self, _reviewerMeta):
            try: 
                gender = re.split('\s\w+[-]\w+\s', _reviewerMeta)[1].split()[0]
                if gender != 'on':
                    return gender 
            except: 
                return None
        
        
        def set_role(self, _rev_soup):
            try:
                return _rev_soup.find('p', {'class':'reviewerInfo'}).text.strip('Reviewer: ').split(' ')[-1].replace('(','').replace(')','')
            except:
                return None
            
            
        def set_medDuration (self, _reviewerMeta):
            try:
                dur = re.split('on Treatment for ', _reviewerMeta)[1].split('(Patient)')[0].strip()
                try:
                    return str(med_dur_conversion[dur]), med_dur_conversion[dur]
                except:
                    return None, None
            except:
                return None, None
            
            
        def set_reviewDate  (self, _rev_soup):
            try:
                return _rev_soup.find('div', {'class': 'date'}).text.split(' ',1)[0]

            except:
                return None
                
        def set_condition (self, _rev_soup):
            try:
                condition = _rev_soup.find('div', {'class': 'conditionInfo'}).text
                temp = condition.split('Condition: ')[1]
                return temp
            except:
                return None
                
        def set_effectiveness (self, _rev_soup):
                try:
                    temp = _rev_soup.find('div' ,{'class' : 'catRatings firstEl clearfix'}).text
                    return float(re.search(r'\d+', temp).group()) 
                except:
                    return None

        def set_ease_of_use (self, _rev_soup):
                try:
                    temp = _rev_soup.find('div' ,{'class' : 'catRatings clearfix'}).text
                    return float(re.search(r'\d+', temp).group())
                except:
                    return None

        def set_satisfaction (self, _rev_soup):
                try:
                    temp = _rev_soup.find('div' ,{'class' : 'catRatings lastEl clearfix'}).text
                    return float(re.search(r'\d+', temp).group())
                except:
                    return None
                
        #from drugs.com        
        def set_genRating  (self, _rev_soup):
                    return None

        def set_comment (self, _rev_soup, ik):
                try: 
                    temp = _rev_soup.find('p', {'id':'comFull'+str(ik+1)}).text
                    temp = re.split('Hide Full', temp)[0]
                    return temp.lstrip('Comment:')
                except:
                    return None

        def set_upVotes (self, _rev_soup):
                try:
                    temp = _rev_soup.find('p', {'class' : "helpful"}).text
                    return int(re.search(r'\d+', temp).group())
                except:
                    return None


############################
# revised
# by default will try to load an existing pickle file for existing all_drug_list, and will scrape if load fails or if specified to do so
def build_depression_drugs(site, pickleopt, picklename, load_or_scrape='load', num_drugs = 1):
    # Set condition
    condition = 'depression'
    def doItAll(parser, start_num, tag):
        start = time.time()
        if load_or_scrape == 'load':
            try:
                all_drugs_list = pickle.load(open( 'all_drug_list_'+site+'.p', "rb" ) )
                print('loaded list')
            except:
                print("There isn't a pickle file of drug metadata availble to work with. Now scraping metadata.")
                all_drugs_list = parser.get_drug_metadata('depression', 1, 1)
                pickle.dump( all_drugs_list, open( 'all_drug_list_'+site+'.p', "wb" ) )
        elif load_or_scrape == 'scrape':
            all_drugs_list = parser.get_drug_metadata('depression', 1, 1)
            pickle.dump( all_drugs_list, open( 'all_drug_list_'+site+'.p', "wb" ) )
            print('scraped list:', time.time()-start)
            
        drug_list = []
        generics_list = [new_drug.generic.strip(' systemic') for new_drug in all_drugs_list]

        for new_drug in all_drugs_list[:num_drugs]:
            if (new_drug.name in generics_list) or (new_drug.num_rev>=200):
                print(new_drug.name)
                drug_list.append(new_drug)
                new_drug, revs_url_list = parser.get_revs_url_list(new_drug)
                for ik, url in enumerate(revs_url_list):
                    new_drug = scrape_parse_reviews(url, new_drug, parser, tag)
                    new_drug.get_revAttrDetails()
                    drug_list[-1] = new_drug
                    pickle.dump( drug_list, open( picklename+'.p', "wb" ) )
                print('number of drugs on short list so far:', len(drug_list))
        return drug_list, all_drugs_list, generics_list

    if site == 'ddc':
        # Initialize site objects
        DDC_parser = DrugsDotCom('Drugs_dot_com', 'ddc')
        tag = 'block-wrap comment-wrap'
        filled_drug_list, all_drugs_list, generics_list = doItAll(DDC_parser,0, tag)
        
    elif site == 'wmd':
        WMD_parser = WebMD('WebMD', 'wmd')
        tag = 'userPost'
        filled_drug_list, all_drugs_list, generics_list = doItAll(WMD_parser,1, tag)
        
    return filled_drug_list, all_drugs_list, generics_list