import pytest
from scorer import RecommendationScorer

def relevance_score(u, i, ctx): 
    return 0.9 if i == "item1" else 0.4
    
def popularity_score(u, i, ctx): 
    return 0.8 if i in ["item1", "item2"] else 0.2

class TestRecommendationScorer:
    def setup_method(self):
        self.scorer = RecommendationScorer()
        self.scorer.add_scorer("Relevance", relevance_score, weight=0.7)
        self.scorer.add_scorer("Popularity", popularity_score, weight=0.3)

    def test_calculate_score(self):
        score, explanation = self.scorer.calculate_score("user1", "item1")
        assert pytest.approx(score, 0.01) == 0.87
        assert "Relevance" in explanation
        assert "Popularity" in explanation

    def test_rank_candidates(self):
        candidates = ["item1", "item2", "item3"]
        ranked = self.scorer.rank_candidates("user1", candidates)
        
        assert len(ranked) == 3
        assert ranked[0]["item_id"] == "item1"
        assert ranked[1]["item_id"] == "item2"
        assert ranked[2]["item_id"] == "item3"

    def test_rank_empty_candidates(self):
        assert self.scorer.rank_candidates("user1", []) == []

    def test_scorer_no_registered_functions(self):
        empty_scorer = RecommendationScorer()
        score, expl = empty_scorer.calculate_score("u", "i")
        assert score == 0.0
        assert "No scorers" in expl
