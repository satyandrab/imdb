#import urllib2
import mechanize
import cookielib
from lxml import html
global count
count = 0

import csv
# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

data_writer = csv.writer(open("imdb v1.0.csv", "wb"))
data_writer.writerow(['URL', 'Title', 'year', 'Release date', 'Genres', 'Language', 'Country', 'Main image', 'Duration', 'Rating', 'Director', 'Stars', 'Short Description', 'Story line', 'Budget', 'Opening Weekend', 'Gross','Production Company','Runtime','SoundMix', 'Color', 'Aspect Ration', 'Official Sites', 'Also Known As', 'Filming Location' ,'Writers', 'TagLines', 'Plot Keywords'])

def getMovieURL(url):
    print url
    html_response = br.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, url)
    parsed_source.make_links_absolute()
    
    url_list = parsed_source.xpath("//td[@class='title']/a/@href")
    for landing_url in url_list:
        print landing_url
        imdb(landing_url)

def imdb(url):
    print url
    
    
    html_response = br.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    f = open('test.txt','w')
    f.write(result)
    parsed_source = html.fromstring(result, url)
    parsed_source.make_links_absolute()
    
    data_list = []
    
    """ URL """
    data_list.append(url)
    
    """ item_name """
    try:
        item_name = parsed_source.xpath("//td[@id='overview-top']/h1/text()")
        print item_name
        data_list.append("".join(item_name).strip())
    except:
#        raise
        data_list.append("")
        
    """ year """
    try:
        year = parsed_source.xpath("//td[@id='overview-top']/h1/span/a/text()")
        print year
        data_list.append("".join(year).strip())
    except:
#        raise
        data_list.append("")
        
    """ release date """
    try:
        release_date = parsed_source.xpath("//time[@itemprop='datePublished']/text()")
        print release_date
        data_list.append("".join(release_date).strip())
    except:
#        raise
        data_list.append("")
        
    """ Genres """
    try:
        Genres = parsed_source.xpath("//h4[contains(text(),'Genres:')]/following-sibling::a/text()")
        print Genres
        data_list.append(", ".join(Genres).strip())
    except:
#        raise
        data_list.append("")
        
    """ language """
    try:
        language = parsed_source.xpath("//a[@itemprop='inLanguage']/text()")
        print language
        data_list.append(", ".join(language).strip())
    except:
#        raise
        data_list.append("")
        
    """ Country """
    try:
        country = parsed_source.xpath("//h4[contains(text(),'Country:')]/following-sibling::a/text()")
        print country
        data_list.append(", ".join(country).strip())
    except:
#        raise
        data_list.append("")
        
    """ Main image """
    try:
        main_image = parsed_source.xpath("//td[@id='img_primary']/a/img/@src")
        print main_image
        data_list.append("".join(main_image).strip())
    except:
#        raise
        data_list.append("")
    
    """ Duration """
    try:
        duration = parsed_source.xpath("//td[@id='overview-top']/div[2]/text()")
        print duration
        data_list.append("".join(duration).replace('-','').strip())
    except:
#        raise
        data_list.append("")
        
    """ Rating """
    try:
        rating = parsed_source.xpath("//div[@class='titlePageSprite star-box-giga-star']/text()")
        print rating
        data_list.append("".join(rating).strip())
    except:
#        raise
        data_list.append("")
        
    """ Director """
    try:
        director = parsed_source.xpath("//a[@itemprop='director']/text()")
        print director
        data_list.append("".join(director).strip())
    except:
#        raise
        data_list.append("")
        
    """ Stars """
    try:
        stars = parsed_source.xpath("//a[@itemprop='actors']/text()")
        print stars
        data_list.append(", ".join(stars[:-1]).strip())
    except:
#        raise
        data_list.append("")
        
    """ Short description """
    try:
        short_desc = parsed_source.xpath("//td[@id='overview-top']/p/text()")
        print short_desc
        data_list.append(", ".join(short_desc).strip())
    except:
#        raise
        data_list.append("")
    
    """ story line """
    try:
        story_line = parsed_source.xpath("//div[@class='article']/p/text()")
        print story_line
        data_list.append(", ".join(story_line).strip())
    except:
#        raise
        data_list.append("")
        
    """ Budget """
    try:
        budget = parsed_source.xpath("//h4[contains(text(),'Budget:')]/following::text()[1]")
        print budget
        data_list.append(", ".join(budget).strip())
    except:
#        raise
        data_list.append("")
        
    """ Opening Weekend """
    try:
        opening_weekend = parsed_source.xpath("//h4[contains(text(),'Opening Weekend:')]/following::text()[1]")
        print opening_weekend
        data_list.append(", ".join(opening_weekend).strip())
    except:
#        raise
        data_list.append("")
        
    """ Gross """
    try:
        gross = parsed_source.xpath("//h4[contains(text(),'Gross:')]/following::text()[1]")
        print gross
        data_list.append(", ".join(gross).strip())
    except:
#        raise
        data_list.append("")
        
    """ Production Company """
    try:
        product_company = parsed_source.xpath("//div[h4[contains(text(),'Production Co:')]]/a/text()")
        print product_company
        data_list.append(", ".join(product_company).strip())
    except:
#        raise
        data_list.append("")
        
        
    """  Runtime """
    try:
        run_time = parsed_source.xpath("//div[h4[contains(text(),'Runtime:')]]/time/text()")
        print run_time
        data_list.append(", ".join(run_time).strip())
    except:
#        raise
        data_list.append("")
        
    
    """  SoundMix """
    try:
        sound_mix = parsed_source.xpath("//div[h4[contains(text(),'Sound Mix:')]]/a/text()")
        print sound_mix
        data_list.append(", ".join(sound_mix).strip())
    except:
#        raise
        data_list.append("")
        
        
    """  Color """
    try:
        color = parsed_source.xpath("//div[h4[contains(text(),'Color:')]]/a/text()")
        print color
        data_list.append(", ".join(color).strip())
    except:
#        raise
        data_list.append("")
        
    """ Aspect Ration """
    try:
        aspect_ration = parsed_source.xpath("//div[h4[contains(text(),'Aspect Ratio:')]]/text()[1]")
        print aspect_ration
        data_list.append(", ".join(aspect_ration).strip())
    except:
#        raise
        data_list.append("")
        
    """ Official Sites """
    try:
        official_sites = parsed_source.xpath("//div[h4[contains(text(),'Official Sites:')]]/a/text()")
        print official_sites
        data_list.append(", ".join(official_sites).strip())
    except:
#        raise
        data_list.append("")
        
    """ Also Known As """
    try:
        also_known_as = parsed_source.xpath("//div[h4[contains(text(),'Also Known As:')]]/text()[1]")
        print also_known_as
        data_list.append(", ".join(also_known_as).strip())
    except:
#        raise
        data_list.append("")
        
    """ Filming Location """
    try:
        filming_location = parsed_source.xpath("//div[h4[contains(text(),'Filming Locations:')]]/a/text()")
        print filming_location
        data_list.append(", ".join(filming_location).strip())
    except:
#        raise
        data_list.append("")
        
    """ Writers """
    try:
        writers = parsed_source.xpath("//div[h4[contains(text(),'Writers:')]]/a/text()")
        print writers
        data_list.append("".join(writers).strip())
    except:
#        raise
        data_list.append("")
        
    """ TagLines """
    try:
        tag_lines = parsed_source.xpath("//div[h4[contains(text(),'Taglines:')]]/text()[1]")
        print tag_lines
        data_list.append("".join(tag_lines).strip())
    except:
#        raise
        data_list.append("")
        
    """ Plot Keywords """
    try:
        plot_keywords = parsed_source.xpath("//div[h4[contains(text(),'Plot Keywords:')]]/a/text()")
        print plot_keywords
        data_list.append(" , ".join(plot_keywords).strip())
    except:
#        raise
        data_list.append("")
        
        
    print '+'*78
    try:
        if item_name:
            data_writer.writerow(data_list)
            print data_list
    except:
        pass
    print '+'*78

if __name__ == '__main__':
    #url = 'http://www.imdb.com/title/tt0172495/'
    #imdb(url)
    
    for i in range(1, 3600, 50):
        print i
        url = 'http://www.imdb.com/search/title?sort=moviemeter,asc&start='+str(i)+'&title_type=feature&year=2000,2000'
        getMovieURL(url)
