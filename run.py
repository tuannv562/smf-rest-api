import argparse
import re
from server import Server
from storage import Storage

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


def get_args(args):
    id_range = None
    attribute_type = None
    if args.ldisk:
        id_range = args.ldisk
        attribute_type = ATTRIBUTE_TYPE_LDISK
    elif args.pool:
        id_range = args.pool
        attribute_type = ATTRIBUTE_TYPE_POOL
    elif args.raid:
        id_range = args.raid
        attribute_type = ATTRIBUTE_TYPE_RAID
    else:
        id_range = args.cache
        attribute_type = ATTRIBUTE_TYPE_CACHE
    ip = str(args.ip)
    p = re.compile(REGEX_IPV4)
    if not p.match(ip):
        raise ValueError('Invalid storage IP')
    id_list = str(id_range).split('x')
    if len(id_list) != 2:
        raise ValueError('Invalid range number')
    lower_bound = int(id_list[0])
    upper_bound = int(id_list[1])
    if lower_bound < 0 or upper_bound < 0 or lower_bound > upper_bound:
        raise ValueError('Invalid range number')
    return (ip, attribute_type, lower_bound, upper_bound)


def main():
    args = setup_command()
    ip, attribute_type, lower_id, upper_id = get_args(args)
    server = Server(args.host, args.port, args.user, args.password)
    storage = Storage(server, ip)

    cache_ids = list(storage._get_all_cache_id())
    print(cache_ids)
    # print(storage._set_wbc_for_ldisks(1, True))
    # cache_ids = list(storage._get_all_ldisk_on_wbc())
    # print(cache_ids)
    #storage.remove(attribute_type, lower_id, upper_id)


if __name__ == '__main__':
    main()
