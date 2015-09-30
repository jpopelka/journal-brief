"""
Copyright (c) 2015 Tim Waugh <tim@cyberelk.net>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""

from datetime import datetime
from flexmock import flexmock
from journal_brief.cli.main import CLI
import logging
from systemd import journal
from tempfile import NamedTemporaryFile


logging.basicConfig(level=logging.DEBUG)


class TestCLI(object):
    def test_param_override(self):
        with NamedTemporaryFile(mode='wt') as configfile:
            configfile.write('priority: err')
            configfile.flush()
            cli = CLI(args=['--conf', configfile.name])

            # Default value
            assert cli.config.get('cursor_file') == 'cursor'

            # Specified in config
            assert cli.config.get('priority') == 'err'

            # Specified on command-line
            cli = CLI(args=['--conf', configfile.name,
                            '-p', 'debug'])
            assert cli.config.get('priority') == 'debug'

    def test_dry_run(self):
        (flexmock(journal.Reader)
            .should_receive('get_next')
            .and_return({'__CURSOR': '1',
                         '__REALTIME_TIMESTAMP': datetime.now(),
                         'MESSAGE': 'message'})
            .and_return({}))

        with NamedTemporaryFile(mode='wt') as configfile:
            with NamedTemporaryFile(mode='rt') as cursorfile:
                configfile.write('cursor-file: {0}\n'.format(cursorfile.name))
                configfile.flush()
                cli = CLI(args=['--conf', configfile.name, '--dry-run'])
                cli.run()
                assert not cursorfile.read()
