import unittest
from main import Earley


class EasyTestFromExample(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 1, 2, 2
        G['neterms'] = 'T'
        G['alphabet'] = 'ab'
        G['rules'] = ['T->aTbT',
                      'T->']
        G['start_symbol'] = 'T'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("aababb", True),
            ("aabbba", False),
            ("abbab", False),
            ("aaababbb", True),
            ("abba", False),
            ("ab", True),
            ("", True)
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)


class CheckWayFromNetermToNeterm(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 3, 4, 8
        G['neterms'] = 'SMT'
        G['alphabet'] = 'abcdpm'
        G['rules'] = ['S->SpM',
                      'S->M',
                      'M->MmT',
                      'M->T',
                      'T->a',
                      'T->b',
                      'T->c',
                      'T->d']
        G['start_symbol'] = 'S'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("apbmd", True),
            ("apbmcpd", True),
            ("apd", True),
            ("a", True),
            ("apmd", False),
            ("dp", False),
            ("p", False),
            ("zzzzzzzzz", False),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)


class CheckDoubleNeterminalInGrammar(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 4, 2, 5
        G['neterms'] = 'SABQ'
        G['alphabet'] = 'aw'
        G['rules'] = ['S->aSS',
                      'S->SA',
                      'A->Aa',
                      'A->BAw',
                      'Q->']
        G['start_symbol'] = 'S'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("aaaaa", False),
            ("awa", False),
            ("", False),
            ("a", False),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)


class CheckMoreEmptyNeterminals(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 3, 3, 5
        G['neterms'] = 'SABQ'
        G['alphabet'] = 'abc'
        G['rules'] = ['S->aAbB',
                      'A->cA',
                      'B->ccB',
                      'A->',
                      'B->']
        G['start_symbol'] = 'S'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("acbcc", True),
            ("acccbccc", False),
            ("acbc", False),
            ("accccbcccccc", True),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)


class MiddleTest1(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 4, 3, 8
        G['neterms'] = 'STUV'
        G['alphabet'] = 'abc'
        G['rules'] = ['S->aTc',
                      'S->cS',
                      'T->aU',
                      'T->aT',
                      'U->aU',
                      'U->V',
                      'V->bV',
                      'V->c']
        G['start_symbol'] = 'S'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("caaacc", True),
            ("aacc", True),
            ("cccacc", False),
            ("aabbbbcc", True),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)


class MiddleTest2(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 3, 3, 6
        G['neterms'] = 'STU'
        G['alphabet'] = 'abc'
        G['rules'] = ['S->bT',
                      'S->a',
                      'T->cUac',
                      'T->',
                      'U->bSab',
                      'U->a']
        G['start_symbol'] = 'S'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("bcbaabac", True),
            ("bcbcabac", False),
            ("bcbac", False),
            ("a", True),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)


class TheStrongestTestWithTheLongestStrings(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        G = dict()
        G['kol_neterms'], G['kol_terms'], G['kol_rules'] = 3, 2, 6
        G['neterms'] = 'STU'
        G['alphabet'] = 'bc'
        G['rules'] = ['S->SbSb',
                      'S->Tb',
                      'S->bS',
                      'S->cU',
                      'T->Ub',
                      'U->']
        G['start_symbol'] = 'S'
        self.earley.fit(G)

    def runTest(self):
        expected = [
            ("bbbcb", True),
            ("bbbbbbbbcc", False),
            ("bbbbbbbbbbbbbbbbcbcbcbb", True),
            ("bbbbbbbbbbbbbb", True),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.predict_result(string), result)



if __name__ == '__main__':
    unittest.main()
