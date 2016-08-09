__author__ = 'plaix'
import codecs, os, string, math

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/')

def prob_dist(file):
    data = ""
    with codecs.open(DATA_PATH + file, encoding='utf-8', errors='ignore') as f:
        data = f.read()

    for c in string.punctuation:
        data = data.replace(c, "")
    data = data.lower().split()

    # stop = stopwords.words('english')
    # data = [token for token in data if token not in stop]

    # lemmatizer = WordNetLemmatizer()
    # data = [str(lemmatizer.lemmatize(token)) for token in data]

    prob_dist = dict()
    data_size = len(data)
    for token in data:
        if token not in prob_dist:
            prob_dist[token] = data.count(token) / float(data_size)

    return prob_dist

def KL_divergence(dist, dist2):
    tokens = []
    divergence = 0
    # for token in dist:
    #     tokens.append(token)
    for token in dist2:
        tokens.append(token)
    tokens = set(tokens)
    vocabulary_size = len(tokens)
    epsilon = 1e-7
    collection_size = len(dist2)

    def lidstone_second(token):
        value = dist2[token] if token in dist2 else 0
        return (value + epsilon) / (collection_size + epsilon*vocabulary_size)

    for token in dist:
        divergence += dist[token] * math.log(dist[token]/lidstone_second(token))

    return divergence

prob_d = prob_dist('TomSawyerPart1.txt')
#prob_d2 = prob_dist('TomSawyerPart2.txt')
prob_d3 = prob_dist('Moby.txt')
#prob_d4 = prob_dist('TomSawyerGerman.txt')
print(KL_divergence(prob_d, prob_d3))