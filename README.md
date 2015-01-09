# EliteProspects Scraper

### Installation:

1. Install python 3 (`brew install python3`).
2. Set python3 & pip3 as your defaults by linking them to your /usr/local/bin:
  * `ln -s /usr/local/Cellar/python3/3.4.2_1/bin/python3.4 /usr/local/bin/python`
  * `ln -s /usr/local/Cellar/python3/3.4.2_1/bin/pip3.4 /usr/local/bin/pip`
3. Install RabbitMQ (`brew install rabbitmq`).
4. Install [heroku-toolbelt](https://toolbelt.heroku.com/).
5. Install the dependencies (`pip install -r requirements.txt`).
6. Rename the environment config template to `development.env`.
7. Replace any credentials in the config for your local environment that might differ from the defaults.
8. Create a symbolic link from the environment you want to use as your default environment (e.g. `ln -s config/development.env .env`).
