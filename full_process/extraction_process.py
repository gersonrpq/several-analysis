from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta
import time
import argparse
import logging
import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


#TOPIC = '/g/11hczw_m64' # Id google Indexed Topic
COUNTRIES = ['ES','MX']
TIMEZONE = 60 # Central Europe Time zone
HL = 'es-ES' # Language Looked

TrendRequester = TrendReq(hl=HL,
                         tz=TIMEZONE)


def extract_process_behaviour(keyword, location, starting_date, requester : TrendReq = TrendRequester, timeframe = 'today 5-y'):
    flag = False
    new_data = pd.DataFrame()
    ending_date = datetime.now().strftime('%Y-%m-%d')
    tiempo = f"{starting_date} {ending_date}"
    while not flag:
        try:
            requester.build_payload(kw_list=[keyword],cat=0,geo=location, timeframe=tiempo)
            new_data =  requester.interest_over_time()
            new_data = new_data.reset_index()
            new_data['Country'] = location
            flag = True
        except Exception as error:
            
            logger.info(f"Error {error} has happened while extracting keyword behaviour")
            logger.info(f'Waiting 15 seconds for the next {location} behaviour request')
            time.sleep(15)
    return new_data

def extract_process_similar_subject(keyword, location, requester : TrendReq = TrendRequester, timeframe = 'today 5-y'):
    flag = False
    top, rising = pd.DataFrame(), pd.DataFrame()
    while not flag:
        try:
            requester.build_payload(kw_list=[keyword],cat=0,geo=location, timeframe=timeframe)
            new_data =  requester.related_topics()
            subject = list(new_data.keys())[0]
            top, rising = new_data[subject]['top'], new_data[subject]['rising']
            flag = True
        except Exception as error:
            
            logger.info(f"Error {error} has happened")
            logger.info(f'Waiting 15 seconds for {location} request while extracting top and rising terms')
            time.sleep(15)
    return top, rising



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script getting trends of keywords')
    parser.add_argument('keyword',default='eSim', help='Keyword to search')

    args = parser.parse_args()
    KEY = args.keyword
    
    starting_date = (datetime.now() - timedelta(days=365*3)).strftime('%Y-%m-%d')

    logger.info('Starting Extraction Process')

    for country in COUNTRIES:
        logger.info(f'Starting {country} extraction')

        logger.info(f'Extracting {country} keyword behaviour')
        behaviour_data = extract_process_behaviour(KEY,country,starting_date)
        behaviour_data.to_csv(f'./tmp/{country}_behaviour_{KEY}.csv',index=False)
        logger.info(f'Extraction {country} keyword behaviour DONE')
        
        logger.info(f'Extracting {country} keyword top and rising topics')
        top, rising = extract_process_similar_subject(KEY, country)
        
        top.to_csv(f'./tmp/{country}_top_{KEY}.csv',index=False)
        rising.to_csv(f'./tmp/{country}_rising_{KEY}.csv',index=False)
        logger.info(f'Extraction {country} keyword top and rising topics DONE')

        
        logger.info(f'Ending {country} extraction')

    logger.info('Extraction Process ended')    