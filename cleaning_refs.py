med_dur_conversion = {
    "less than 1 month": [0,1],
    "less than 1 month (Caregiver)": [0,1],
    "1 to 6 months":[1,6],
    "1 to 6 months (Caregiver)":[1,6],
    "6 months to less than 1 year": [6, 12],
    "6 months to less than 1 year (Caregiver)": [6, 12],
    "1 to less than 2 years (Caregiver)": [12, 24],
    "1 to less than 2 years": [12, 24],
    "2 to less than 5 years": [24, 60],
    "2 to less than 5 years (Caregiver)": [24, 60],
    "5 to less than 10 years": [60, 120],
    "10 years or more": [120, 300],
    '1 to 6 months': [1, 6],
    "5 to 10 years": [60, 120],
    "6 months to 1 year": [6, 12],
    "2 to 5 years":[24, 60],
    "less than 1 month" : [0,1]}


cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}


drug_list_all = ['hctz','ssri','snri','xr','suboxone','respirdal', 'meth','geodon','benztropine', 'valium','lyrica','melatonin','lamictal','depakote','cogentin','neurontin','nexium','hydralazine','topamax', 'ambien','provigil', 'mirapex', 'saphris','miralax','zolpidem', 'Percocet', 'adderall','risperdal','buspirone', 'lorazepam', 'ativan', 'lunesta','vistaril', 'Strattera','Clonazepam','Savella' , 'Pamelor', 'Paxil CR', 'Endep tablet', 'Irenka', 'Trintellix', 'Serzone', 'Remeron', 'clomipramine HCL', 'Viibryd', 'fluvoxamine', 'Pexeva', 'Desyrel', 'nefazodone', 'Norfranil tablet', 'Limbitrol', 'Elavil Solution', 'fluvoxamine MALEATE ER', 'Oleptro', 'doxepin HCL', 'nortriptyline', 'L-Methylfolate Forte', 'imipramine', 'Alprazolam Intensol', 'trazodone', 'vortioxetine', 'Seroquel','Ludiomil', 'escitalopram', 'Emsam', 'Etnofril tablet', 'Limbitrol DS', 'Forfivo XL', 'L-Methylfolate Formula', 'Asendin tablet', 'doxepin', 'Khedezla', 'trimipramine MALEATE', 'Budeprion SR', 'Fetzima', 'Rexulti', 'risperidone', 'protriptyline', 'E-Vill 50 tablet', 'Symbyax', 'Nardil', 'Sinequan Concentrate', 'desipramine', 'Deconil tablet', 'Triavil', 'citalopram', 'Norpramin', 'desipramine HCL', 'E-Vill 100 tablet', 'paliperidone', 'duloxetine', 'Sk-Pramine tablet', 'Budeprion XL', 'Amitid tablet', 'E-Vill 25 tablet', 'bupropion', 'venlafaxine', 'Tofranil', 'Sinequan', 'Parnate', 'Vivactil', 'isocarboxazid', 'amitriptyline HCL', 'Adapin capsule', 'atomoxetine', 'doxepin HCL capsule', 'alprazolam', 'desvenlafaxine', 'Anafranil', 'lamotrigine', 'tramadol', 'Janimine tablet', 'imipramine HCl', 'lisdexamfetamine', 'Rapiflux', 'Stabanil tablet', 'Paxil', 'aripiprazole', 'Aplenzin', 'amitriptyline / chlordiazepoxide', 'Remeron SolTab', 'sertraline', 'Aventyl Hydrochloride', 'Aventyl capsule', 'Prozac Weekly', 'l-methylfolate', 'Elavil tablet', 'Lexapro', 'Duo-Vil', 'Niravam', 'phenelzine SULFATE', 'armodafinil', 'trimipramine', 'amoxapine', 'Surmontil', 'amitriptyline Solution', 'amitriptyline', 'Effexor XR', 'Methylin ER', 'Vanatrip tablet', 'quetiapine', 'selegiline', 'amitriptyline / perphenazine', 'phenelzine', 'Wellbutrin XL', 'E-Vill 75 tablet', 'Tofranil-PM', 'Emitrip tablet', 'Enovil Solution', 'levomilnacipran', 'XaQuil XR', 'vilazodone', 'Luvox CR', 'Effexor', 'brexpiprazole', 'Zoloft', 'imipramine pamoate', 'protriptyline HCL', 'Etrafon', 'Luvox tablet', 'niacin', 'thyroid desiccated', 'Xanax', 'maprotiline', 'Pristiq', 'E-Vill 10 tablet', 'Wellbutrin', 'doxepin tablet', 'Celexa', 'Sinequan capsule', 'Abilify', 'Deplin', 'maprotiline HCL', 'Marplan', 'Imavate tablet', 'tranylcypromine', 'lithium', 'Ludiomil tablet', 'paroxetine', 'Wellbutrin SR', 'olanzapine', 'Prozac', 'modafinil', 'Kenvil tablet', 'Zyprexa Zydis', 'Zyprexa', 'Cymbalta', 'Re-Live tablet', 'fluvoxamine MALEATE', 'Asendin', 'clomipramine', 'Q.E.L tablet', 'methylphenidate', 'fluoxetine', 'Desyrel Dividose', 'Etrafon Forte', 'Seroquel XR', 'fluoxetine / olanzapine', 'mirtazapine', 'nortriptyline HCL']
drug_list = [word.lower() for word in drug_list_all]

adds_all = ['weepiness','dr', 'meds','mdd','aspergers','crittenden','walmart','wikkipedia', 'dysthymia','ocd','apnea','ptsd', 'occ','pancreatitis','electroconvulsive','neuropathy','mgs','antipsychotic','thyrotoxicosis','oculogyric','ADHD','pychotic','tricyclic','mitral', 'dyskinesia', 'hypomanic','hypomania', 'dystonic', 'tardive', 'Pristq', 'fibromyalgia', 'akathesia' ]
adds = [word.lower() for word in adds_all]

new_words = drug_list+adds