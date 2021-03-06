# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2014 Mozilla Corporation
#
# Contributors:
# Jeff Bryner jbryner@mozilla.com

import netaddr


def isIPv4(ip):
    try:
        # netaddr on it's own considers 1 and 0 to be valid_ipv4
        # so a little sanity check prior to netaddr.
        # Use IPNetwork instead of valid_ipv4 to allow CIDR
        if '.' in ip and len(ip.split('.'))==4:
            # some ips are quoted
            netaddr.IPNetwork(ip)
            return True
        else:
            return False
    except:
        return False


def findIPv4(words):
    for word in words.strip().split():
        saneword = word.strip().strip('"').strip("'").strip(",")
        if isIPv4(saneword):
            yield saneword


class message(object):
    def __init__(self):
        '''
        takes an incoming message
        and sets the doc_type
        '''

        self.registration = ['google']
        self.priority = 5

    def onMessage(self, message, metadata):
        # make sure it's a google activity event
        # set the doc type
        # and do any clean up

        # check for details.kind like 'admin#reports#activity'
        if ( 'details' in message.keys() and
             'kind' in message['details'].keys() and
             'activity' in message['details']['kind']):

            # details.etag might be quoted..unquote it
            if 'etag' in message['details'].keys():
                message['details']['etag'] = message['details']['etag'].replace('"', '')

            metadata['doc_type']= 'google'


        return (message, metadata)