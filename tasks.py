from huey import RedisHuey, crontab

from scrape import get_data_send_mail

queue = RedisHuey("scrape-trending")


@queue.periodic_task(crontab(minute="0", hour="*/4"))
def send_mail():
    get_data_send_mail()
