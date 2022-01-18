import bashparse, metric

filename = ''


nodes = bashparse.parse(open(filename).read())

print('len nodes: ', len(nodes))
print('raw score: ', calculate_raw_file_score(nodes))
print('weighted score: ', calculate_weighted_file_score(nodes))
print('hashed raw score: ', calculate_raw_hashing_score(nodes))
print('hashed weighted score: ', calculate_weighted_hasing_score(nodes))

