
# Description
This project was built to develop my use of building RestAPI microservices and simple relational databases. The HTML was built using boilerplate code to focus on the backend. The project used Flask, Python, SQL, HTML and CSS

N.B. This repo consists of the final state of the app, as the original project repo was initiated as a private repo on a separate account. Therefore previous repo history (commits etc) cannot be found.

# Setup

## Requirements
User must have python and postgres installed on machine
All requirements are stored in the requirements.txt file.

## Installation 

Clone repo in terminal:
- run `git clone https://github.com/KAcodes/News-Scraper.git`


Create and Activate virtual environment:
- run `python3 -m venv venv`
      `source ./venv/bin/activate`
 
Install necessary requirements:
- run  `pip3 install -r requirements.txt`

### Environment variables
As there is currently no live database, a local PostgreSQL database must be made with the following values of your choice, and also placed in an `.env`:
`DB_HOST`
`DB_PORT`
`DB_NAME`
`DB_USER`
`DB_PASSWORD`

Run database setup script:
- run  `bash (or other shell) reset_database.sh`

Run flask server:
- run  `python3 api.py`

The app should open up on local page http://127.0.0.1:5000 