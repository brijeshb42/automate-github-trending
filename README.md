# Automate Github Trending

Send email notification with the list of trending repositories on Github.

## Usage
* `git clone git@github.com:brijeshb42/automate-github-trending.git`.
* Create a virtual environment.
* `pip install -r requirements.txt`
* Copy `config.py.default` to `config.py` and edit the values.
* Install and start redis.
* Run `huey_consumer.py tasks.queue`.


* Uses mailchimp's service to send mails.

### Subscribe to the list [here](http://eepurl.com/bmCJOT).
