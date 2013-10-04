'''Copy data from one client to another existing client.

Usage:
    exo [options] datacopy <cik> <destcik> [--ids=<id1,id2,idN>] [--count=<n>]

Options:
    --create          Create any resources that do not exist (Non-Functional).
    --count=<n>       Number of datapoints to copy [default: 200].'''
import re
import os

import yaml

class Plugin():
    def command(self):
        return 'datacopy'
    def run(self, cmd, args, options):
        cik = options['cik']
        rpc = options['rpc']
        ExoException = options['exception']
        if cmd == 'datacopy':
            count = int(args['--count'])
            destcik = args['<destcik>']

            print("Getting Source Tree for {0}".format(cik))
            infotreesrc = rpc._infotree(cik)
            print("Getting Destination Tree for {0}".format(destcik))
            infotreedest = rpc._infotree(destcik)


            for rid, aliases in infotreesrc["info"]["aliases"].items():
                destrid = None

                for alias in aliases:
                    for drid, daliases in infotreedest["info"]["aliases"].items():
                        if alias in daliases:
                            destrid = drid

                if destrid is not None:
                    print("Reading:\t{0}".format(aliases[0]))
                    try:
                        entries = rpc.read(cik, rid, count, sort='desc')
                    except: #Need a reference to OnePlatformException here.
                        print("Error Reading Data")
                        continue

                    print("Writing:\t{0}".format(aliases[0]))
                    try:
                        rpc.record(destcik, destrid, entries)
                    except: #Need a reference to OnePlatformException here.
                        print("Error Copying Some Data, Maybe Duplicates?")
                else:
                    print("Not found in destination:\t{0}".format(aliases[0]))
