#!/usr/bin/python
# search string in mailbox
# Mail are marked as \Deletec
# To expunge them from the filesystem (IMAP spool):
# cyr_expire  -v -X 0 -p user.monitor-store-1

import smtplib
import sys
from random import getrandbits
import imaplib
import argparse
import os

sender = {{ sender}}
destination = 'monitor-{{ansible_hostname | replace('-backend-pro', '') | replace('-replicat-pro', '')}}'
lmtp_admin = {{ lmtp_admin }}
lmtp_password = {{ lmtp_password }}
cyrus_admin = 'cyrus'
cyrus_password = '{{ cyrus_password }}' 

def parse():
    parser = argparse.ArgumentParser(
        description='Send by LMTP a word. Then search with IMAP this word, delete the mail with this word.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("server", nargs="?",
                        default="localhost",
                        help="Where to search the word",
                        )
    args = parser.parse_args()
    return args.server


def send_mail(server, word, sender, destination):
    msg = ("From: %s\r\nTo: %s\r\n\r\n%s\n"
           % (sender, destination, word))
    server = smtplib.LMTP(server, port=24)
    server.login(lmtp_admin, lmtp_password)
    # server.set_debuglevel(1)
    server.sendmail(sender, destination, msg)
    server.quit()


def imap_search(server, word, destination):
    conn = imaplib.IMAP4(server)
    authcb = lambda resp: "{0}\00{1}\00{2}".format(
        destination, cyrus_admin, cyrus_password)
    conn.authenticate("PLAIN", authcb)
    conn.select("INBOX")
    mail_uid = conn.search(None, 'BODY', word)[1][0]
    if mail_uid:
        conn.store(mail_uid, '+FLAGS', '\\Deleted')
        conn.close()
        conn.logout()
        return 0
    else:
        conn.close()
        conn.logout()
        return 1


def expunge(destination):
    mailbox = 'user.' + destination
    command = '/usr/sbin/cyr_expire -X 0 -p ' + mailbox
    os.system(command)

if __name__ == '__main__':
    server = parse()
    word = str(getrandbits(64))
    send_mail(server, word, sender, destination)
    val = imap_search(server, word, destination)
    expunge(destination)
    sys.exit(val)
