import heapq


class Suggester:

    def __init__(self):
        self.data_file_path = "data/word_search.tsv"
        self.words = []
        self.inverted_index_of_substr = {}
        self.min_char_exact_match = 3
        self.load_file_and_prepare_inverted_index()

    def add_all_inverted_index(self, word, word_index):
        """ Get all substring of length 'min_char_exact_match' from word, compute it's hash 
        and add the word's array index to all the substring key in the inverted_index_of_substr dictionary

        Example
        --------
        Given a word 'hello' whose index is 5 in self.words array, after this function finishes execution,
        the inverted_index_of_substr dictionary looks like

        {
            "hel": (5),
            "ell": (5),
            "llo": (5),
            ...
        }

        :param word:
        :param word_index: index of word in self.words
        :type word: string
        :type word_index: integer
        """
        for i in range(len(word)):
            j = i + self.min_char_exact_match
            if j <= len(word):
                substring_hash = self.compute_hash(word[i: j])
                if substring_hash in self.inverted_index_of_substr:
                    self.inverted_index_of_substr[substring_hash].add(word_index)
                else:
                    self.inverted_index_of_substr[substring_hash] = set()
                    self.inverted_index_of_substr[substring_hash].add(word_index)

    def calculate_score(self, word_index, word, user_input):
        """ Calculate the ranking score of word basis
        1. Frequency of occurence
        2. Length of the word
        3. Prefix index

        :param word_index: position/index of the word in self.words array
        :param word: the word whose score needs to be calculated
        :param user_input: string that user has typed in
        :type word_index: integer
        :type word: string
        :rtype float
        """
        weight_for_prefix_match = 0.6
        weight_for_frequency = 0.2
        if len(word) < len(user_input):
            return 0
        prefix_match = 0
        for i in range(min(len(word), len(user_input))):
            if word[i] == user_input[i]:
                prefix_match += 1
            else:
                break
        res = prefix_match * weight_for_prefix_match + weight_for_frequency * self.words[word_index][1]
        return res

    def compute_hash(self, s):
        """ Compute hash for a given string

        :param s: string to hash
        """
        p = 31
        m = int(1e9) + 9
        hash_value = 0
        p_pow = 1
        for c in s:
            hash_value = (hash_value + (ord(c) - ord('a') + 1) * p_pow) % m
            p_pow = (p_pow * p) % m
        return hash_value

    def load_file_and_prepare_inverted_index(self):
        """
        Load words in memory along with frequency.
        Also calculating the inverted index of substrings of length 3 to a list of word
        """
        data_file = open(self.data_file_path, 'r')
        word_index = 0
        for line in data_file:
            word_info = line.strip().split("\t")
            word = str(word_info[0])
            frequency = int(word_info[1])
            self.words.append((word, frequency))
            self.add_all_inverted_index(word, word_index)
            word_index += 1

    def get_array_index_of_suggested_words(self, word):
        """ Search for all the substring of "word" in inverted index and return combined set of all word array indexes
        :param word:
        :return:
        """
        array_index_of_suggested_words = set()
        for i in range(len(word)):
            j = i + self.min_char_exact_match
            if j <= len(word):
                substring_hash = self.compute_hash(word[i: j])
                if substring_hash in self.inverted_index_of_substr:
                    for word_index in self.inverted_index_of_substr[substring_hash]:
                        array_index_of_suggested_words.add(word_index)
        # print("array_index_of_suggested_words %s" % len(array_index_of_suggested_words))
        return array_index_of_suggested_words

    def suggest_for(self, user_input, num_words=25):
        """ :returns as list of words for auto suggestion. List length is limited by num_words

        :param user_input:
        :param num_words:
        :return:
        """
        word_index_of_suggestions = self.get_array_index_of_suggested_words(user_input)
        results = []
        for index in word_index_of_suggestions:
            word = self.words[index][0]
            heapq.heappush(results, (self.calculate_score(index, word, user_input), word))

        sorted_results = heapq.nlargest(num_words, results)
        return map(lambda result: result[1], sorted_results)
