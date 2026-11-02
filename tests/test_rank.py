import unittest
from scripts.rank import calculate
class RankTest(unittest.TestCase):
    def test_missing_history_is_not_zero(self):
        old={'projects':[{'id':1,'stars':10}]}
        new={'projects':[{'id':1,'stars':15,'full_name':'a/b'},{'id':2,'stars':50,'full_name':'c/d'}]}
        self.assertEqual(calculate(old,new),[{'id':1,'full_name':'a/b','stars':15,'delta7':5,'growth_pct':50.0}])
    def test_zero_base_and_negative_delta(self):
        old={'projects':[{'id':1,'stars':0},{'id':2,'stars':9}]}
        new={'projects':[{'id':1,'stars':3,'full_name':'a/b'},{'id':2,'stars':7,'full_name':'c/d'}]}
        result=calculate(old,new)
        self.assertIsNone(result[0]['growth_pct']); self.assertEqual(result[1]['delta7'],-2)
if __name__ == '__main__': unittest.main()
