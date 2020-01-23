Progetto per l'esame di information retrieval con lo scopo di implementare una ricerca personalizzata sfruttando Elasticsearch.

Per poter accedere all'index e al servizio di gestione dell'index è necessario eseguire il comando `docker-compose up -d` nella directory principale del progetto, con cui vengono attivati il servizio elasticsearch e il servizio kibana. I due servizi sono raggiungibili rispetivamente alla pagina localhost:9200 e localhost:5601. Per quanto riguarda elasticsearch nel momento effettivo in cui il servizio è attivo sarà solamente visualizzata una pagina web che indica lo stato di salute del sistema. 

I tweets scaricati sono salvati in un file json raggiungibile al link https://drive.google.com/open?id=1icq1eDQJOfpL4MbOoCItODlFIa7Z1KZf. Dopo aver scaricato i tweet è necessario eseguire il file indexer/indexer.py, che crea l'index e carica i tweet. 

Nella directory user_profile/data è presente una serie di file json uno per ogni utente su cui è stata costruita una bag of words salvata nel file bow.json

Per eseguire la webapp è necessario spostarsi nella in webapp ed eseguire app.py, sarà poi raggiungibile a localhost:5000.