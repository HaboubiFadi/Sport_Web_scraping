### SPORT_WEB_SCRAPING

Web Scraping with Selenium, Docker, Bitnami Airflow, and MongoDB

## Overview

This project aims to automate the web scraping process for a popular sports betting website using Python, Selenium, Docker, Bitnami Airflow, and MongoDB. The scraping is scheduled and orchestrated using Docker containers for Selenium (hub and node_chrome), and Bitnami Airflow manages the workflow.

## Features


Selenium Automation: Utilizes Selenium for web scraping, ensuring accurate and reliable data extraction.

Dockerized Environment: Implements Docker containers for Selenium hub, node_chrome, and Bitnami Airflow, ensuring portability and easy deployment.

Scheduled Scraping: Bitnami Airflow schedules and orchestrates the scraping process, allowing for efficient data retrieval.

MongoDB Integration: Data extracted from the website is stored in MongoDB for structured and persistent storage.



## Prerequisites
Docker installed on your machine
Basic knowledge of Python and web scraping concepts


## Usage
### Define your Web Scraping Logic:

Update the dags/scraping_script.py file with your specific web scraping logic.

### Configure Airflow DAG:

Customize the scraping_dag.py file in the dags/ directory to suit your scraping requirements.

### Run the Project:

Follow the setup instructions to run the project using Docker.
/ docker-compose build 
/ docker-compose up -d
### Monitor and Analyze:

Access the Airflow UI to monitor the DAG execution and review the extracted data in MongoDB.

## Contributions

Contributions are welcome! Feel free to open issues or pull requests for any improvements or additional features.

