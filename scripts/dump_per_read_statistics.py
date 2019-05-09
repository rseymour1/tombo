#! /usr/bin/env python
"""Dump per-read statistics

This script takes a per-read statistics file and dumps its contents out into a tab-separated values file. The columns in the file are 'chrm', 'pos', 'strand', 'read_id' and 'stat'.
"""
from tombo import tombo_stats
from tombo.tombo_helper import intervalData
import argparse
import sys
import os

def extract_per_read_stats(fname):
    """Dump per-read statistics to tab-separated values"""
    if not os.path.isfile(fname):
        sys.exit('"{}" is not a valid file'.format(fname))

    pr_stats = tombo_stats.PerReadStats(fname)

    with open('per_read_stats.txt', 'w') as out_fp:
        out_fp.write('{}\t{}\t{}\t{}\t{}\n'.format(
            'chrm', 'pos', 'strand', 'read_id', 'stat'))
        for (chrm, strand), cs_blocks in pr_stats.blocks_index.items():
            for start, block_name in cs_blocks.items():
                for pos, stat, read_id in pr_stats.get_region_per_read_stats(
                        intervalData(chrm, start, start + pr_stats.region_size,
                                    strand)):
                    out_fp.write('{}\t{}\t{}\t{}\t{}\n'.format(
                        chrm, pos, strand, read_id, stat))


def main(fname):
    extract_per_read_stats(fname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="the per-read statistics file produced by tombo"
    )
    args = parser.parse_args()
    main(args.input_file)
