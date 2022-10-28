This Python3 script scrapes data from the search page `https://web36.gov.mb.ca/school/school` about schools in Manitoba. The given webpage contains the names of all the different districts in a dropdown-box. The script loops through all of the pages for each district (some of which contain pagination) and outputs the data for each school. It writes the data into a TSV file with the following fields:

* Name

* Address

* City

* Province

* Postal code

* Phone

* Fax

* Grades

* Program

Python libraries used in the script:

* Requests

* Pandas

* BeautifulSoup

* re - Regular expression
