payload = 'columns=planetname_display%2Cra_str%2Cdec_str%2Cperiod%2Ctransitduration%2Cingressjd%2Cmidpointcalendar%2Cegressjd%2Ctargetobsstartcalendar%2Ctargetobsendcalendar%2Cfractionobservable%2Cplanetname&format=CSV&label=&mission=ExoplanetArchive&rows=both&table=transits.tbl&useTimestamp=1&user=&workspace=TMP_IND2FM_19424/TransitView/2019.12.30_10.27.12_005517'

#%%
from astropy.time import Time
         
t = Time("2019-12-31 20:17:00.000", format='iso', scale='ut1')
print(t.jd)
#%%


import requests

url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/IceTable/nph-iceTbl?log=TblView.ExoplanetArchive&workspace=TMP_Mx6wwr_21211%2FTransitView%2F2019.12.30_15.21.52_021211&table=transits.tbl&pltxaxis=&pltyaxis=&checkbox=1&initialcheckedval=1&splitlabel=0&rowLabel=planetname&newSchema=1&dhxr1577733223547=1"
response = requests.request("GET", url)
print(response.text)


