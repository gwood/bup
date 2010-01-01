#!/usr/bin/env python
import sys, time
import hashsplit, git, options
from helpers import *

optspec = """
bup split [-t] [filenames...]
--
b,blobs    output a series of blob ids
t,tree     output a tree id
c,commit   output a commit id
n,name=    name of backup set to update (if any)
bench      print benchmark timings to stderr
"""
o = options.Options('bup split', optspec)
(opt, flags, extra) = o.parse(sys.argv[1:])

if not (opt.blobs or opt.tree or opt.commit or opt.name):
    log("bup split: use one or more of -b, -t, -c, -n\n")
    o.usage()

start_time = time.time()

(shalist,tree) = hashsplit.split_to_tree(hashsplit.autofiles(extra))
if opt.blobs:
    for (mode,name,sum) in shalist:
        print sum
if opt.tree:
    print tree
if opt.commit or opt.name:
    msg = 'Generated by command:\n%r' % sys.argv
    ref = opt.name and ('refs/heads/%s' % opt.name) or None
    commit = git.gen_commit_easy(ref, tree, msg)
    if opt.commit:
        print commit

secs = time.time() - start_time
if opt.bench:
    log('\nbup: %.2fkbytes in %.2f secs = %.2f kbytes/sec\n'
        % (ofs/1024., secs, ofs/1024./secs))
