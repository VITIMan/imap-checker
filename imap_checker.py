#!/usr/bin/python
# -*- coding: utf-8 -*-

# Credits and references
# https://blog.jtlebi.fr/2013/04/12/fetching-all-messages-since-last-check-with-python-imap/
# http://stackoverflow.com/questions/703185/using-email-headerparser-with-imaplib-fetch-in-python
# http://unix.stackexchange.com/a/4530
# Notifications
# http://crysol.org/es/node/1356


# http://stackoverflow.com/questions/4281821/pynotify-not-working-from-cron


# python imports
import ConfigParser
import imaplib
import logging
import os
from email.parser import HeaderParser

# 3rd. libraries imports
import pynotify

logger = logging.getLogger(__name__)


def fetch_mails(mail_server, last_uid, last_uid_file):
    """
    """
    if last_uid_file is None:
        last_uid_file = last_uid

    messages = []
    # for uid in xrange(last_uid_file, last_uid+1):
    data = mail_server.uid('fetch', last_uid, '(RFC822)')
    header_data = data[1][0][1]

    parser = HeaderParser()
    msg = parser.parsestr(header_data)

    logger.debug("Fetched! From:{}, Subject:{}".format(
        msg["From"], msg["Subject"]))
    # messages.append(msg)
    return msg


def check_mails(host, user, password):
    """
    """
    home_path = os.path.expanduser("~")
    os.chdir(home_path)
    mail_server = imaplib.IMAP4_SSL(host)

    if (mail_server.login(user, password)[0] != 'OK'):
        exit("no conn")

    try:
        with open('.imap_check', 'r') as f:
            last_uid_file = f.readline()
            last_uid_file = int(last_uid_file)
    except (IOError, ValueError):
        logger.debug("file not found in {}".format(home_path))
        last_uid_file = None

    last_email_in_folder = mail_server.select('INBOX')[1][0]
    last_uid = mail_server.uid('search', None, last_email_in_folder)[1][0]

    # debug
    logger.debug("last_uid_file:{}, last_uid:{}".format(
        last_uid_file, last_uid))

    if last_uid_file is not None and int(last_uid) <= int(last_uid_file):
        msg = {}
    else:
        msg = fetch_mails(mail_server, last_uid, last_uid_file)

    if not last_uid_file or int(last_uid) != int(last_uid_file):
        try:
            with open('.imap_check', 'w') as f:
                f.write(last_uid)
        except IOError:
            logger.debug("cannot write in file")

    return msg


# get configuration
config = ConfigParser.SafeConfigParser()
# TODO For now we read from local path
# TODO Catch error
config.read('config')
host = config.get('imap', 'host')
user = config.get('imap', 'user')
password = config.get('imap', 'password')

msg = check_mails(host, user, password)

# notify
if msg:
    pynotify.init("Imap checker")
    notification = pynotify.Notification(msg["From"],
                                         message=msg["Subject"],
                                         icon="emblem-debian")
    notification.show()

    # OSX notification test purposes
    # from pync import Notifier
    # Notifier.notify(msg["Subject"][:25], title=msg["From"][:10])
    # Notifier.remove(os.getpid())
    # Notifier.list(os.getpid())
else:
    # debug
    logger.debug("no email")
