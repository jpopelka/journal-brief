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

import tests.util
from journal_brief.config import Config, ConfigError
import logging
from tempfile import NamedTemporaryFile
import pytest
import yaml


logging.basicConfig(level=logging.DEBUG)


class TestConfig(object):
    @pytest.mark.parametrize('badyaml', [
        """
exclusions
  - MESSAGE: [foo]
        """,
    ])
    def test_validation_bad_yaml(self, badyaml):
        with NamedTemporaryFile(mode='wt') as cfp:
            cfp.write(badyaml.strip())
            cfp.flush()
            with pytest.raises(ConfigError):
                cfg = Config(config_file=cfp.name)

    @pytest.mark.parametrize('badconfig', [
        "disallowed: 1",
        "cursor-file: [1]",
        "debug: [1]",
        "debug: debug",
        "output: none",
        "output: [json]",
        "priority: -1",
        "priority: [0, 1, 2, error, 2]",

        # Test multiple errors
        """
disallowed: 1
cursor-file: [1]
debug: [1]
        """,
    ])
    def test_validation_bad(self, badconfig):
        with NamedTemporaryFile(mode='wt') as cfp:
            cfp.write(badconfig.strip())
            cfp.flush()
            with pytest.raises(ConfigError):
                cfg = Config(config_file=cfp.name)

    @pytest.mark.parametrize('badconfig', [
        "{key}: 1",
        """
{key}:
  map: 1
        """,
        """
{key}:
  - 1
        """,
        """
{key}:
  - PRIORITY: [-1]
        """,
        """
{key}:
  - PRIORITY: -1
        """,
        """
{key}:
  - PRIORITY:
      map: 1
        """,
        """
{key}:
  - MESSAGE: 1
        """,
        """
{key}:
  - MESSAGE: [baz]
  - MESSAGE:
      - foo
      - [bar]
        """,
    ])
    @pytest.mark.parametrize('key', ['inclusions', 'exclusions'])
    def test_validation_bad_inclusion_exclusion(self, key, badconfig):
        with NamedTemporaryFile(mode='wt') as cfp:
            cfp.write(badconfig.format(key=key).strip())
            cfp.flush()
            with pytest.raises(ConfigError):
                cfg = Config(config_file=cfp.name)

    @pytest.mark.parametrize('badconfig', [
        """
exclusions:
  - MESSAGE: [/(mismatched parenth/]
        """,
    ])
    def test_validation_bad_regex(self, badconfig):
        with NamedTemporaryFile(mode='wt') as cfp:
            cfp.write(badconfig.strip())
            cfp.flush()
            with pytest.raises(ConfigError):
                cfg = Config(config_file=cfp.name)