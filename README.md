# Towers of Hanoi backup pruning

A script to identify which backups can be deleted
based on a Towers of Hanoi exponential retention
backup rotation policy.

Given a list of archive names ending in a timestamp,
prints a list of archive names to delete.
Archive names need to end in the format `_%Y-%m-%d_%H-%M-%S`.

Rather than recording a track and sequence number
with each backup, this infers that information
from the timestamp on each backup.

Multiple backups on the same day are considered to be a "single"
backup -- that is, if day 2020-12-28 is to be retained, all backups
for that day are retained.

The default configuration is to treat the expected minimum backup
frequency as daily, and to keep two from each track.
