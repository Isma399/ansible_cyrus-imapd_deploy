#!/usr/bin/python
# coding: utf8
import argparse
import cyruslib


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", help="Mailbox to copy")
    args = parser.parse_args()
    return args.user


def list_quota(user, server):
    try:
        imap = cyruslib.CYRUS("imap://" + server + ":143")
        imap.login("{{ cyrus_admin }}", "{{ cyrus_password }}")
        used, quota = imap.lq('user.' + user)
        return used, quota
    except cyruslib.CYRUSError, e:
        print "%s: %s" % (e[1], e[2])


def update_quota(user, server, quota):
    try:
        imap = cyruslib.CYRUS("imap://" + server + ":143")
        imap.login("{{ cyrus_admin }}", "{{ cyrus_password }}")
        imap.sq('user.' + user, quota[1] + 100000)
    except cyruslib.CYRUSError, e:
        print "%s: %s" % (e[1], e[2])



if __name__ == '__main__':
    user = parse()
    quota = list_quota(user, "{{ mail_domain }}")
    percent = round(float(quota[0]) / quota[1], 2) * 100
    if percent >= 95:
        update_quota(user, "{{ mail_domain }}", quota)        
        print "Over quota, setting new quota (+100 000)"
        quota = list_quota(user, "{{ mail_domain }}")
        percent = round(float(quota[0]) / quota[1], 2) * 100
    print "   Quota   % Used     Used Root"
    print str(quota[1]) + "\t" + str(percent)  + "\t" + str(quota[0]) + "\tuser." + user 
