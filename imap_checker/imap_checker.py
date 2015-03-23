#!/usr/bin/python
# -*- coding: utf-8 -*-

# Credits and references
# https://blog.jtlebi.fr/2013/04/12/fetching-all-messages-since-last-check-with-python-imap/
# http://stackoverflow.com/questions/703185/using-email-headerparser-with-imaplib-fetch-in-python
# http://unix.stackexchange.com/a/4530
# Notifications
# http://crysol.org/es/node/1356
# http://stackoverflow.com/questions/7331351/python-email-header-decoding-utf-8
# log
# http://stackoverflow.com/questions/13180720/maintaining-logging-and-or-stdout-stderr-in-python-daemon

# http://stackoverflow.com/questions/4281821/pynotify-not-working-from-cron

# python imports
import ConfigParser
import email.Header
import imaplib
import logging
import logging.config
import os
import signal
import sys
import time
from email.parser import HeaderParser
from logconfig import LOGGING
from optparse import OptionParser

# 3rd. libraries imports
import daemon
import pynotify
from pidfile import PidFile

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

pid_file = "/tmp/imap_checker.pid"


def sig_terminate(signum, frame):
    logger.info("caught signal {}, stopping...".format(signum))
    pid = os.getpid()
    os.kill(pid, signal.SIGHUP)


def fetch_mails(mail_server, last_uid, last_uid_file):
    """
    """
    if last_uid_file is None:
        last_uid_file = last_uid

    # messages = []
    # for uid in xrange(last_uid_file, last_uid+1):
    data = mail_server.uid('fetch', last_uid, '(RFC822)')
    header_data = data[1][0][1]

    parser = HeaderParser()
    msg = parser.parsestr(header_data)
    logger.debug("Fetched! From:{}, Subject:{}".format(
        msg["From"], msg["Subject"]))

    subject, encoding = email.Header.decode_header(msg["Subject"])[0]
    logger.debug("Decoding subject:{} encoding:{}".format(subject, encoding))

    # messages.append(msg)
    message_formatted = {"From": msg["From"],
                         "Subject": subject}
    return message_formatted


def check_mails(host, user, password):
    """
    """
    uid_path = os.path.expanduser("~/.imap_check")
    mail_server = imaplib.IMAP4_SSL(host)

    if (mail_server.login(user, password)[0] != 'OK'):
        exit("no conn")

    try:
        with open(uid_path, 'r') as f:
            last_uid_file = f.readline()
            last_uid_file = int(last_uid_file)
    except (IOError, ValueError):
        logger.debug("file not found in {}".format(uid_path))
        last_uid_file = None

    last_email_in_folder = mail_server.select('INBOX')[1][0]
    last_uid = mail_server.uid('search', None, last_email_in_folder)[1][0]

    logger.debug("last_uid_file:{}, last_uid:{}".format(
        last_uid_file, last_uid))

    if last_uid_file is not None and int(last_uid) <= int(last_uid_file):
        msg = {}
    else:
        msg = fetch_mails(mail_server, last_uid, last_uid_file)

    if not last_uid_file or int(last_uid) != int(last_uid_file):
        try:
            with open(uid_path, 'w') as f:
                f.write(last_uid)
        except IOError:
            logger.debug("cannot write in file")

    return msg


def checker(host, user, password, fetch_time):
    while True:
        msg = check_mails(host, user, password)

        try:
            if msg:
                pynotify.init("Imap checker")
                notification = pynotify.Notification(
                    msg["From"],
                    message=msg["Subject"],
                    icon="applications-email-panel")
                notification.set_timeout(5000)
                notification.show()

                # OSX notification test purposes
                # from pync import Notifier
                # Notifier.notify(msg["Subject"][:25], title=msg["From"][:10])
                # Notifier.remove(os.getpid())
                # Notifier.list(os.getpid())
            else:
                logger.debug("no email")
        except Exception:
            logger.exception("error detected")
            raise
        time.sleep(fetch_time)


def stop_process():
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.readline())
    except IOError:
        print("Cannot open pidfile")
    except (TypeError, ValueError):
        print("Incorrect pidfile")

    os.kill(pid, signal.SIGTERM)
    logger.debug("Stop succesful")
    sys.exit(0)


def run():
    parser = OptionParser()
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      help="debug, no daemonize")
    parser.add_option("--stop", action="store_true",
                      dest="stop",
                      help="stop the process")
    parser.add_option("--logfile",
                      action="store",
                      dest="log",
                      help="output to a log file")

    opts, args = parser.parse_args()

    # stop the process
    if opts.stop is not None:
        try:
            stop_process()
        except UnboundLocalError:
            print "no process detected"
            sys.exit(1)

    # signal preparation
    signal.signal(signal.SIGTERM, sig_terminate)
    # signal.signal(signal.SIGHUP, sig_terminate)

    # configuration
    config = ConfigParser.SafeConfigParser({'fetch_time': '30'})

    config_path = os.path.expanduser("~/.imap_conf")
    try:
        config.read(config_path)
        host = config.get('imap', 'host')
        user = config.get('imap', 'user')
        password = config.get('imap', 'password')
        fetch_time = float(config.get('imap', 'fetch_time'))
    except ConfigParser.NoSectionError as e:
        print("check config or create the file ~/.imap_conf: {}".format(
            e))
        sys.exit(1)

    # parsing options
    if opts.debug is not None:
        # TODO kwargs
        logger.debug("Script execution for debugging purposes")
        checker(host, user, password, fetch_time)
    else:
        ctxt = daemon.DaemonContext(
            files_preserve=[logger.root.handlers[1].stream],)
        ctxt.pidfile = PidFile(pid_file)

        logger.debug("Daemonize")
        with ctxt:
            checker(host, user, password, fetch_time)


if __name__ == "__main__":
    run()
