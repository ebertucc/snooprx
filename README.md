# SnoopRx
Herein lies our group project for Intro to Data Science. The goal of this project was to see how well textual user reviews ("comments") for prescription drugs could be used to predict their associated ratings. Or, phrased as a question: To what extent/under what conditions do user comments predict user ratings?

## Scraping
Our data sources for this project are user reviews submitted to [Drugs.com](https://www.drugs.com/) and [WebMD](https://www.webmd.com/). We scraped both sites with the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) library, although we decided to focus on drugs.com due to a combination of scraping speed and more interpretable reviews. (WebMD has three separate categories for its ratings, while drugs.com only uses one.) The scraping process is documented in the web_scrapers4.ipynb

## Cleaning
Since we're primarily interested in textual data (i.e., the review comments), an automated spellchecker would be helpful. We decided to employ the [PyEnchant](http://pythonhosted.org/pyenchant/) library to this end, and while our progress on this front is still nascent, we're optimistic that it will ultimately bear fruit. It's also worth noting that PyEnchant is essentially a wrapper for, and thus requires binaries for, the `enchant` C library, which will only run on 32bit Python.

## Exploration
The following notebooks contain explorations of drug review corpora:
 - Corpus Analysis.ipynb
 - Depression-Drugs-Data-Exploration.ipynb

## Modeling
We tried various machine learning models to predict ratings from review texts, including regression, classification, and clustering techniques. In every case, we used TF-IDF-weighted document-term matrices to train the models and made extensive use of [scikit-learn](http://scikit-learn.org/stable/index.html) These efforts are documented in the following notebooks:
 - Classifiers.ipynb
 - Clustering.ipynb
 - Regressions.ipynb

## External Packages
In order to run the various notebooks in this repo, you'll need the following packages:
 - pandas
 - numpy
 - matplotlib
 - scikit-learn
 - pyenchant
 - beautifulsoup

# TODO
 - More cleaning. 
 - Move pickle files to `data` folder.
 - Move various functions and scripts to `utils` folder.
 - Implement spellchecking.
 - Improve spellchecking.