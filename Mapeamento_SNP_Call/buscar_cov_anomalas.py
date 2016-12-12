"""Count gaps in BAM/SAM files.

Usage:
     find_gaps.py [--coverage=<cov>] INPUT SAMPLE
     find_gaps.py (-h | --help)

Options:
     -h --help                   show this
     -c <cov>, --coverage <cov>  especify the minimum coverage to account for [default: 2]

"""

import pysam
import matplotlib.pyplot as plt
from docopt import docopt
import numpy as np

def find_gaps(args):
    print("Where are the gaps below {}x ?".format(args['--coverage']))
    sampath = args['INPUT']
    samfile = pysam.AlignmentFile(sampath,"rb")
    # until_eof=True defines that input sam doesnt have a index
    # uncomment the 2 lines below to print all reads aligned to samfile
    # for read in samfile.fetch(until_eof=True):
    #     print (read)
    # Checking if sam has index
    try:
        if samfile.check_index() == True:
            "The alignment file has an index."
    # if it doesnt, create an index
    except ValueError:
        pysam.index(samfile.filename, catch_stdout=False)
    # count the number of reads in chr ref
    # print samfile.count(reference='ref',until_eof=True)
    # this gives a tuple with references names
    chromossomes = samfile.references
    # this gives a tuple of length of references in the same order as references tuple 
    len_chromossomes = samfile.lengths
    # iterate over each base of all references (chromossomes) and print the coverage
    bases = []
    for idx in xrange(len(chromossomes)):
        pos_low = 0
	# gen_start specify that the chromossomes starts at base 0. It will be used to account for positions in the genome that doesnt have pileup reads.
	# Threfore, it will count the zero zero positions.
        gen_start = 0
        for pileupcolumn in samfile.pileup(reference=chromossomes[idx], start=0, end=len_chromossomes[idx],stepper='nofilter'):
            n=0
            pos = pileupcolumn.pos
            # we check what's the size of zero zero interval
            size_zero = abs(gen_start - pos)
            # if it's size is at least one we record it
            if size_zero >= 1:
                bases.append((size_zero,0))
            # the new genome position to keep track is now the current
            gen_start = pos + 1
#            print ("\ncoverage at base %s = %s" %
#               (pileupcolumn.pos, pileupcolumn.n))
            for pileupread in pileupcolumn.pileups:
		# query position is None if is_del or is_refskip is set. We're rejecting positions which has these kind of variants
                if not pileupread.is_del and not pileupread.is_refskip:
                    n += 1
            if n <= int(args['--coverage']):
                pos_low = pos_low + 1
            else:
                if (pos_low != 0):
                    bases.append((pos_low, pos-1))
                pos_low=0
        if (pos_low != 0):
            bases.append((pos_low,pos))
    samfile.close()
    return bases

if __name__ == '__main__':
    arguments = docopt(__doc__)
#    print(arguments)
    gaps = find_gaps(arguments)
    sample_name=arguments['SAMPLE']
    cov_array=np.array([x[0] for x in gaps])
    total = sum(cov_array)
    print("Total bases <= {} is {}".format(arguments['--coverage'],total))
    for n_cov in gaps:
        print("{sample}\t{cov}".format(sample=sample_name, cov=n_cov[0]))
