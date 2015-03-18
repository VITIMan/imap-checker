#!/usr/bin/python
# -*- coding: utf-8 -*-

# Credits and references
# https://blog.jtlebi.fr/2013/04/12/fetching-all-messages-since-last-check-with-python-imap/
# http://stackoverflow.com/questions/703185/using-email-headerparser-with-imaplib-fetch-in-python
# http://unix.stackexchange.com/a/4530
# Notifications
# http://crysol.org/es/node/1356

# python imports
import imaplib
from email.parser import HeaderParser

# 3rd. libraries imports
import pynotify


def fetch_mail():
    mail_server = imaplib.IMAP4_SSL('imap.example.com')

    if (mail_server.login('email@example.com', 'PASSWORD')[0] != 'OK'):
        exit("no conn")

    # TODO: use home path
    try:
        with open('.imap_check', 'r') as f:
            last_uid_file = f.readline()
            last_uid_file = int(last_uid_file)
    except (IOError, ValueError):
        # file not found
        last_uid_file = None

    last_email_in_folder = mail_server.select('INBOX')[1][0]
    last_uid = mail_server.uid('search', None, last_email_in_folder)[1][0]

    # debug
    # print last_uid_file, type(last_uid_file)
    # print last_uid, type(last_uid)

    if last_uid_file is not None and int(last_uid) <= int(last_uid_file):
        msg = {}
    else:
        data = mail_server.uid('fetch', last_uid, '(RFC822)')
        header_data = data[1][0][1]

        parser = HeaderParser()
        msg = parser.parsestr(header_data)

    # debug
    # print msg['From']
    # print msg['Subject']

    # TODO: use home path
    if not last_uid_file or int(last_uid) != int(last_uid_file):
        try:
            with open('.imap_check', 'w') as f:
                f.write(last_uid)
        except IOError:
            # Cannot write
            pass

    return msg

# TODO Catch error
msg = fetch_mail()

# notify
if msg:
    pynotify.init("Imap checker")
    notification = pynotify.Notification(msg["From"],
                                         message=msg["Subject"],
                                         icon="emblem-debian")
    notification.show()
else:
    print "NO EMAIL"
