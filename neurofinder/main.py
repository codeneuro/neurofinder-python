import json
import os
from numpy import inf, NaN, newaxis, argmin, delete, asarray, isnan, sum, nanmean
from scipy.spatial.distance import cdist
from regional import one, many

def load(file):
    """
    Load neuronal regions from a file or string.
    """
    if os.path.isfile(file):
        with open(file, 'r') as f:
            values = json.load(f)
    else:
        values = json.loads(file)

    return many([v['coordinates'] for v in values])
        
def match(a, b, threshold=inf):
    """
    Find unique matches between two sets of regions.

    Params
    ------
    a, b : regions
        The regions to match.

    threshold : scalar, optional, default = inf
        Threshold distance to use when selecting matches.
    """
    targets = b.center
    target_inds = range(0, len(targets))
    matches = []
    for s in a:
        update = 1

        # skip if no targets left, otherwise update
        if len(targets) == 0:
            update = 0
        else:
            dists = cdist(targets, s.center[newaxis])
            if dists.min() < threshold:
                ind = argmin(dists)
            else:
                update = 0

        # apply updates, otherwise add a nan
        if update == 1:
            matches.append(target_inds[ind])
            targets = delete(targets, ind, axis=0)
            target_inds = delete(target_inds, ind)
        else:
            matches.append(NaN)

    return matches

def shapes(a, b, threshold=inf):
    """
    Compare shapes between two sets of regions.

    Parameters
    ----------
    a, b : regions
        The regions for which to estimate overlap.

    threshold : scalar, optional, default = inf
        Threshold distance to use when matching indices.
    """
    inds = match(a, b, threshold=threshold)
    d = []
    for jj, ii in enumerate(inds):
        if ii is not NaN:
            d.append(a[jj].overlap(b[ii], method='rates'))
        else:
            d.append((NaN, NaN))

    result = asarray(d)

    if sum(~isnan(result)) > 0:
        inclusion, exclusion = tuple(nanmean(result, axis=0))
    else:
        inclusion, exclusion = 0.0, 0.0

    return inclusion, exclusion

def centers(a, b, threshold=inf):
    """
    Compare centers between two sets of regions.

    The recall rate is the number of matches divided by the number in self,
    and the precision rate is the number of matches divided by the number in other.
    Typically a is ground truth and b is an estimate.
    The F score is defined as 2 * (recall * precision) / (recall + precision)

    Before computing metrics, all sources in self are matched to other,
    and a threshold can be set to control matching.

    Parameters
    ----------
    a, b : regions
        The regions for which to estimate overlap.

    threshold : scalar, optional, default = 5
        The distance below which a source is considered found.
    """
    inds = match(a, b, threshold=threshold)

    d = []
    for jj, ii in enumerate(inds):
        if ii is not NaN:
            d.append(a[jj].distance(b[ii]))
        else:
            d.append(NaN)

    result = asarray(d)

    result[isnan(result)] = inf
    compare = lambda x: x < threshold

    recall = sum(asarray(list(map(compare, result)))) / float(a.count)
    precision = sum(asarray(list(map(compare, result)))) / float(b.count)

    return recall, precision