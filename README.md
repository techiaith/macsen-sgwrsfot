# Sgwrsfot ar gyfer Macsen

Dyma'r elfen sgwrsfot ar gyfer Macsen - meddalwedd cynorthwyydd personol digidol rydyn ni’n defnyddio i ddatblygu technoleg lleferydd a deallusrwydd artiffisial Cymraeg - sydd yn adnabod bwriad o fewn testun ac sy'n ymateb gydag ateb ac/neu ddata i alluogi Macsen i ymateb yn gywir ac yn ystyrlon.

Dyma enghraifft o'i ddefnydd:

_Beth fydd y tywydd yfory ym Mhwllheli?_

https://localhost:5455/perform_skill?text=Beth+fydd+y+tywydd+yfory+ym+Mhwllheli%3F

```
{
  "intent": "beth.fydd.y.tywydd", 
  "version": 1, 
  "success": true
  "result": 
    [
      {
        "url": "", 
        "title": "Dyma tywydd yfory gan OpenWeatherMap ar gyfer Pwllheli.",
        "description": ""
      }, 
      {
        "title": ""      
        "description": "Yfory am 9 o'r gloch yn y bore bydd hi'n bwrw glaw a'r tymheredd fydd 8 gradd Celsius.", 
        "url": "", 
      }, 
      {
        "title": ""
        "description": "Yn hwyrach yfory am hanner dydd bydd hi'n bwrw glaw a'r tymheredd yn 9 gradd Celsius.", 
        "url": "", 
      }
    ], 
}
```

Defnyddir hybrid o lyfrgelloedd adnabod bwriad cod agored [Padatious](https://mycroft.ai/documentation/padatious/) ac [Adapt](https://mycroft.ai/documentation/adapt/) gan MyCroft.ai, yn ogystal a cydrannau ieithyddiaeth Cymraeg.

 Mae'r sgwrsfot yn medru adnabod sawl bwriad (neu dymuniad) o bump sgil (neu parth). Gwelir y sgiliau yn:
 
 https://github.com/techiaith/macsen-sgwrsfot/tree/master/online-api/assistant/skills
 
 Gwelir bwriadau pob sgil o fewn eu is-ffolder `intent`. e.e. 
 
 https://github.com/techiaith/macsen-sgwrsfot/tree/master/online-api/assistant/skills/spotify/intents
 
 Mae'r ffolderi `intents` yn cynnwys data ar gyfer hyfforddi Padatious ac Adapt. 
 
 
## Llwytho i lawr a gosod y sgwrsfot

Bydd angen cyfrifiadur gyda docker (https://www.docker.com/get-started) wedi'i osod arno eisoes. Bydd angen i chi drefnu allweddi API eich hunain i'r gwasanaethau allanol canlynol:

 - OpenWeatherMap (https://openweathermap.org/api)
 - TimezoneDB (https://timezonedb.com/api) 
 - Spotify (https://developer.spotify.com/documentation/web-api/) 
 
A'u rhoi mewn ffeiliau `apikey.py` o fewn is-ffolder yn y sgil berthnasol. 
 
Diolch i docker, mae'r proses gosod popeth arall yn hawdd iawn. Agorwch ffenestr 'Terminal' ar eich cyfrifiadur, ac o fewn ychydig iawn o  orchmynion bydd y sgwrsfot yn rhedeg ar eich system:
 
```
$ git clone https://github.com/techiaith/macsen-sgwrsfot.git
$ cd macsen-sgwrsfot
( ... rhoi ffeiliau apikey.py i fewn ...)
$ make build-online-api
$ make run-online-api
```
