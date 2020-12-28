#!/usr/bin/env python3

import datetime
import re
import sys


# Seconds between backups, nominally (timestamp divisor for sequence number)
seq_granularity = 24 * 60 * 60
# Number of backups to keep per track (duplicate seqs count as 1)
seqs_keep_per_track = 2


def date_of_archive(archive_name):
    m = re.search(r'_(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}$)', archive_name)
    datestr = m.groupdict()['date']
    date = datetime.datetime.strptime(datestr, '%Y-%m-%d_%H-%M-%S')
    return date


def track_from_seq(seq):
    track = 0
    # Treat sequence number zero like a daily (an odd number) to avoid
    # the infinite loop.
    if seq < 1:
        return track
    while seq % 2 == 0:
        track += 1
        seq /= 2
    return track


def archive_info(archive_name):
    date = date_of_archive(archive_name)
    seq = int(date.timestamp() / seq_granularity)
    track = track_from_seq(seq)
    return {
        'name': archive_name,
        'date': date,
        'seq': seq,
        'track': track,
    }


def find_deletes_for_track(archives):
    seqnums = sorted(a['seq'] for a in archives)
    keep_seqs = set(seqnums[-seqs_keep_per_track:])
    return [a for a in archives if a['seq'] not in keep_seqs]


def find_deletes(archive_names):
    ainfo = [archive_info(n) for n in archive_names]
    trackvals = {a['track'] for a in ainfo}

    def delnames_by_tracknum(tv):
        track = [a for a in ainfo if a['track'] == tv]
        return [a['name'] for a in find_deletes_for_track(track)]
    
    return [a for tv in trackvals for a in delnames_by_tracknum(tv)]


def main():
    """
    Read archive names from stdin and print to-delete names to stdout.
    
    Archive names are newline separated.
    """
    names = [l.rstrip('\n') for l in sys.stdin]
    if names:
        for d in find_deletes(names):
            print(d)


if __name__ == '__main__':
    main()
