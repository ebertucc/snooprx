from bs4 import BeautifulSoup as bf
import requests
import re
import pickle
from collections import defaultdict



#utility methods
def load_soup(url):
    html = requests.get(url).text
    soup = bf(html, 'html5lib')
    return soup

# takes url list, scrapes, returns pages of soup
def scraper(url_list):
    soup_list = []
    for url in url_list:
        soup_list.append( [url, load_soup(url)])
    return soup_list 


# for a particular drug
# uses methods from the two parser classes to slice and dice soup into review objects
# should be a "site" method...
def parse_reviews(pages, drug, parser, tag):
    for page in pages:
        rev_stew = page[1].find_all('div' ,{'class' : tag})
        for ik, item in enumerate(rev_stew):
            new_review = review(drug, item, parser, ik)
            drug.reviews.append(new_review)
            
                     
# each drug has a name and a url_stem
class drug:
    
    def __init__(self):# , name):
        self.name = '' #name
        self.generic = ''
        self.url_drug = '' #{'ddc': '', 'wmd': ''}
        self.url_drug_revs = ''
        self.reviews = []#{'ddc': '', 'wmd': ''}
        self.score = 0     
        self.num_rev = 0 #{'ddc': '', 'wmd': ''}
        self.num_rev_pages = 0

        
# for a particular drug
# Review object
class review(drug):
    
        def __init__(self, drug, _review_soup, site, ik):
            
            reviewer_info = site.set_reviewerMeta(_review_soup, ik)
            self.drugName = drug.name
            self.site = site.name
            self.condition = site.set_condition(_review_soup)
            self.reviewDate = site.set_reviewDate(_review_soup)
            self.userName = site.set_userName(reviewer_info) #temp.split(',')[0]
            self.ageRange = site.set_ageRange(reviewer_info) #re.search('\s\w+[-]\w+\s', temp).group().strip()
            self.gender = site.set_gender(reviewer_info) #re.split('\s\w+[-]\w+\s', temp)[1].split()[0]
            self.role = site.set_role(_review_soup)
            self.medDuration = site.set_medDuration(reviewer_info) #re.split('on Treatment for ', temp)[1].split('(Patient)')[0].strip()
            self.effectiveness = site.set_effectiveness(_review_soup)
            self.ease_of_use = site.set_ease_of_use(_review_soup)
            self.satisfaction = site.set_satisfaction(_review_soup)
            self.genRating = site.set_genRating(_review_soup)
            self.comment = site.set_comment(_review_soup, ik)
            self.upVotes = site.set_upVotes(_review_soup)




            
            
# ************ Drugs.com ************  Parser

# modified from source: 
# https://blog.nycdatascience.com/student-works/web-scraping/anti-epileptic-drug-review-analysis/

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
            return _new_drug
            
        def get_drug_metadata(self, condition, pg_init, pg_n):
            # all drugs for a condition
            #call function to build list of all drugs used to treat depression
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
#                     print(drug_meta.__dict__)
            return _drug_list_ds
        

        def get_revs_url_list(self, _new_drug):
            cond_soup = load_soup(_new_drug.url_drug_revs)
            mega = str(((cond_soup.find('div', {'id': 'contentWrap'})).find('div', {'class': 'contentBox'})))#.find('div', {'class':'responsive-table-wrap-mobile'})
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
        # bug fix: added a tag to the tags list.  There may be more lurking...
        def set_reviewerMeta (self, _rev_soup, ik):
            tags = ['user-name user-type user-type-2_non_member', 'user-name user-type user-type-1_standard_member','user-name user-type user-type-0_select_member']
            if _rev_soup.find('p', {'class': tags[0]}):
                return _rev_soup.find('p', {'class': tags[0]})
            elif _rev_soup.find('p', {'class': tags[1]}):
                return _rev_soup.find('p', {'class': tags[1]})
            elif _rev_soup.find('p', {'class': tags[2]}):
                return _rev_soup.find('p', {'class': tags[2]})
            else:
                return None
            
        def set_userName (self, _reviewerMeta):
                try:
                    return _reviewerMeta.contents[0].strip()
                except:
                    return 'Anonymous'

                
        #need to fix this        
        def set_ageRange (self, _reviewerMeta):
                try:
                    return re.search('\s\w+[-]\w+\s', _reviewerMeta).group().strip()
                except:
                    return None
                    
                    
        #gender not specified on drugs.com
        def set_gender (self, _reviewerMeta):
                return None
            
        #role not specified on drugs.com
        def set_role(self, _rev_soup):
            return None
            
        def set_medDuration (self, _reviewerMeta):
                try: 
                    dates =_reviewerMeta.find_all('span')#, {'class':'small light'})
                    if len(dates)>1:
                        return str(dates[0]).split('<span class="tiny light">(taken for')[1].split(')</span>')[0].strip()
                except:
                    return None

                
        def set_reviewDate (self, _reviewerMeta):
                try:
                    dates =_reviewerMeta.find_all('span', {'class':"tiny light comment-date"})
                    if len(dates)>1:
                        return str(dates[1]).split('<span class="tiny light comment-date">')[1].split('</span>')[0]
                    else:
                        return str(dates[0]).split('<span class="tiny light comment-date">')[1].split('</span>')[0]
                except:
                    return None
                
                
        def set_condition (self, _rev_soup):
                try:
                    return _rev_soup.find('div', {'class':'user-comment'}).b.get_text()
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
                    return int(_rev_soup.find('div',{'class': 'rating-score'}).get_text())
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
            _new_drug.url_drug_revs=  'http://www.webmd.com'+str(drug_data[3]).split('a href="')[1].split('">')[0]#.split('href="')[1].split('"')[0]
#             print(_new_drug.url_drug_revs[site])
            return _new_drug
            
        def get_drug_metadata(self, condition, pg_init, pg_n):
            # all drugs for a condition
            #call function to build list of all drugs used to treat depression
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
#                 print(drug_meta.__dict__)
            return _drug_list_ds

        def get_revs_url_list(self, _new_drug):
            cond_soup = load_soup(_new_drug.url_drug_revs)
            print(_new_drug.url_drug_revs)
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
#     url_list = [url_c[0] + drug_stem + url_c[1] +str(ik) + url_c[2] for ik in range(pg_init, pg_n+1)]
                revs_urls = revs_urls+ [ _new_drug.url_drug_revs+ '&pageIndex=' +str(ik) + '&sortby=3'+'&conditionFilter='+str(cond) for ik in range(0, pg_n+1)]
#                 url_list = [ _new_drug.url_drug_revs[site]+ url_c[1] +str(ik) + url_c[2]+url_c[3] for ik in range(pg_init, pg_n+1)]
#                 revs_urls = revs_urls+revs_url_list(new_drug, start_num, pg_n, WMD_parser.abbrev, cond)
                total_revs +=int(cond_pg[1])
            _new_drug.num_rev = total_revs
            return _new_drug, revs_urls
        
            
        def set_reviewerMeta (self, _rev_soup, ik):
            try:
                return _rev_soup.find('p', {'class':'reviewerInfo'}).text.strip('Reviewer: ')
            except:
                return None
            
        #below takes reviewer soup
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
                return re.search('\s\w+[-]\w+\s', _reviewerMeta).group().strip()
            except:
                return None

        def set_gender (self, _reviewerMeta):
            try: 
                return re.split('\s\w+[-]\w+\s', _reviewerMeta)[1].split()[0]
            except: 
                return None
        
        def set_role(self, _rev_soup):
            try:
                return _rev_soup.find('p', {'class':'reviewerInfo'}).text.strip('Reviewer: ').split(' ')[-1].replace('(','').replace(')','')
            except:
                return None
            
        def set_medDuration (self, _reviewerMeta):
            try:
                return re.split('on Treatment for ', _reviewerMeta)[1].split('(Patient)')[0].strip()
            except:
                return None
            
        #below takes full soup
        #untested for webMD
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
                    return int(re.search(r'\d+', temp).group())
                except:
                    return None

        def set_ease_of_use (self, _rev_soup):
                try:
                    temp = _rev_soup.find('div' ,{'class' : 'catRatings clearfix'}).text
                    return int(re.search(r'\d+', temp).group())
                except:
                    return None

        def set_satisfaction (self, _rev_soup):
                try:
                    temp = _rev_soup.find('div' ,{'class' : 'catRatings lastEl clearfix'}).text
                    return int(re.search(r'\d+', temp).group())
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

                
def build_depression_drugs(site, pickleopt, picklename):
    # Set condition
    condition = 'depression'
    def doItAll(parser, start_num, tag):
        start = time.time()
        all_drugs_list = parser.get_drug_metadata('depression', 1, 1)
        print('got list:', time.time()-start)
        drug_list = []
        generics_list = [new_drug.generic.strip(' systemic') for new_drug in all_drugs_list]
        print('number of generics:', len(generics_list))

        for new_drug in all_drugs_list:
            if (new_drug.name in generics_list) or (new_drug.num_rev>=200):
                print(new_drug.name)
#                 new_drug_Soup = scraper([new_drug.url_drug_revs[parser.abbrev]])
                new_drug, revs_url_list = parser.get_revs_url_list(new_drug)
#                 print(revs_url_list)
                new_drug_Soup = scraper(revs_url_list)
                print('scraped sites:', time.time()- start)
                parse_reviews(new_drug_Soup, new_drug, parser, tag)
                print('parsed reviews:', time.time()- start)
                drug_list.append(new_drug)
                print('number of drugs on short list so far:', len(drug_list))
#             print(len(new_drug.reviews[parser.abbrev]))
            print('got first drug:', time.time())
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
        
    if pickleopt =='y':
        pickle.dump( filled_drug_list, open( picklename+'.p', "wb" ) )
        
    return filled_drug_list, all_drugs_list, generics_list
        