"""
Tests for sentiment analysis utility functions using context7.
"""

import unittest
from unittest.mock import patch

from ...utils.sentiment import compute_vader_score
from ..fixtures.mock_data import TEST_TEXT_SAMPLES


class TestSentimentUtils(unittest.TestCase):
    """Test sentiment analysis utility functions."""

    def test_compute_vader_score_positive_text(self):
        """Test VADER score computation for positive text."""
        positive_text = "I love this amazing product! It's fantastic!"
        score = compute_vader_score(positive_text)

        # Positive text should have positive score
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, -1.0)

    def test_compute_vader_score_negative_text(self):
        """Test VADER score computation for negative text."""
        negative_text = "This is terrible and awful. I hate it!"
        score = compute_vader_score(negative_text)

        # Negative text should have negative score
        self.assertLess(score, 0)
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, -1.0)

    def test_compute_vader_score_neutral_text(self):
        """Test VADER score computation for neutral text."""
        neutral_text = "The product works as expected."
        score = compute_vader_score(neutral_text)

        # Neutral text should have score close to 0
        self.assertLessEqual(abs(score), 0.5)  # Allow some variation
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, -1.0)

    def test_compute_vader_score_empty_text(self):
        """Test VADER score computation for empty text."""
        score = compute_vader_score("")

        # Empty text should return 0
        self.assertEqual(score, 0.0)

    def test_compute_vader_score_whitespace_only(self):
        """Test VADER score computation for whitespace-only text."""
        score = compute_vader_score("   \n\t   ")

        # Whitespace-only should return 0
        self.assertEqual(score, 0.0)

    def test_compute_vader_score_special_characters(self):
        """Test VADER score with special characters."""
        special_text = "!@#$%^&*()_+{}[]|\\:;\"'<>?,./"
        score = compute_vader_score(special_text)

        # Should handle special characters gracefully
        self.assertIsInstance(score, float)
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, -1.0)

    def test_compute_vader_score_emoji_text(self):
        """Test VADER score with emoji-heavy text."""
        emoji_text = "😀😃😄😁😆😅😂🤣"
        score = compute_vader_score(emoji_text)

        # Should handle emojis
        self.assertIsInstance(score, float)
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, -1.0)

    def test_compute_vader_score_mixed_sentiment(self):
        """Test VADER score with mixed sentiment text."""
        mixed_text = "I love the design but hate the performance"
        score = compute_vader_score(mixed_text)

        # Mixed sentiment should be closer to neutral
        self.assertIsInstance(score, float)
        self.assertLessEqual(abs(score), 0.8)  # Not extremely positive or negative

    def test_compute_vader_score_very_long_text(self):
        """Test VADER score with very long text."""
        long_text = "This is a great product. " * 100  # 2500+ characters
        score = compute_vader_score(long_text)

        # Should handle long text
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)  # Should be positive

    def test_compute_vader_score_different_languages(self):
        """Test VADER score with non-English text."""
        # VADER is primarily designed for English
        spanish_text = "Me gusta mucho este producto"
        score = compute_vader_score(spanish_text)

        # Should still return a valid score
        self.assertIsInstance(score, float)
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, -1.0)

    def test_compute_vader_score_numbers_only(self):
        """Test VADER score with numbers only."""
        numbers_text = "123456789"
        score = compute_vader_score(numbers_text)

        # Numbers should be neutral
        self.assertEqual(score, 0.0)

    def test_compute_vader_score_consistency(self):
        """Test that VADER scores are consistent across calls."""
        text = "This is a consistently positive message!"

        score1 = compute_vader_score(text)
        score2 = compute_vader_score(text)
        score3 = compute_vader_score(text)

        # Scores should be identical for same input
        self.assertEqual(score1, score2)
        self.assertEqual(score2, score3)

    def test_compute_vader_score_with_test_samples(self):
        """Test VADER scores with predefined test samples."""
        # Test positive samples
        for text in TEST_TEXT_SAMPLES["positive"]:
            score = compute_vader_score(text)
            self.assertGreater(
                score, 0, f"Positive text should have positive score: {text}"
            )

        # Test negative samples
        for text in TEST_TEXT_SAMPLES["negative"]:
            score = compute_vader_score(text)
            self.assertLess(
                score, 0, f"Negative text should have negative score: {text}"
            )

        # Test neutral samples
        for text in TEST_TEXT_SAMPLES["neutral"]:
            score = compute_vader_score(text)
            self.assertLessEqual(
                abs(score), 0.31, f"Neutral text should have neutral score: {text}"
            )

    @patch("sentiment_analysis.utils.sentiment.vader")
    def test_compute_vader_score_with_mocked_vader(self, mock_vader):
        """Test compute_vader_score with mocked VADER analyzer."""
        # Setup mock
        mock_vader.polarity_scores.return_value = {"compound": 0.5}

        # Test
        score = compute_vader_score("test text")

        # Verify
        self.assertEqual(score, 0.5)
        mock_vader.polarity_scores.assert_called_once_with("test text")

    def test_compute_vader_score_type_validation(self):
        """Test that compute_vader_score validates input types."""
        # Test with None
        with self.assertRaises(TypeError):
            compute_vader_score(None)

    def test_compute_vader_score_unicode_handling(self):
        """Test VADER score with unicode characters."""
        unicode_text = "This is amazing! 🎉 ñoño café résumé"
        score = compute_vader_score(unicode_text)

        # Should handle unicode gracefully
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)  # Should be positive due to "amazing!"

    def test_compute_vader_score_case_sensitivity(self):
        """Test if VADER is case sensitive."""
        text_lower = "this is amazing!"
        text_upper = "THIS IS AMAZING!"
        text_mixed = "This Is Amazing!"

        score_lower = compute_vader_score(text_lower)
        score_upper = compute_vader_score(text_upper)
        score_mixed = compute_vader_score(text_mixed)

        # All should be positive
        self.assertGreater(score_lower, 0)
        self.assertGreater(score_upper, 0)
        self.assertGreater(score_mixed, 0)

        # Upper case might have higher intensity in VADER
        self.assertGreaterEqual(score_upper, score_lower)


if __name__ == "__main__":
    unittest.main()
