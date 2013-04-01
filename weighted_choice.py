"""
Credit: https://github.com/Anaphory/weighted_choice/blob/master/__init__.py
"""

import numpy.random
import bisect


def weighted_choice(weights, random=numpy.random):
    """ Weighted choice from a list or dict
    
    Given a dictionary {k_0: w_0, k_1: w_1, ...} or a sequence [w_0,
    w_1, ...], with non-negative numbers w_0, w_1, ..., return a
    random key k_i resp. a random index i with probability
    proportional to w_i.
    """
    try:
        rnd = random.random() * sum(weights.values())
    except AttributeError:
        rnd = random.random() * sum(weights)
        
    if rnd < 0:
        raise ValueError("Sum of weights is negative")

    try:
        iteration = weights.items()
    except AttributeError:
        iteration = enumerate(weights)
    for i, w in iteration:
        if w<0:
            raise ValueError("Negative weight encountered.")
        rnd -= w
        if rnd < 0:
            return i
    raise ValueError("Sum of weights is not positive")

W, V, TW = (0, 1, 2)

def weighted_heap(frequencies):
    # h is the heap. It's like a binary tree that lives in an array.
    # It has a Node for each pair in `frequencies`. h[1] is the root. Each
    # other Node h[i] has a parent at h[i>>1]. Each node has up to 2
    # children, h[i<<1] and h[(i<<1)+1].  To get this nice simple
    # arithmetic, we have to leave h[0] vacant.
    h = [None]                          # leave h[0] vacant
    for v, w in enumerate(frequencies):
        h.append([w, v, w])
    for i in range(len(h) - 1, 1, -1):  # total up the tws
        h[i>>1][TW] += h[i][TW]           # add h[i]'s total to its parent
    return h

def weighted_heap_pop(h, random=numpy.random):
    if h[1][TW] < 1:
        raise IndexError("pop from empty heap")

    gas = h[1][TW]* random.random()     # start with a random amount of gas

    i = 1                     # start driving at the root
    while gas > h[i][W]:      # while we have enough gas to get past node i:
        gas -= h[i][W]        #   drive past node i
        i <<= 1               #   move to first child
        if gas > h[i][TW]:    #   if we have enough gas:
            gas -= h[i][TW]   #     drive past first child and descendants
            i += 1            #     move to second child
    w = h[i][W]               # out of gas! h[i] is the selected node.
    v = h[i][V]

    h[i][W] -= 1              # make sure this node isn't chosen again
    while i:                  # fix up total weights
        h[i][TW] -= 1
        i >>= 1
    return v

def weighted_sample(frequencies, n, random=numpy.random):
    heap = weighted_heap(frequencies)        # just make a heap...
    for i in range(n):
        yield weighted_heap_pop(heap)        # and pop n frequencies off it.

def weighted_sample_histogram(frequencies, k, random=numpy.random):
    W = sum(frequencies)
    for frequency in frequencies:
        if k < 1:
            yield 0
        else:
            if frequency >= 1:
                W -= frequency
                if W < 1:
                    if k <= frequency:
                        good = k
                    else:
                        raise ValueError("Sum of absolute frequencies less than number of samples")
                else:
                    good = numpy.random.hypergeometric(frequency, W, k)
            else:
                good = 0
            k -= good
            yield good
    raise StopIteration