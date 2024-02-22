import pandas as pd 

file_path = 'filtered_links.csv'
df = pd.read_csv(file_path)

link = 'https://mobilityex.com/#/search/service-providers/2887?svc=Moving%20Services%20Company%20&sort=companylegalname%2Casc&range=50&mocs=104&assocs=800&query=q%3D%204&spc=10'

if link in df['Links'].values:
    print('yes')
    