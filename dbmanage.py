#!/usr/bin/env python

from argparse import ArgumentParser
from configparser import ConfigParser
import psycopg2


class Config(ConfigParser):

    filename = 'dbmanage.cfg'

    @property
    def index_file(self):
        return self['versioning']['index_file']

    @property
    def database(self):
        return self['database']['database']

    @property
    def host(self):
        return self['database']['host']

    @property
    def dsn(self):
        def get_option(name):
            return self.get('database', name)

        connection_params = dict(
            database=get_option('database'),
            host=get_option('host'),
            port=get_option('port'),
            user=get_option('user'),
            password=get_option('password')
        )
        return ' '.join(['{}={}' for k, v in connection_params.items() if v])

    @classmethod
    def create_default_config(cls):
        config = cls()

        config.add_section('database')
        config.set('database', 'database', '')
        config.set('database', 'host', 'localhost')
        config.set('database', 'port', '5432')
        config.set('database', 'user', '')
        config.set('database', 'password', '')

        config.add_section('versioning')
        config.set('versioning', 'index_file', 'index.txt')

        with open('dbmanage.cfg', 'w') as f:
            config.write(f)


def read_config():
    config = Config()
    config.read(['dbmanage.cfg'])
    return config


def create_parser():
    parser = ArgumentParser(description='Create, destroy, and upgrade your database')
    subparsers = parser.add_subparsers(dest='command')

    create_subparser = subparsers.add_parser('create', help='Create a database')

    destroy_subparser = subparsers.add_parser('destroy', help='Destroy your database')

    info_subparser = subparsers.add_parser('list', help='List versioning information')
    info_subparser.add_argument('-a', '--applied', help='List applied patches only')
    info_subparser.add_argument('-u', '--unapplied', help='List unapplied patches only')

    upgrade_subparser = subparsers.add_parser('upgrade', help='Upgrade your database')
    upgrade_subparser.add_argument('--only', help='Apply a specific patch')

    return parser


def main():
    config = read_config()
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'create':
        create(config)
    elif args.command == 'destroy':
        destroy(config)
    else:
        upgrade(config)


def get_connection(config):
    return psycopg2.connect(config.dsn)


def create(config):
    conn = get_connection(config)
    cur = conn.cursor()


def upgrade(config):
    pass


def destroy(config):
    pass


if __name__ == '__main__':
    main()
