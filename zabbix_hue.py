#!/usr/bin/env python
# coding: utf-8


from __future__ import unicode_literals
import argparse
import ConfigParser
import json
import os
import zhue


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Available commands', dest='action')
    temperature_parser = subparsers.add_parser(
        'temperature',
        help='Temperature readings'
    )
    temperature_parser.add_argument(
        'temperature_action',
        choices=['discover', 'read']
    )
    temperature_parser.add_argument(
        'hue_id',
        action='store',
        nargs='?'
    )
    battery_parser = subparsers.add_parser(
        'battery',
        help='Battery readings'
    )
    battery_parser.add_argument(
        'battery_action',
        choices=['discover', 'read']
    )
    battery_parser.add_argument(
        'hue_id',
        action='store',
        nargs='?'
    )
    light_level_parser = subparsers.add_parser(
        'light_level',
        help='Lightlevel readings'
    )
    light_level_parser.add_argument(
        'light_level_action',
        choices=['discover', 'read']
    )
    light_level_parser.add_argument(
        'hue_id',
        action='store',
        nargs='?'
    )
    return parser.parse_args()


def read_config(filename='/etc/zabbix/bin/hue-credentials.conf',
                section='philips-hue'):
    config = ConfigParser.ConfigParser(
        {
            'hostname': None,
            'username': None
        }
    )
    if not os.path.isfile(filename):
        filename = os.path.basename(filename)
    config.read(filename)
    h = config.get(section, 'hostname')
    u = config.get(section, 'username')
    return h, u



def __connect(hostname=None, username=None):
    if not hostname and not username:
        h, u = read_config()
    else:
        h = hostname
        u = username
    if h:
        return zhue.Bridge(hostname=h, username=u)
    else:
        # This may take too long. Consider raising the timeout
        return zhue.Bridge.discover(username=u)


def __print_hue_info(hue_devices):
    json_data = {'data':[]}
    for d in hue_devices:
        json_data['data'].append(
            {
                '{#HUE_ID}': d.hue_id
                # '{#HUE_NAME}': d.name
            }
        )
    print(json.dumps(json_data))


def battery_discover():
    b = __connect()
    hue_devices = [x for x in b.devices if hasattr(x, 'battery')]
    return __print_hue_info(hue_devices)


def battery_read(hue_id=None):
    b = __connect()
    if hue_id:
        data = [b.sensor(hue_id=hue_id).battery]
    else:
        data = [x.battery for x in b.devices if hasattr(x, 'battery')]
    for d in data:
        print(d)


def temperature_discover():
    b = __connect()
    hue_devices = [x for x in b.temperature_sensors]
    return __print_hue_info(hue_devices)


def temperature_read(hue_id=None):
    b = __connect()
    if hue_id:
        data = [b.sensor(hue_id=hue_id).temperature]
    else:
        data = [x.temperature for x in b.temperature_sensors]
    for d in data:
        print(d)


def light_level_discover():
    b = __connect()
    hue_devices = [x for x in b.light_level_sensors]
    return __print_hue_info(hue_devices)


def light_level_read(hue_id=None):
    b = __connect()
    if hue_id:
        data = [b.sensor(hue_id=hue_id).light_level]
    else:
        data = [x.light_level for x in b.light_level_sensors]
    for d in data:
        print(d)


def main():
    args = parse_args()
    if args.action == 'temperature':
        if args.temperature_action == 'discover':
            temperature_discover()
        elif args.temperature_action == 'read':
            temperature_read(args.hue_id)
    elif args.action == 'light_level':
        if args.light_level_action == 'discover':
            light_level_discover()
        elif args.light_level_action == 'read':
            light_level_read(args.hue_id)
    elif args.action == 'battery':
        if args.battery_action == 'discover':
            battery_discover()
        elif args.battery_action == 'read':
            battery_read(args.hue_id)


if __name__ == '__main__':
    main()
