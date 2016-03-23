import json
from neurofinder import load, match, similarity, overlap

a = load('a.json')
b = load('b.json')

#print(match(a, b, min_distance=5))
print(similarity(a, b))

# recall, precision = similarity(a, b, metric='distance', minDistance=threshold)
# stats = overlap(a, b, method='rates', minDistance=threshold)

# score = 2 * (recall * precision) / (recall + precision)

# if sum(~isnan(stats)) > 0:
#     overlap, exactness = tuple(nanmean(stats, axis=0))
# else:
#     overlap, exactness = 0.0, 1.0