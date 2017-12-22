import pandas as pd

# each drug has a name and a url_stem
class drug:
    
    def __init__(self):# , name):
        self.site_abbrev = ''
        self.name = '' #name
        self.generic = ''
        self.url_drug = '' #{'ddc': '', 'wmd': ''}
        self.url_drug_revs = ''
        self.reviews = []#{'ddc': '', 'wmd': ''}
        self.score = 0     
        self.num_rev = 0 #{'ddc': '', 'wmd': ''}
        self.num_rev_pages = 0
        self.attributes = []
        self.attributeDetails = {}
        self.df = ''
        
    def get_revAttrDetails(self):
        attributes = list(self.reviews[0].__dict__.keys())
        attributes.remove('comment')
        attributes.remove('medDuration')
        attributes.remove('ageRange')
        attr_opts = {}
        for attr in attributes: 
            full_list = [self.reviews[ik].__dict__[attr] for ik in range(len(self.reviews))]
            attr_opts[attr] = set(full_list)
        self.attributes = attributes
        self.attributeDetails = attr_opts
    
    def build_df(self):
        list_d = [self.reviews[ik].__dict__ for ik in range(len(self.reviews))]
        self.df = pd.DataFrame(list_d)
        
    def slice_data(self, attribute, slice_label):
        return self.df[self.df[attribute] == slice_label]

        
# for a particular drug
# Review object
class review(drug):
    
        def __init__(self, drug, _review_soup, site, ik):
            
            reviewer_info = site.set_reviewerMeta(_review_soup, ik)
            self.drugName = drug.name
            self.site = site.name
            self.condition = site.set_condition(reviewer_info)# changed, unsure of effects on wmd
            self.reviewDate = site.set_reviewDate(_review_soup)
            self.userName = site.set_userName(reviewer_info) #temp.split(',')[0]
            self.ageRange_str, self.ageRange = site.set_ageRange(reviewer_info) #re.search('\s\w+[-]\w+\s', temp).group().strip()
            self.gender = site.set_gender(reviewer_info) #re.split('\s\w+[-]\w+\s', temp)[1].split()[0]
            self.role = site.set_role(_review_soup)
            self.medDuration_str, self.medDuration = site.set_medDuration(reviewer_info) #re.split('on Treatment for ', temp)[1].split('(Patient)')[0].strip()
            self.effectiveness = site.set_effectiveness(_review_soup)
            self.ease_of_use = site.set_ease_of_use(_review_soup)
            self.satisfaction = site.set_satisfaction(_review_soup)
            self.genRating = site.set_genRating(_review_soup)
            self.comment = site.set_comment(_review_soup, ik)
            self.upVotes = site.set_upVotes(_review_soup)


class drug_dataset:
    
    def __init__(self, _one_drug_df):
        self.data, self.target = self.filter_set_data(_one_drug_df)
        self.target_names = self.set_target_names()

    def filter_set_data(self, _one_drug_df):
        abbrev = 'ddc'
        if abbrev == 'ddc':
            rating = 'genRating'
        elif _one_drug.site == 'wmd':
            rating = 'satisfaction'
            
        df_temp = _one_drug_df[['comment', rating]].dropna(thresh=2)
        data = df_temp['comment'].tolist()
        targets = df_temp[rating].tolist()

        return data, targets     

    def set_target_names(self):
        return list(set(self.target))