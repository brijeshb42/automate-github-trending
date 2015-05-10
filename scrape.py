import datetime

import requests
from bs4 import BeautifulSoup
import mailchimp
from jinja2 import Environment, PackageLoader

from config import *

api_object = mailchimp.Mailchimp(MAIL_CHIMP_KEY)

URL_TRENDING = "https://github.com/trending"


def update_template(content, template_id):
    status = api_object.templates.update(
        template_id, {'html': content}
    )
    return status['complete']


def create_campaign(name, subject, list_id, template_id, send=False):
    campaign = api_object.campaigns.create(
        'regular',
        {
            'list_id': list_id,
            'subject': subject,
            'from_email': MAIL_FROM,
            'from_name': 'Bitwiser.in',
            'template_id': template_id,
            'title': name
        },
        {}
    )
    if send:
        status = api_object.campaigns.send(campaign['id'])
        return status
    else:
        return campaign['id']


def send_newsletter(
        list_id=MAIL_LIST_ID,
        template_id=MAIL_TEMPLATE_ID,
        subject="Bitwiser.in - Github Trending Repos",
        cname="Github Trending Repos",
        html=None):
    if not subject or not cname or not html:
        return
    todays_date = datetime.datetime.now().strftime('%d-%m-%Y')
    template_updated = update_template(html, template_id)
    if template_updated:
        subject = subject+" for "+datetime.datetime.now().strftime('%A, %B %d')
        campaign_name = cname + todays_date
        status = create_campaign(
            campaign_name, subject, list_id, template_id, True)
        return status


def get_latest_trending(lang=None):
    url = URL_TRENDING
    if lang:
        url = URL_TRENDING + "?l=" + lang
    res = requests.get(url)
    if res.status_code > 200:
        return
    repos = []
    soup = BeautifulSoup(res.content)
    trending = soup.select(".repo-list-item")
    for repo in trending:
        res = {}
        res["name"] = repo.select(".repo-list-name > a")[0]["href"]
        desc = repo.select(".repo-list-description")
        meta = repo.select(".repo-list-meta")
        if len(desc) > 0:
            res["description"] = desc[0].contents[0].strip()
        if len(meta) > 0:
            meta = str(
                " ".join(meta[0].contents[0].strip().encode("ascii", "ignore")
                         .split())).replace(" Built by", "")
            meta1 = meta.split()
            res["language"] = meta1[0]
            res["stars"] = meta1[1]
        repos.append(res)
    return repos


def send_mail(repos=[]):
    env = Environment(loader=PackageLoader(__name__, './'))
    template = env.get_template("mailer.html")
    script = {
      "@context": "http://schema.org",
      "@type": "EventReservation",
      "reservationNumber": "IO12345",
      "underName": {
        "@type": "Person",
        "name": "Brijesh Bittu"
      },
      "reservationStatus": "confirmed",
      "reservationFor": {
        "@type": "Event",
        "name": "Github Trending Repositories",
        "startDate": datetime.datetime.now().isoformat(),
        "location": {
          "@type": "Place",
          "name": "Github.com"
        }
      }
    }
    html = template.render(repos=repos, script=script)
    with open("output.html", "w") as fil:
        fil.write(html.encode('utf-8'))
    send_newsletter(html=html)


def get_data_send_mail():
    send_mail(get_latest_trending())


if __name__ == "__main__":
    get_data_send_mail()
