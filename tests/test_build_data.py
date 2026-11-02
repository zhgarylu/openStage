import json,tempfile,unittest
from pathlib import Path
from scripts.build_data import build
class BuildDataTest(unittest.TestCase):
    def test_only_approved_is_public(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'data/weekly/approved').mkdir(parents=True)
            (root/'data/projects.json').write_text(json.dumps({'projects':[{'id':1,'stars':1}]}))
            (root/'data/weekly/pending.json').write_text(json.dumps({'review_state':'pending'}))
            (root/'data/weekly/approved/notapproved.json').write_text(json.dumps({'review_state':'pending'}))
            (root/'data/weekly/approved/approved.json').write_text(json.dumps({'review_state':'approved','reviewed_by':'A','reviewed_at':'today','projects':[]}))
            build(root)
            out=json.loads((root/'site/src/data/weekly.json').read_text())
            self.assertEqual(len(out),1);self.assertEqual(out[0]['reviewed_by'],'A')
if __name__=='__main__':unittest.main()
