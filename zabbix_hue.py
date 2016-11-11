#!/usr/bin/env python
# coding: utf-8


from __future__ import unicode_literals
import argparse
import json
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


def __connect(username, hostname=None):
    if hostname:
        return zhue.Bridge(hostname=hostname, username=username)
    else:
        return zhue.Bridge.discover(username=username)


def __print_hue_ids(hue_ids):
    json_data = {'data':[]}
    for hid in hue_ids:
        json_data['data'].append({'#HUE_ID': hid})
    print(json.dumps(json_data))


def battery_discover():
    b = __connect(hostname=hostname, username=username)
    hue_ids = [x.hue_id for x in b.sensors if hasattr(x.config, 'battery')]
    return __print_hue_ids(hue_ids)


def battery_read(hue_id=None):
    b = __connect(hostname=hostname, username=username)
    if hue_id:
        data = [b.sensor(hue_id=hue_id).config.battery]
    else:
        data = [x.config.battery for x in b.sensors if hasattr(x.config, 'battery')]
    for d in data:
        print(d)


def temperature_discover():
    b = __connect(hostname=hostname, username=username)
    hue_ids = [x.hue_id for x in b.temperature_sensors]
    return __print_hue_ids(hue_ids)


def temperature_read(hue_id=None):
    b = __connect(hostname=hostname, username=username)
    if hue_id:
        data = [b.sensor(hue_id=hue_id).temperature]
    else:
        data = [x.temperature for x in b.temperature_sensors]
    for d in data:
        print(d)


def light_level_discover():
    b = __connect(hostname=hostname, username=username)
    hue_ids = [x.hue_id for x in b.light_level_sensors]
    return __print_hue_ids(hue_ids)


def light_level_read(hue_id=None):
    b = __connect(hostname=hostname, username=username)
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