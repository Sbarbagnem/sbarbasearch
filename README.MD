# README

Information retrieval project: develop a Twitter search engine with presonalized search.   
Group members:

* Samuele Ventura, ID: 793060,  email: s.ventura6@campus.unimib.it
* Federico Belotti, ID: 808708, email: f.belotti8@campus.unimib.it

The project has been tested on [Pop!_OS](https://system76.com/pop) 19.10 and MacOS 10.15.2.  
If you're using Windows...use Linux!

## Requirements

In order to use this project, one needs to:

* Download and install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Download and install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/)
* Download and install [conda](https://docs.conda.io/projects/conda/en/latest/index.html)
* Download the [data folder](https://drive.google.com/drive/folders/1xKj7u-e2lf5GcJPHhDgBkNyPB70AP4Yv?usp=sharing) and unpack it in the project root: please remember that all the modules refers to the files in the data folder as they are, so do not change their positions or names!  
This folder contains:
  * A folder named `models` which contains all the word embeddings trained with TWEC and the additional `bigrams.pkl` and `trigrams.pkl` models
  * A folder named `query`, which contains the `query.json` with 478528 multiple topics (sport, economy, politics, music, cinema, technology) tweets from 01-21-2020 to 02-04-2020, and the `query.pkl` which contains a list of lists with the preprocessed and tokenized tweets
  * A folder named `twec`, which contains all the .txt files needed to train TWEC
  * A folder named `users`, which contains all the users tweets and their respective preprocessed and tokenized .pkl files

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

## Usage

If you're running a **Linux-like distro** you better start running `sudo sysctl -w vm.max_map_count=262144`, otherwise Kibana service won't start properly.    
When you've downloaded the [data folder](https://drive.google.com/drive/folders/1xKj7u-e2lf5GcJPHhDgBkNyPB70AP4Yv?usp=sharing) and unpacked it in the project root, you can start the services up running `docker-compose up -d`, then `python -m indexer.create_index` to create the index, which can be managed at http://localhost:5601/app/kibana.  
Run the webapp with `python -m webapp.app` and browse to http://127.0.0.1:5000/.

### Useful commands

A **rule of thumb** to run every runnable script in this project is: `python -m folder.script_name [options...]`.  
Every script you wanna run, **you must run it from the project root**, so if for example you want to run a preprocess stage, from the project root run `python -m preprocess.preprocess --help` to see whats options you have, then run the script with the desired options.  
Here are listed all the runnble scripts:

* `python -m crawl_tweet.crawl_tweet_query` downloads or updates the query tweets using tweepy API. Run it with `--help` to see all the available options
* `python -m crawl_tweet.crawl_tweet_users` downloads or updates the users tweets using tweepy API. Run it with `--help` to see all the available options
* `python -m embeddings.create_twec_data` creates the txt files to train TWEC. Run it with `--help` to see all the available options
* `python -m embeddings.train_embeddings` trains TWEC models. Run it with `--help` to see all the available options
* `python -m embeddings.train_phraser` trains bigrams and/or trigrams models. Run it with `--help` to see all the available options
* `python -m indexer.create_index` creates the index used by [Elasticsearch](https://www.elastic.co/) during the search.
* `python -m preprocess.preprocess` preprocess the query and the users json files. Run it with `--help` to see all the available options
* `python -m user_profile.create_bow` creates the users profiles fitting a TF model. Run it with `--help` to see all the available options
* `python -m webapp.app` starts the webapp at http://127.0.0.1:5000/

### Typical workflow

If you want, for example, update users and query tweets, preprocessed them, learn bigram or trigram models and/or a new word embeddings with different parameters, please consider to follow those steps in order:

1. [Optional] `python -m crawl_tweet.crawl_tweet_query` to update the query tweets
2. [Optional] `python -m crawl_tweet.crawl_tweet_users` to update the users tweets
3. `python -m preprocess.preprocess` to preprocess the query and the users json files, and save the preprocessed files as list of sentences, where each sentence is a list of tokens. This is needed for both the phrases and the twec model
4. `python -m embeddings.train_phraser` to learn bigram and/or trigram models
5. `python -m embeddings.create_twec_data` to create txts needed to train twec
6. `python -m embeddings.train_embeddings` to train the twec models
7. `python -m user_profile.create_bow` to update the users profiles fitting a new TF model
8. `python -m indexer.create_index` to create the index used by [Elasticsearch](https://www.elastic.co/) during the search
9. `python -m webapp.app` starts the webapp at http://127.0.0.1:5000/
