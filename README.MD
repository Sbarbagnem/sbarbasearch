# README

Information retrieval project: develop a Twitter search engine with presonalized search.   
Group members:

* Samuele Ventura, ID: 793060
* Federico Belotti, ID: 808708

## Requirements

In order to use this project, one needs to:

* Download and install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Download and install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/)
* Download and install [conda](https://docs.conda.io/projects/conda/en/latest/index.html)
* Download the [data folder](https://drive.google.com/drive/folders/1xKj7u-e2lf5GcJPHhDgBkNyPB70AP4Yv?usp=sharing) and unpack it in the project root: please remember that all the modules refers to the files in the data folder as they are, so do not change their positions or names!

## Installation

Follow those instructions to create the workspace:

* `git clone https://github.com/Sbarbagnem/sbarbasearch.git`
* `cd sbarbasearch`
* Copy the **data folder** in here
* Clone the TWEC repository with `git clone https://github.com/valedica/twec.git`, needed to train a particular version of the Temporal Word Embeddings. For more information https://github.com/valedica/twec
* `conda env create --name sbarbasearch --file=environment.yml`
* `conda activate sbarbasearch`
* `cd twec; pip install -e .; cd ..` to install TWEC
* `python requirements_installer.py` to install packages needed to [NLTK](https://www.nltk.org/)

Per poter accedere all'index e al servizio di gestione dell'index è necessario eseguire il comando `docker-compose up -d` nella directory principale del progetto, con cui vengono attivati il servizio elasticsearch e il servizio kibana. I due servizi sono raggiungibili rispetivamente alla pagina localhost:9200 e localhost:5601. Per quanto riguarda elasticsearch nel momento effettivo in cui il servizio è attivo sarà solamente visualizzata una pagina web che indica lo stato di salute del sistema. 

I tweets scaricati sono salvati in un file json raggiungibile al link https://drive.google.com/open?id=1icq1eDQJOfpL4MbOoCItODlFIa7Z1KZf. Dopo aver scaricato i tweet è necessario eseguire il file indexer/indexer.py, che crea l'index e carica i tweet. 

Nella directory user_profile/data è presente una serie di file json uno per ogni utente su cui è stata costruita una bag of words salvata nel file bow.json

Per eseguire la webapp è necessario spostarsi nella in webapp ed eseguire app.py, sarà poi raggiungibile a localhost:5000.