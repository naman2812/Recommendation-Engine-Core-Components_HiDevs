import pytest
from evaluator import RecommendationEvaluator

class TestRecommendationEvaluator:
    def setup_method(self):
        self.evaluator = RecommendationEvaluator()
        
    def test_precision_at_k(self):
        recs = ["item1", "item2", "item3"]
        truth = ["item1", "item4"]
        
        assert self.evaluator.precision_at_k(recs, truth, k=3) == 1/3
        assert self.evaluator.precision_at_k(recs, truth, k=1) == 1.0
        
    def test_recall_at_k(self):
        recs = ["item1", "item2", "item3"]
        truth = ["item1", "item4"]
        
        assert self.evaluator.recall_at_k(recs, truth, k=3) == 0.5
        
    def test_ndcg_at_k(self):
        recs = ["item1", "item2", "item3"]
        truth = ["item3"]
        
        ndcg = self.evaluator.ndcg_at_k(recs, truth, k=3)
        assert ndcg > 0.0 and ndcg < 1.0 # item3 is at rank 3, so DCG < IDCG
        
        truth2 = ["item1"]
        assert self.evaluator.ndcg_at_k(recs, truth2, k=3) == 1.0 # Perfect ranking
        
    def test_evaluate_all(self):
        recommendations = {
            "user1": ["item1", "item2", "item3", "item4"],
            "user2": ["item5", "item6", "item7"]
        }
        ground_truth = {
            "user1": ["item1", "item3", "item8"], 
            "user2": ["item9"]                    
        }
        
        metrics = self.evaluator.evaluate_all(recommendations, ground_truth, k=3)
        
        assert "precision@3" in metrics
        assert "recall@3" in metrics
        assert "ndcg@3" in metrics
        
        # user1 has 2 hits (prec=2/3, rec=2/3)
        # user2 has 0 hits (prec=0, rec=0)
        # Average precision = (2/3 + 0) / 2 = 1/3
        assert pytest.approx(metrics["precision@3"], 0.01) == 0.333
