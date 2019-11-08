# Copyright (C) 2019  GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Author: Aggelos Kolaitis <akolaitis@admin.grnet.gr>
Last Update: 2019/11/08
Description: Clone storage and/or interface configuration between machines

# Usage:
$ mjt_clone_config --source SOURCE --dest DEST --storage --interfaces [--force]

# Notes:
* Machines can be matched using system id, hostname, domain name or tags.
  See `utils.py:query_machines()` for details.
* This may be a destructive operation. The scripts asks for confirmation by
  default, but accepts a '--force' flag.
"""

import argparse
import logging

# logging.basicConfig(level=logging.DEBUG)

from maasjuju_toolkit.util import (
    query_machines, exit_with_error, session, MaaSError)


def clone_config(args):
    """Clones MaaS machines configuration"""
    sources = query_machines(args.source)
    if len(sources) > 1:
        exit_with_error('[ERROR] More than one source machines!: {}'.format(
            list(x.hostname for x in sources)))
    elif not sources:
        exit_with_error('[ERROR] No source machine!')

    destinations = query_machines(args.dest)
    if not destinations:
        exit_with_error('[ERROR] No destination machines!')

    source = sources[0]

    print('Will clone configuration from {} ({}) to:'.format(
        source.system_id, source.hostname
    ))
    for dest in destinations:
        print('* {} ({})'.format(dest.system_id, dest.hostname))

    if not args.force:
        re = input('Are you sure [y/N]? ')
        if re.lower() != 'y':
            exit_with_error('[ERROR] Aborted!')

    try:
        result = session().Machines.clone(
            # source=source.system_id,
            # destination=[x.system_id for x in destinations],
            interfaces=args.interfaces,
            storage=args.storage
        )

        print(result)

    except MaaSError as e:
        exit_with_error(f'[ERROR] MaaS: {e}')


def main():
    """parses arguments and does work"""

    parser = argparse.ArgumentParser(
        description='Αdd tags to many MaaS machines'
    )
    parser.add_argument('--source', type=str, required=True,
                        help='Source machine')
    parser.add_argument('--dest', type=str, required=True,
                        help='Destination machines')
    parser.add_argument('--interfaces', action='store_true', default=False,
                        help='Clone network interfaces configuration')
    parser.add_argument('--storage', action='store_true', default=False,
                        help='Clone storage configuration')
    parser.add_argument('--force', action='store_true', default=False,
                        help='Do not ask for confirmation')

    clone_config(args = parser.parse_args())


if __name__ == '__main__':
    main()