from BeautifulSoup import BeautifulSoup
import mechanize
from BeautifulSoup import SoupStrainer
import sys

URL ="http://www.transportdirect.info/transportdirect/en/journeyplanning/jplandingpage.aspx?id=gman.me.uk&do=p&d=SW113TP&oo=en&on=cellID%20location&o=339892,405924&p=1"


####################################################################
def main(url):

    br = mechanize.Browser()
    br.set_handle_robots(False)
    if url == None or url == "default":
        url = URL

    br.open(url)
    br.select_form(name='JourneyDetails')
    #get journey details in table form as it makes this easier to parse
    br.submit(name='buttonShowTableOutward')
    html = br.response().read()
    """
    f = open("test.html", "r")
    html = f.read()
    f.close()
    """

    soup = BeautifulSoup(html, parseOnlyThese=SoupStrainer('table'))

    table = soup.find('table', 'jdetail').extract()
    tbody = table.tbody
    rows = tbody.findAll('tr')

    journeys = []
    for row in rows:
        cells = row.findAll('td')
        indivJourney = []
        #list: [modes, changes, start, end, duration]
        for index, cell in enumerate(cells):
            cell = cell.string
            if index == 0:
                #this is the modes of transport.
                transList = cell.lower().split(', ')
                for index, modes in enumerate(transList):
                    #to get parity with my tfl scraper and tfl terms
                    if modes == "underground":
                        transList[index] = "tube"
                    if modes == "ferry":
                        transList[index] = "river"
                indivJourney.append(transList)
            else:
                indivJourney.append(cell)
        journeys.append(indivJourney)

    #get the individual legs of each journey option
    for index, journey in enumerate(journeys):
        jDetails = []

        #don't waste time if it's via car as I don't car about driving
        if str(journey[0][0]) != "car":
            #now get the individual journey details
            jdTable = soup.find('table', 'jdtgrid').extract()
            jdTbody = jdTable.tbody
            jdRows = jdTbody.findAll('tr')
            for jdRow in jdRows:
                indivLeg = []
                cells = jdRow.findAll('td')
                for cell in cells:
                    text = ""
                    #each cell also has html formatting so we need to
                    #extract the data from each tag and collate them together
                    for content in cell.contents:
                        try:
                            text = text + content.contents[0].strip() + " " 
                        except:
                            if content.string is not None:
                                text = text + content.string.strip()
                    
                    #print text
                    #print "--------"
                    indivLeg.append(text)
                #print "#####"
                jDetails.append(indivLeg)

            journeys[index][-1] = jDetails

            #submit form with next leg clicked!
            buttonName = "summaryResultTableControlOutward$summaryRepeater$ctl0%s$ImageButton" % str(index + 2)
            br.select_form(name='JourneyDetails')
            br.submit(name=buttonName)
            html = br.response().read()
            soup = BeautifulSoup(html, parseOnlyThese=SoupStrainer('table'))

    return journeys

####################################################################
if __name__ == "__main__":
    main(sys.argv[1])
