import json
from numpy import inf, NaN, newaxis, argmin, delete, asarray, isnan, sum, nanmean
from scipy.spatial.distance import cdist
from regional import one, many

def load(file):
    """
    Load neuronal regions from a file.
    """
    with open(file, 'r') as f:
        values = json.load(f)
        return many([v['coordinates'] for v in values])
    
def match(a, b, unique=True, min_distance=inf):
    """
    Find matches between two sets of regions.

    Can select nearest matches with or without enforcing uniqueness;
    if unique is False, will return the closest source in other for
    each source in self, possibly repeating sources multiple times
    if unique is True, will only allow each source in other to be matched
    with a single source in self, as determined by a greedy selection procedure.
    The min_distance parameter can be used to prevent far-away sources from being
    chosen during greedy selection.

    Params
    ------
    a, b : regions
        The regions to match.

    unique : boolean, optional, deafult = True
        Whether to only return unique matches.

    min_distance : scalar, optiona, default = inf
        Minimum distance to use when selecting matches.
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
            if dists.min() < min_distance:
                ind = argmin(dists)
            else:
                update = 0

        # apply updates, otherwise add a nan
        if update == 1:
            matches.append(target_inds[ind])
            if unique is True:
                targets = delete(targets, ind, axis=0)
                target_inds = delete(target_inds, ind)
        else:
            matches.append(NaN)

    return matches

def shapes(a, b, min_distance=inf):
    """
    Compare shapes between two sets of regions.
    
    Parameters
    ----------
    a, b : regions
        The regions for which to estimate overlap.

    min_distance : scalar, optional, default = inf
        Minimum distance to use when matching indices.
    """
    inds = match(a, b, unique=True, min_distance=min_distance)
    d = []
    for jj, ii in enumerate(inds):
        if ii is not NaN:
            d.append(a[jj].overlap(b[ii], method='rates'))
        else:
            d.append((NaN, NaN))

    result = asarray(d)

    if sum(~isnan(result)) > 0:
        overlap, exactness = tuple(nanmean(result, axis=0))
    else:
        overlap, exactness = 0.0, 1.0

    return overlap, exactness

def centers(a, b, threshold=5):
    """
    Compare centers between two sets of regions.

    The recall rate is the number of matches divided by the number in self,
    and the precision rate is the number of matches divided by the number in other.
    Typically a is ground truth and b is an estimate.
    The F score is defined as 2 * (recall * precision) / (recall + precision)

    Before computing metrics, all sources in self are matched to other,
    and a minimum distance can be set to control matching.

    Parameters
    ----------
    a, b : regions
        The regions for which to estimate overlap.

    threshold : scalar, optional, default = 5
        The distance below which a source is considered found.

    min_distance : scalar, optional, default = inf
        Minimum distance to use when matching indices.
    """
    inds = match(a, b, unique=True, min_distance=threshold)

    d = []
    for jj, ii in enumerate(inds):
        if ii is not NaN:
            d.append(a[jj].distance(b[ii]))
        else:
            d.append(NaN)

    result = asarray(d)

    result[isnan(result)] = inf
    compare = lambda x: x < threshold

    recall = sum(map(compare, result)) / float(a.count)
    precision = sum(map(compare, result)) / float(b.count)

    return recall, precision