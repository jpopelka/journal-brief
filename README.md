# journal-brief
Show new systemd journal entries since last run.

This can be run from cron to get a briefing of journal entries sent by
email.  Example:

```
$ cat /etc/cron.daily/journal-brief
#!/bin/sh
exec journal-brief -p err
```

## Configuration

A YAML configuration in `~/.config/journal-brief/journal-brief.conf`
defines which journal entries should be shown.

### Inclusions

Each inclusion is defined by a list of journal fields and their
possible matches. All fields defined in an inclusion must match at
least one of their possible match values for an entry to be included.

For example, the configuration below matches all entries of priority 3
(err) or lower (like `journalctl -p err`), but also includes entries
of priority 6 or lower from the specified systemd unit (like
`journalctl -p info -u myservice.service`):

```yaml
inclusions:
- PRIORITY: [0, 1, 2, 3]
- PRIORITY: [4, 5, 6]
  _SYSTEMD_UNIT: [myservice.service]
```

The `priority` configuration parameter sets the log level to add to
all inclusions, and if the PRIORITY field match is not a list it is
matched as a maximum value so the above could be written as:

```yaml
priority: err
inclusions:
- PRIORITY: info
  _SYSTEMD_UNIT: [myservice.service]
```


### Exclusions

Each exclusion is defined by a list of journal fields and their
possible matches. All fields in an exclusion must match at least one
of their possible match values for an entry to be excluded.

For example:

```yaml
exclusions:
- MESSAGE:
  - exclude this
  - exclude this too
  SYSLOG_IDENTIFIER:
  - from here
- MESSAGE_ID: [c7a787079b354eaaa9e77b371893cd27]
- MESSAGE: ["/Normal exit \(.*run\)/"]
```

This would cause `journal-brief` to ignore journal entries that
satisfy both conditions: `SYSLOG_IDENTIFIER` is `from here`, and
`MESSAGE` is either `exclude this` or `exclude this too`.

It will also ignore any entries with the specified `MESSAGE_ID`.

In addition, any entries whose `MESSAGE` matches the regular
expression `Normal exit \(.*run\)` will be excluded. Regular
expressions are indicated with `/` at the beginning and end of the
match string.

The available journal fields are described in the
systemd.journal-fields(7) manual page.

## Install

### From git
```
python3 setup.py install
```

### From PyPI
```
pip3 install journal-brief
```
