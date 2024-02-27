# Instuctions
## Installation 
Installed the required libraries

    pip install -r requirements.text
If it doesn't work, install `selenium` and `pandas` separately 

## Run
Run the crawler to scrape the URLS

    python crawler.py
It'll create a output file with URLS named `filtered_links.csv`

Run the scraper to scrape the Data from the URLs
  
    python scraper.py
Final output will be generated in the `output.csv` file

## Tricks
<b>1.0</b>    Sometime the code breaks. It happens when the page which is being scrapped is not responding. It can be for net connectivity or anything else. Then go to the `output.csv` and copy the link of last page it scrapped. Then find it to `filtered_links.csv`. Suppose You get it at 35th cell, You replace the link of 36th cell. 

<b>2.0</b>    You can devide the input and output file and run several times at the same time at the `scraper.py`. you just have to make a simple change in the code of `scraper.py`. Input the input file directory for `scraper.py`, the URLs file, where you get `filtered_links.csv.csv` (1 times in the code) and same for the output file `output.csv` (4 times in the code)
