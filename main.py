import concurrent.futures

def load_config():
    with open("config", "r") as f:
        config = f.read()
    return config

def load_wordlist():
    with open(wordlistpath, "r") as f:
        wordlist = f.read().split("\n")
    return wordlist

config = load_config()
wordlistpath = config.split("wordlist=\"")[1].split("\"")[0]
wordlist = load_wordlist()

def is_correct(word):
    if word in wordlist:
        return True
    else:
        return False

def get_similarity_score(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    matrix = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]

    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

    score = 1 - matrix[len1][len2] / max(len1, len2)
    return score

def get_similar_worker(args):
    word, similarity_rate, wordlist_chunk = args
    similar_words = []
    for w in wordlist_chunk:
        score = get_similarity_score(word, w)
        if score >= similarity_rate:
            similar_words.append(w)
    return similar_words

def get_similar(word, similarity_rate, chunks=4):
    similar_words = []
    chunk_size = len(wordlist) // chunks

    chunks = [(word, similarity_rate, wordlist[i:i + chunk_size]) for i in range(0, len(wordlist), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(get_similar_worker, chunks))

    for similar_word_list in results:
        similar_words.extend(similar_word_list)

    if similar_words:
        return similar_words
    else:
        return None