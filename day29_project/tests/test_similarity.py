import pytest
from similarity import SimilarityCalculator

class TestSimilarityCalculator:
    def setup_method(self):
        self.calc = SimilarityCalculator()

    def test_cosine_similarity(self):
        v1 = {"item1": 5, "item2": 3}
        v2 = {"item1": 4, "item2": 2}
        v3 = {"item3": 5}
        
        sim12 = self.calc.cosine_similarity(v1, v2)
        sim13 = self.calc.cosine_similarity(v1, v3)
        
        assert pytest.approx(sim12, 0.01) == 0.997
        assert sim13 == 0.0
        
    def test_cosine_similarity_empty(self):
        assert self.calc.cosine_similarity({}, {"a": 1}) == 0.0
        assert self.calc.cosine_similarity({}, {}) == 0.0

    def test_jaccard_similarity(self):
        s1 = {"python", "java", "c++"}
        s2 = {"python", "javascript", "ruby"}
        
        sim = self.calc.jaccard_similarity(s1, s2)
        assert sim == 0.2
        
    def test_jaccard_similarity_empty(self):
        assert self.calc.jaccard_similarity(set(), set()) == 1.0
        assert self.calc.jaccard_similarity({"a"}, set()) == 0.0

    def test_pearson_correlation(self):
        r1 = {"item1": 5, "item2": 3, "item3": 2}
        r2 = {"item1": 4, "item2": 2, "item3": 1}
        r3 = {"item1": 1, "item2": 3, "item3": 5}
        
        corr12 = self.calc.pearson_correlation(r1, r2)
        corr13 = self.calc.pearson_correlation(r1, r3)
        
        assert pytest.approx(corr12, 0.01) == 1.0
        assert pytest.approx(corr13, 0.01) == -0.982
        
    def test_pearson_correlation_empty(self):
        assert self.calc.pearson_correlation({}, {"a": 1}) == 0.0
        assert self.calc.pearson_correlation({}, {}) == 0.0
