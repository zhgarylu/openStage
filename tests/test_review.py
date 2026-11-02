import unittest
from scripts.review import approve
class ReviewTest(unittest.TestCase):
    def setUp(self):self.draft={'week':'2026-W46','review_state':'pending','projects':[{'id':1},{'id':2}]}
    def test_requires_explicit_selection(self):
        with self.assertRaises(ValueError):approve(self.draft,[],'editor','2026-11-02')
        with self.assertRaises(ValueError):approve(self.draft,[3],'editor','2026-11-02')
        with self.assertRaises(ValueError):approve(self.draft,[1],' ','2026-11-02')
    def test_approved_preserves_selected_order(self):
        result=approve(self.draft,[2,1],'editor','2026-11-02')
        self.assertEqual(result['review_state'],'approved');self.assertEqual([p['id'] for p in result['projects']],[2,1])
if __name__=='__main__':unittest.main()
