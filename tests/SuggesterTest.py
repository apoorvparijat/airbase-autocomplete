import unittest

from lib.Suggester import Suggester


class SuggesterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file = open('data/word_search.tsv', 'r')
        words_hash = {}
        for line in file:
            word_info = line.strip().split("\t")
            word = str(word_info[0])
            frequency = int(word_info[1])
            words_hash[word] = frequency
        cls.words_hash = words_hash
        cls.suggester = Suggester()

    def test_suggest(self):
        suggested_words = self.suggester.suggest_for('apoorv')
        self.assertEqual(self, suggested_words == 25, True)


if __name__ == '__main__':
    unittest.main()
