# TO DO
* Testare tf-idf per costruire profilo utente
* Modificare lo scraping dei tweet in modo da poter inserire per ogni tweet il topic (separare query) e controllare che non sia già stato scaricato
* Sistemare import dell'analyzer da un file di setting sia in webapp che indexer (di default la ricerca usa lo stesso analyzer defninito nel setting di indicizzazione quindi nella search non serve definirlo a meno che non si voglia usare un analyzer differente)
* Creare custom analyzer per eliminare sporco nei tweet come caratteri speciali, link (solo quello finale che rimanda la tweet?)
* Capire come costruire profilo utente (per ogni utente leggere un insieme di tweet, non sempre lo stesso, e per ogni topic estrarre delle parole significative (tf-idf) ipotizzando che i tweet esaminati siano di interesse per l'utente in questione) 
* Mettere la possibilità di ordinare i risultati in base a diversi fattori? (followers, like, retweet, data, score)
* Guardare come usare word2vec e elasticsearch (è possibile solo come ulteriore filtro ad una normale query, non è possibile calcolare direttamente il RSV come matching tra vettori)