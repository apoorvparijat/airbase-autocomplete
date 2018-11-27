import unittest

from lib.Suggester import Suggester


class SuggesterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Read test data and load it as hash map """
        file = open('data/word_search.tsv', 'r')
        words_hash = {}
        for line in file:
            word_info = line.strip().split("\t")
            word = str(word_info[0])
            frequency = int(word_info[1])
            words_hash[word] = frequency
        cls.words_hash = words_hash
        cls.suggester = Suggester()

    def test_suggester_should_have_25_results(self):
        suggested_words = self.suggester.suggest_for('that')
        self.assertTrue(len(suggested_words) == 25)

    def test_suggester_should_be_typo_tolerant(self):
        self.assertTrue('greatness' in self.suggester.suggest_for('grtness'))
        self.assertTrue('greatness' in self.suggester.suggest_for('graetness'))

    def test_suggester_should_priortize_prefix(self):
        s = self.suggester.suggest_for('prac', 250)
        practical_index = s.index('practical')
        impractical_index = s.index('impractical')
        self.assertTrue(practical_index < impractical_index)

    def test_suggester_should_match_anywhere(self):
        s = self.suggester.suggest_for('eryx', 210)
        self.assertTrue('archaeopteryx' in s)

    def test_suggester_should_rank_short_words_before_longer_ones(self):
        s = self.suggester.suggest_for('environ', 250)
        environment_index = s.index('environment')
        environmentalism_index = s.index('environmentalism')
        self.assertTrue(environment_index < environmentalism_index)


if __name__ == '__main__':
    unittest.main()
