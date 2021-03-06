#%%
import requests
import re 
from bs4 import BeautifulSoup
import datetime
import julian
from colorama import init
from termcolor import colored

def save_as_file(string, filename):
    with open(filename,"w") as f:
        f.write(string)

def convert_to_jd(datetime_tuple):
    # time = (2019, 12, 31, 0, 0, 0)
    d = datetime.datetime(*datetime_tuple)
    return julian.to_jd(d)

def get_planet_data(toi_names): 
    url = "https://exofop.ipac.caltech.edu/tess/gototoitid.php"
    payload = 'toi='
    headers = {
    'Origin': 'https://exofop.ipac.caltech.edu',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    data = []
    
    for name in toi_names:
        try:
            response = requests.request("POST", url, headers=headers, data = payload+name)
            # save_response(response,name)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find("tbody")
            tr = table.find_all("tr")[1]
            td = table.find_all("td")

            response = response.text
            ra = re.search("\d+\.\d+&deg",response).group(0)[:-4]
            dec = re.search("[+|-]\d+\.\d+&deg",response).group(0)[1:-4]
            tyc_name = re.search("TYC\s.+\-\d,",response).group(0)[:-1]

            planet = []
            planet.extend(["TOI "+name,tyc_name, ra, dec])
            tmp = [td[3].text, td[4].text, td[7].text]  # epoch,period,duration
            tmp = [ i[:i.find(" ")-1] for i in tmp]
            planet.extend(tmp)

            data.append(planet)
            print("   TOI",name,"=",planet)

        except Exception as e:
            print(e)
            print("Failed for: ",name)

    #             0       1      2   3     4       5       6
    # data  = [ name, tyc_name, ra, dec, epoch, period, duration]
    print()
    return data


def get_transit_data(planet_data,begin_data,end_date):

    for data in planet_data:

        # Generating Directory
        # ===========================================================================
        url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TransitView/nph-visibletbls?dataset=transits"
        response = requests.request("GET", url).text
        directory = re.search("TMP.+_\d{6}",response).group(0)

        # Sending query on server
        # ===========================================================================
        url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TransitSearch/nph-transitsearch?"
        params = {
        "destDir":directory,
        "customParams":1,
        "period":data[5],
        "tdur":data[6],
        "tranmid":data[4],
        "ra":data[2],
        "dec":data[3],
        "all_ephem":1,
        "locations":"%22Custom,24.6653,72.7819%22",
        "begin":begin_data,
        "end":end_date}

        for key in params:
            url += key+"="+str(params[key])+"&"
        url = url.rstrip("&")

        response = requests.request("GET",url)
        # print("Respone:\n",response.status_code)
        # print("directory\n",directory)
        # print("URL:\n",url)
        # print()

        #  apply settings
        # ======================================================================================================
        url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/IceTable/nph-iceTbl?log=TblView.ExoplanetArchive&workspace="
        url += directory        
        url += "&table=transits.tbl&pltxaxis=&pltyaxis=&checkbox=1&initialcheckedval=1&splitlabel=0&rowLabel=planetname&newSchema=1&dhxr1577733223547=1"
        response = requests.request("GET", url)

        #  Downloading Data from server
        # ======================================================================================================
        url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/IceTable/nph-iceTblDownload"

        payload = 'columns=planetname_display%2Cra_str%2Cdec_str%2Cperiod%2Ctransitduration%2Cingressjd%2Cmidpointcalendar%2Cegressjd%2Ctargetobsstartcalendar%2Ctargetobsendcalendar%2Cfractionobservable%2Cplanetname&format=CSV&label=&mission=ExoplanetArchive&rows=both&table=transits.tbl&useTimestamp=1&user=&workspace='
        response = requests.request("POST", url, data = payload+directory)

        file_data = response.text
        file_data = file_data[file_data.rfind("#")+1:]
        save_as_file(file_data,data[0]+".csv")
        print("   File Created:","TOI_"+data[0]+".csv")
    print()
#%%
toi_names = [1592,1606]#,1598,1608,1580,1005,1548,1471,1490]
toi_names = [str(i) for i in toi_names]

print(colored("Generating planet Data....","red"))
planet_data = get_planet_data(toi_names)

print(colored("Generating Transit Files....","red"))
get_transit_data( planet_data,
                convert_to_jd((2019,12,31)),
                convert_to_jd((2020,3,31))
                )
print(colored("--DONE!--","green"))