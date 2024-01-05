# Author: Wojciech Pechmann

import re,csv, os
from django.conf import settings
import uuid

import datetime 
  

#from marketpulse.settings import BASE_DIR

class TweetCleanerUtils:
    def clean_tweet(nstr):
        """
        Parameters
        ----------
        nstr : str
            A string row (eg. from a CSV file), while iterating,
            sent in for filtering/cleaning based on the below reg-ex.

        Returns
        ----------
        nstr : str
            Cleaned string.
        """
        # Links
        nstr = re.sub('http(?:[\d\w]|[^\s\d\w])+','user',nstr)
        # Users
        nstr = re.sub('\@[\w\d]+','user',nstr)

        # 's 'd
        nstr = re.sub('\'[sd]','',nstr)

        #trailing s
        nstr = re.sub('(\w{2,})s[\b$]',r'\1',nstr)

        # Stock codes
        nstr = re.sub('(?:(?: |\t|^)\$?(?:(?:[A-HJ-Z]{1})|(?:[A-Z]{2,})))+(?:$| |\t)',' stck ',nstr)

        #NUMBERS
        nstr = re.sub('\d+[\,\.\-]*\d*',' NMBR ',nstr)

        #Any symbols
        nstr = re.sub('[^\s\d\w]',' ',nstr)

        #Spaces
        nstr = re.sub('[ \t]+',' ',nstr)

        #Repeat N
        nstr = re.sub('(?:NMBR\s)+','NMBR ',nstr)

        #Spaces
        nstr = re.sub('[ \t]+',' ',nstr)

        #to lower case
        nstr = nstr.lower()

        return nstr


    def clean_labeled_CSV(input_file: str, destination: str, textCol: str, lblCol: str):
        """
        Cleans a labeled CSV file and saves the output to another CSV with the labels from the original file

        Parameters
        ----------
        input_file : str
            Path of the CSV file with raw tweets, containing unimportant 
            fragments like usernames, special characters, etc. .

        destination : str
            Path of the CSV file that will have the clean text. If no file is present, it will be created.

        textCol: str
            Name of the column with the text to clena in the original CSV
        
        lblCol: str
            Name of the column with the labels in the original CSV
        """

        input_file = os.path.join(settings.BASE_DIR, 'server/application/prediction/sentiment_model/', input_file)
        
        W_TXT_COL_NAME = 'text'
        W_LBL_COL_NAME = 'label'

        f=open(input_file, encoding="utf-8", newline='')

        processed_file = open(destination, mode="+w",encoding="utf-8",newline='')

        reader = csv.DictReader(f)
        writer = csv.DictWriter(processed_file, fieldnames=[W_TXT_COL_NAME, W_LBL_COL_NAME])

        r = {W_TXT_COL_NAME: W_TXT_COL_NAME,W_LBL_COL_NAME: W_LBL_COL_NAME}
        writer.writerow(r)

        for row in reader:
            clean = TweetCleanerUtils.clean_tweet(row[textCol])

            r = {W_TXT_COL_NAME: clean,W_LBL_COL_NAME: row[lblCol]}
            writer.writerow(r)




    def clean_CSV(input_file: str, destination: str, textCol: str):
        """
        Cleans all text rows in a CSV file and saves the output to another CSV file

        Parameters
        ----------
        input_file : str
            Path of the CSV file with raw tweets, containing unimportant 
            fragments like usernames, special characters, etc. .

        destination : str
            Path of the CSV file that will have the clean text. If no file is present, it will be created.

        textCol: str
            Name of the column with the text to clena in the original CSV
        """

        W_TXT_COL_NAME = 'Text'

        f=open(input_file, encoding="utf-8", newline='')

        processed_file = open(destination, mode="+w",encoding="utf-8",newline='')

        reader = csv.DictReader(f)
        writer = csv.DictWriter(processed_file, fieldnames=[W_TXT_COL_NAME])

        r = {W_TXT_COL_NAME: W_TXT_COL_NAME}
        writer.writerow(r)

        for row in reader:
            clean = TweetCleanerUtils.clean_tweet(row[textCol])
            r = {W_TXT_COL_NAME: clean}
            writer.writerow(r)


    #Helper method used to migrate the training csv files to the db
    def custom_clean():
        input_file = './unclean_2.csv'
        destination='./mig_train4.csv'
        textCol='text'
        lblCol='label'

        

        d = datetime.datetime(2023,12,4) 

        f=open(input_file, encoding="utf-8", newline='')

        processed_file = open(destination, mode="+w",encoding="utf-8",newline='')

        reader = csv.DictReader(f)
        writer = csv.DictWriter(processed_file, fieldnames=['_id','unclean','clean','sentiment','created_at'])

        r = {'_id':'_id','unclean': 'unclean','clean': 'clean','sentiment':'sentiment','created_at':'created_at'}
        writer.writerow(r)
    
        for row in reader:
            clean = TweetCleanerUtils.clean_tweet(row[textCol])

            r = {'_id':uuid.uuid4(),'unclean':row[textCol],'clean': clean,'sentiment':row[lblCol],'created_at':d}
            writer.writerow(r)

    def normalizeSentiment(num):
        match(num):
            case 0:
                return -1
            case 1:
                return 1
            case 2:
                return 0
            case '0':
                return -1
            case '1':
                return 1
            case '2':
                return 0
            case 'positive':
                return 1
            case 'neutral':
                return 0
            case 'negative':
                return -1
            

    def custom_csv_sub(input_file,destination):
        #input_file = './mig_train2.csv'
        #destination='./mig_train4.csv'
        

        d = datetime.datetime(2023,12,4) 

        f=open(input_file, encoding="utf-8", newline='')

        processed_file = open(destination, mode="+w",encoding="utf-8",newline='')

        reader = csv.DictReader(f)
        writer = csv.DictWriter(processed_file, fieldnames=['_id','unclean','clean','sentiment','created_at'])

        r = {'_id':'_id','unclean': 'unclean','clean': 'clean','sentiment':'sentiment','created_at':'created_at'}
        writer.writerow(r)
    
        for row in reader:
            unchanged = row['sentiment']

            changed = TweetCleanerUtils.normalizeSentiment(unchanged)

            r = {'_id':row['_id'],'unclean':row['unclean'],'clean': row['clean'],'sentiment':changed,'created_at':row['created_at']}
            writer.writerow(r)

        
 



