import argparse
import re
from server import Server
from storage import Storage
from cache import Cache

DEFAULT_SMF_URL = 'localhost'
DEFAULT_SMF_PORT = 8088
DEFAULT_SMF_USERNAME = 'admin'
DEFAULT_SMF_PASSWORD = 'Smf_admin123!@'
ATTRIBUTE_TYPE_LDISK = 'LDISK'
ATTRIBUTE_TYPE_POOL = 'POOL'
ATTRIBUTE_TYPE_RAID = 'RAID'
ATTRIBUTE_TYPE_CACHE = 'CACHE'
REGEX_IPV4 = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"


def setup_command():
    parse = argparse.ArgumentParser(
        'Parse argument for remove storage attribue')
    parse.add_argument('-r', '--host', help='URL', default=DEFAULT_SMF_URL)
    parse.add_argument('-p', '--port', help='port number',
                       type=int, default=DEFAULT_SMF_PORT)
    parse.add_argument('-u', '--user', help='SMF username',
                       default=DEFAULT_SMF_USERNAME)
    parse.add_argument('-w', '--password',
                       help='password SMF user', default=DEFAULT_SMF_PASSWORD)
    parse.add_argument(
        '-i', '--ip', help='IP of storage device', required=True)
    group = parse.add_mutually_exclusive_group(required=True)
    group.add_argument('-L', '--ldisk', help='LDISK number range. Ex: 1x10')
    group.add_argument('-P', '--pool', help='pool number range. Ex: 1x10')
    group.add_argument(
        '-G', '--raid', help='RAID group number range. Ex: 1x10')
    group.add_argument(
        '-C', '--cache', help='cache partition number range. Ex: 1x10')
    return parse.parse_args()


def get_range_id(args):
    id_range = None
    if args.raid:
        id_range = args.raid
    elif args.pool:
        id_range = args.pool
    elif args.cache:
        id_range = args.cache
    else:
        id_range = args.ldisk
    ids = str(id_range).split(':')
    if len(ids) != 2:
        raise ValueError('Invalid range of id')
    try:
        lower = int(ids[0])
        upper = int(ids[1])
    except:
        raise ValueError('Invalid range of id')
    return (lower, upper)


def main():
    args = setup_command()
    lower, upper = get_range_id(args)
    server = Server(args.host, args.port, args.user, args.password)
    storage_attribute = None
    if args.raid:
        pass
    elif args.pool:
        pass
    elif args.cache:
        storage_attribute = Cache(server, args.ip, lower, upper)
    else:
        pass
    storage_attribute.remove()


if __name__ == '__main__':
    main()
