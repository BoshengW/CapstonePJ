import pandas as pd

def load_movieLens_dataset(path):
    
    header_rating = ['user_id', 'item_id','rating','timestamp'] ##user-movie rating matix
    header_topic = ['topic', 'catalog_idx']                     ##movie topic matrix
    header_user = ['user_id','age','gender','occupation','zip_code'] ## user meta data
    
    ## loading user-movie matrix
    df_data = pd.read_csv(path+'/u.data', sep='\t', names=header_rating)
    cvt_date_time = pd.to_datetime(df_data['timestamp'], unit='s')
    df_data['rate_datetime'] = cvt_date_time
    
    ## loading movie catalog matrix
    df_catalog = pd.read_csv(path+'/u.genre', sep='|', names=header_topic)
    
    ## loading user meta-data
    df_user_meta = pd.read_csv(path+'/u.user', sep='|', names=header_user)
    
    ## get list of topic for extract movie meta-data dataframe
    list_of_topic = df_catalog['topic'].values.tolist()
    header_movie_meta =  ['movie_id', 'name','release_date','empty','link'] + list_of_topic
    df_movie_meta = pd.read_csv(path+'/u.item', sep='|', names=header_movie_meta, 
                            encoding='latin-1', index_col=False)
    
    ## delete NaN column 'empty' based on seperating "|" 
    df_movie_meta = df_movie_meta.drop(['empty'], axis=1)
    
    
    return df_data, df_movie_meta, df_catalog, df_user_meta