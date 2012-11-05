#import urllib2
import mechanize
import cookielib
from lxml import html
import re
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

data_writer = csv.writer(open("imdb v3.0.csv", "wb"))
data_writer.writerow(['URL', 'Title', 'year', 'Release date', 'Official Sites', 'box office/business', 'Genres', 'Language', 'Country', 'Main image', 'Duration', 'Rating',
                      'Director', 'Stars', 'Short Description', 'Plot Summary', 'synopsis', 'Parents Guide', 'Connections', 
                      'Sound Tracks', 'Budget', 'Opening Weekend', 'Gross','Production Company',
                      'Runtime','SoundMix', 'Color', 'Aspect Ration', 'Official Sites', 'Also Known As', 'Filming Location' ,'Technical Specs',
                       'Writers', 'TagLines', 'Plot Keywords', 'Literature', 'Trailers and Videos', 'Awards'])

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
        
    """ release dates """
    try:
        release_dates_url = url+'releaseinfo'
        release_dates_html_response = br.open(release_dates_url)
        release_dates_html_source = release_dates_html_response.read()
        release_dates_result = release_dates_html_source.replace('\n', '').replace('\r', '')
        release_dates_parsed_source = html.fromstring(release_dates_result, release_dates_url)
        release_dates_parsed_source.make_links_absolute()
        
        release_dates_re = re.compile('<table border="0" cellpadding="2">(.*?)</table')
        release_dates = release_dates_re.findall(str(release_dates_result))
        data_list.append(" ".join(release_dates).strip())
    except:
#        raise
        data_list.append("")
        
    """ official sites """
    try:
        official_sites_url = url+'officialsites'
        officialsites_html_response = br.open(official_sites_url)
        officialsites_html_source = officialsites_html_response.read()
        officialsites_result = officialsites_html_source.replace('\n', '').replace('\r', '')
        officialsites_parsed_source = html.fromstring(officialsites_result, official_sites_url)
        officialsites_parsed_source.make_links_absolute()
        
        release_dates_re = re.compile('<ol>(.*?)</ol')
        release_dates = release_dates_re.findall(str(officialsites_result))
        data_list.append(" ".join(release_dates).strip())
    except:
#        raise
        data_list.append("")
        
    """ box office/business """
    try:
        business_url = url+'business'
        business_html_response = br.open(business_url)
        business_html_source = business_html_response.read()
        business_result = business_html_source.replace('\n', '').replace('\r', '')
        business_parsed_source = html.fromstring(business_result, business_url)
        business_parsed_source.make_links_absolute()
        
        business_re = re.compile('<div id="tn15content">(.*?)<h5>Copyright Holder</h5>')
        business = business_re.findall(str(business_result))
        data_list.append(" ".join(business).strip())
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
        print '*'*78
        story_line_url = url+'plotsummary'
        story_line_html_response = br.open(story_line_url)
        story_line_html_source = story_line_html_response.read()
        story_line_result = story_line_html_source.replace('\n', '').replace('\r', '')
        story_line_parsed_source = html.fromstring(story_line_result, story_line_url)
        story_line_parsed_source.make_links_absolute()
        
        plot_summary_re = re.compile('<p class="plotpar">(.*?)</p>')
        plot_summary = plot_summary_re.findall(str(story_line_result))
        data_list.append(" ".join(plot_summary).strip())
    except:
#        raise
        data_list.append("")
        
    """ synopsis """
    try:
        synopsis_url = url+'synopsis'
        synopsis_html_response = br.open(synopsis_url)
        synopsis_html_source = synopsis_html_response.read()
        synopsis_result = synopsis_html_source.replace('\n', '').replace('\r', '')
        synopsis_parsed_source = html.fromstring(synopsis_result, synopsis_url)
        synopsis_parsed_source.make_links_absolute()
        
        synopsis_re = re.compile('<div id="swiki.2.1">(.*?)</div>')
        synopsis = synopsis_re.findall(str(synopsis_result))
        data_list.append(" ".join(synopsis).strip())
    except:
#        raise
        data_list.append("")
        
    """ parentalguide """
    try:
        parentalguide_url = url+'parentalguide'
        parentalguide_html_response = br.open(parentalguide_url)
        parentalguide_html_source = parentalguide_html_response.read()
        parentalguide_result = parentalguide_html_source.replace('\n', '').replace('\r', '')
        parentalguide_parsed_source = html.fromstring(parentalguide_result, parentalguide_url)
        parentalguide_parsed_source.make_links_absolute()
        
        parentalguide_re = re.compile('<div id="swiki_body">(.*?)<div id="swiki_control2')
        parentalguide = parentalguide_re.findall(str(parentalguide_result))
        data_list.append(" ".join(parentalguide).strip())
    except:
#        raise
        data_list.append("")

    """ Connections """
    try:
        Connections_url = url+'trivia?tab=mc'
        Connections_html_response = br.open(Connections_url)
        Connections_html_source = Connections_html_response.read()
        Connections_result = Connections_html_source.replace('\n', '').replace('\r', '')
        Connections_parsed_source = html.fromstring(Connections_result, Connections_url)
        Connections_parsed_source.make_links_absolute()
        
        Connections_re = re.compile('<div id="main">(.*?)<script type="text/javascript">')
        Connections = Connections_re.findall(str(Connections_result))
        data_list.append(" ".join(Connections).strip())
    except:
#        raise
        data_list.append("")

    """ soundtracks """
    try:
        soundtrack_url = url+'soundtrack'
        soundtracks_html_response = br.open(soundtrack_url)
        soundtracks_html_source = soundtracks_html_response.read()
        soundtracks_result = soundtracks_html_source.replace('\n', '').replace('\r', '')
        soundtracks_parsed_source = html.fromstring(soundtracks_result, soundtrack_url)
        soundtracks_parsed_source.make_links_absolute()
        
        soundtrack_re = re.compile('<ul class="trivia">(.*?)</ul>')
        soundtrack = soundtrack_re.findall(str(soundtracks_result))
        data_list.append(" ".join(soundtrack).strip())
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
        data_list.append(", ".join(also_known_as).strip().encode())
    except:
#        raise
        data_list.append("")
        
    """ Filming Location """
    try:
        locations_url = url+'locations'
        locations_html_response = br.open(locations_url)
        locations_html_source = locations_html_response.read()
        locations_result = locations_html_source.replace('\n', '').replace('\r', '')
        locations_parsed_source = html.fromstring(locations_result, locations_url)
        locations_parsed_source.make_links_absolute()
        
        locations_re = re.compile('<dl>(.*?)</dl>')
        locations = locations_re.findall(str(locations_result))
        data_list.append(" ".join(locations).strip())
    except:
#        raise
        data_list.append("")
        
    """ Technical Specs  """
    try:
        technical_url = url+'technical'
        technical_html_response = br.open(technical_url)
        technical_html_source = technical_html_response.read()
        technical_result = technical_html_source.replace('\n', '').replace('\r', '')
        technical_parsed_source = html.fromstring(technical_result, technical_url)
        technical_parsed_source.make_links_absolute()
        
        technical_re = re.compile('<div id="tn15content">.*?<h5>(.*?)<h3>Related Links</h3>')
        technical = technical_re.findall(str(technical_result))
        data_list.append(" ".join(technical).strip())
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
        
    """ literature  """
    try:
        literature_url = url+'literature'
        literature_html_response = br.open(literature_url)
        literature_html_source = literature_html_response.read()
        literature_result = literature_html_source.replace('\n', '').replace('\r', '')
        literature_parsed_source = html.fromstring(literature_result, literature_url)
        literature_parsed_source.make_links_absolute()
        
        literature_re = re.compile('<div id="tn15content">.*?<h5>(.*?)<div id="tn15bot">')
        literature = literature_re.findall(str(literature_result))
        data_list.append(" ".join(literature).strip())
    except:
#        raise
        data_list.append("")
        
    """ trailers and videos  """
    try:
        videogallery_url = url+'videogallery'
        videogallery_html_response = br.open(videogallery_url)
        videogallery_html_source = videogallery_html_response.read()
        videogallery_result = videogallery_html_source.replace('\n', '').replace('\r', '')
        videogallery_parsed_source = html.fromstring(videogallery_result, videogallery_url)
        videogallery_parsed_source.make_links_absolute()
        
        videogallery = videogallery_parsed_source.xpath("//div[@class='slate']/a/@href")
        data_list.append(", ".join(videogallery).strip())
    except:
#        raise
        data_list.append("")

    """ Awards  """
    try:
        awards_url = url+'awards'
        awards_html_response = br.open(awards_url)
        awards_html_source = awards_html_response.read()
        awards_result = awards_html_source.replace('\n', '').replace('\r', '')
        awards_parsed_source = html.fromstring(awards_result, awards_url)
        awards_parsed_source.make_links_absolute()
        
        awards_re = re.compile('<div id="tn15content">.*?<table.*?>(.*?)<h3>Related Links</h3>')
        awards = awards_re.findall(str(awards_result))
        data_list.append(" ".join(awards).strip())
    except:
#        raise
        data_list.append("")

        
    print '+'*78
    #try:
    temp_list = []
    for data_point in data_list:
        data = data_point.encode('utf-8')
        temp_list.append(data)
    
    if item_name:
        data_writer.writerow(temp_list)
        print temp_list
    #except:
    #    pass
    print '+'*78

if __name__ == '__main__':
    url = 'http://www.imdb.com/title/tt0181984'
    imdb(url)

#    url = 'http://www.imdb.com/search/title?sort=moviemeter,asc&start=101&title_type=feature&year=2000,2000'
#    getMovieURL(url)
    
#    for i in range(1, 3600, 50):
#        print i
#        url = 'http://www.imdb.com/search/title?sort=moviemeter,asc&start='+str(i)+'&title_type=feature&year=2000,2000'
#        getMovieURL(url)