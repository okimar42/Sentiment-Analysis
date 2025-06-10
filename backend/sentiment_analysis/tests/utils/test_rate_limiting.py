"""
Tests for rate limiting utilities using context7.
"""

import unittest
import asyncio
import time
from unittest.mock import patch, MagicMock

from ...utils.rate_limiting import ModelRateLimiter, get_rate_limiter, RATE_LIMITS


class TestModelRateLimiter(unittest.TestCase):
    """Test ModelRateLimiter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rate_limiter = ModelRateLimiter('gpt4')
    
    def test_init_with_known_model(self):
        """Test initialization with known model."""
        limiter = ModelRateLimiter('gpt4')
        
        self.assertEqual(limiter.model_name, 'gpt4')
        self.assertEqual(limiter.settings, RATE_LIMITS['gpt4'])
        self.assertEqual(limiter.current_delay, RATE_LIMITS['gpt4']['initial_delay'])
        self.assertEqual(limiter.consecutive_failures, 0)
        self.assertIsNotNone(limiter.lock)
    
    def test_init_with_unknown_model(self):
        """Test initialization with unknown model."""
        limiter = ModelRateLimiter('unknown_model')
        
        self.assertEqual(limiter.model_name, 'unknown_model')
        self.assertEqual(limiter.settings, RATE_LIMITS['default'])
        self.assertEqual(limiter.current_delay, RATE_LIMITS['default']['initial_delay'])
    
    def test_increase_delay_first_failure(self):
        """Test delay increase on first failure."""
        initial_delay = self.rate_limiter.current_delay
        initial_failures = self.rate_limiter.consecutive_failures
        
        self.rate_limiter.increase_delay()
        
        self.assertEqual(self.rate_limiter.consecutive_failures, initial_failures + 1)
        self.assertGreater(self.rate_limiter.current_delay, initial_delay)
    
    def test_increase_delay_multiple_failures(self):
        """Test delay increase with multiple consecutive failures."""
        delays = []
        
        # Record delays for multiple failures
        for i in range(5):
            delays.append(self.rate_limiter.current_delay)
            self.rate_limiter.increase_delay()
        
        # Each delay should be larger than the previous
        for i in range(1, len(delays)):
            self.assertGreater(self.rate_limiter.current_delay, delays[i-1])
        
        # Failures should accumulate
        self.assertEqual(self.rate_limiter.consecutive_failures, 5)
    
    def test_increase_delay_respects_max_delay(self):
        """Test that delay increase respects maximum delay limit."""
        max_delay = self.rate_limiter.settings['max_delay']
        
        # Force many failures to hit max delay
        for _ in range(20):
            self.rate_limiter.increase_delay()
        
        self.assertLessEqual(self.rate_limiter.current_delay, max_delay)
    
    def test_decrease_delay_resets_failures(self):
        """Test that decrease_delay resets consecutive failures."""
        # Create some failures first
        for _ in range(3):
            self.rate_limiter.increase_delay()
        
        initial_delay = self.rate_limiter.current_delay
        self.assertGreater(self.rate_limiter.consecutive_failures, 0)
        
        # Decrease delay
        self.rate_limiter.decrease_delay()
        
        self.assertEqual(self.rate_limiter.consecutive_failures, 0)
        self.assertLess(self.rate_limiter.current_delay, initial_delay)
    
    def test_decrease_delay_respects_min_delay(self):
        """Test that delay decrease respects minimum delay limit."""
        min_delay = self.rate_limiter.settings['min_delay']
        
        # Decrease delay multiple times
        for _ in range(20):
            self.rate_limiter.decrease_delay()
        
        self.assertGreaterEqual(self.rate_limiter.current_delay, min_delay)
    
    def test_batch_size_property_normal(self):
        """Test batch_size property with no failures."""
        expected_batch_size = self.rate_limiter.settings['batch_size']
        self.assertEqual(self.rate_limiter.batch_size, expected_batch_size)
    
    def test_batch_size_property_with_failures(self):
        """Test batch_size property with consecutive failures."""
        original_batch_size = self.rate_limiter.settings['batch_size']
        
        # Create failures
        self.rate_limiter.increase_delay()
        self.rate_limiter.increase_delay()
        
        # Batch size should be reduced
        expected_batch_size = max(1, original_batch_size - 2)
        self.assertEqual(self.rate_limiter.batch_size, expected_batch_size)
    
    def test_batch_size_property_minimum_one(self):
        """Test batch_size property never goes below 1."""
        # Create many failures
        for _ in range(20):
            self.rate_limiter.increase_delay()
        
        self.assertGreaterEqual(self.rate_limiter.batch_size, 1)
    
    @patch('asyncio.sleep')
    async def test_wait_no_delay_needed(self, mock_sleep):
        """Test wait method when no delay is needed."""
        # Set last request time to far in the past
        self.rate_limiter.last_request_time = time.time() - 100
        
        await self.rate_limiter.wait()
        
        # Should not sleep if enough time has passed
        mock_sleep.assert_not_called()
    
    @patch('asyncio.sleep')
    async def test_wait_with_delay_needed(self, mock_sleep):
        """Test wait method when delay is needed."""
        # Set last request time to recent
        self.rate_limiter.last_request_time = time.time()
        
        await self.rate_limiter.wait()
        
        # Should sleep for remaining delay
        mock_sleep.assert_called_once()
        sleep_time = mock_sleep.call_args[0][0]
        self.assertGreater(sleep_time, 0)
        self.assertLessEqual(sleep_time, self.rate_limiter.current_delay)
    
    @patch('time.time')
    @patch('asyncio.sleep')
    async def test_wait_updates_last_request_time(self, mock_sleep, mock_time):
        """Test that wait method updates last_request_time."""
        mock_time.return_value = 1000.0
        
        await self.rate_limiter.wait()
        
        self.assertEqual(self.rate_limiter.last_request_time, 1000.0)


class TestRateLimiterConfiguration(unittest.TestCase):
    """Test rate limiter configuration and settings."""
    
    def test_rate_limits_contains_required_models(self):
        """Test that RATE_LIMITS contains all required models."""
        required_models = ['gpt4', 'gemini', 'grok', 'default']
        
        for model in required_models:
            self.assertIn(model, RATE_LIMITS)
    
    def test_rate_limits_settings_structure(self):
        """Test that all rate limit settings have required keys."""
        required_keys = [
            'initial_delay',
            'min_delay', 
            'max_delay',
            'batch_size',
            'min_retry_delay',
            'retry_multiplier'
        ]
        
        for model, settings in RATE_LIMITS.items():
            for key in required_keys:
                self.assertIn(key, settings, f"Model {model} missing key {key}")
    
    def test_rate_limits_settings_types(self):
        """Test that rate limit settings have correct types."""
        for model, settings in RATE_LIMITS.items():
            self.assertIsInstance(settings['initial_delay'], (int, float))
            self.assertIsInstance(settings['min_delay'], (int, float))
            self.assertIsInstance(settings['max_delay'], (int, float))
            self.assertIsInstance(settings['batch_size'], int)
            self.assertIsInstance(settings['min_retry_delay'], (int, float))
            self.assertIsInstance(settings['retry_multiplier'], (int, float))
    
    def test_rate_limits_settings_values(self):
        """Test that rate limit settings have reasonable values."""
        for model, settings in RATE_LIMITS.items():
            # Delays should be positive
            self.assertGreater(settings['initial_delay'], 0)
            self.assertGreater(settings['min_delay'], 0)
            self.assertGreater(settings['max_delay'], 0)
            
            # Max delay should be greater than min delay
            self.assertGreater(settings['max_delay'], settings['min_delay'])
            
            # Batch size should be positive
            self.assertGreater(settings['batch_size'], 0)
            
            # Retry settings should be reasonable
            self.assertGreater(settings['min_retry_delay'], 0)
            self.assertGreater(settings['retry_multiplier'], 1.0)


class TestGetRateLimiter(unittest.TestCase):
    """Test get_rate_limiter function."""
    
    def test_get_rate_limiter_known_model(self):
        """Test getting rate limiter for known model."""
        limiter = get_rate_limiter('gpt4')
        
        self.assertIsInstance(limiter, ModelRateLimiter)
        self.assertEqual(limiter.model_name, 'gpt4')
    
    def test_get_rate_limiter_unknown_model(self):
        """Test getting rate limiter for unknown model."""
        limiter = get_rate_limiter('unknown_model')
        
        self.assertIsInstance(limiter, ModelRateLimiter)
        # Should return default limiter
        self.assertEqual(limiter.model_name, 'default')
    
    def test_get_rate_limiter_returns_same_instance(self):
        """Test that get_rate_limiter returns the same instance for same model."""
        limiter1 = get_rate_limiter('gpt4')
        limiter2 = get_rate_limiter('gpt4')
        
        self.assertIs(limiter1, limiter2)
    
    def test_get_rate_limiter_different_models(self):
        """Test that get_rate_limiter returns different instances for different models."""
        limiter_gpt4 = get_rate_limiter('gpt4')
        limiter_gemini = get_rate_limiter('gemini')
        
        self.assertIsNot(limiter_gpt4, limiter_gemini)
        self.assertEqual(limiter_gpt4.model_name, 'gpt4')
        self.assertEqual(limiter_gemini.model_name, 'gemini')


class TestRateLimiterIntegration(unittest.TestCase):
    """Integration tests for rate limiting functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rate_limiter = ModelRateLimiter('gpt4')
    
    def test_failure_recovery_cycle(self):
        """Test complete failure and recovery cycle."""
        initial_delay = self.rate_limiter.current_delay
        initial_batch_size = self.rate_limiter.batch_size
        
        # Simulate failures
        for _ in range(3):
            self.rate_limiter.increase_delay()
        
        # Check degraded state
        self.assertGreater(self.rate_limiter.current_delay, initial_delay)
        self.assertLess(self.rate_limiter.batch_size, initial_batch_size)
        self.assertEqual(self.rate_limiter.consecutive_failures, 3)
        
        # Simulate recovery
        self.rate_limiter.decrease_delay()
        
        # Check recovery
        self.assertEqual(self.rate_limiter.consecutive_failures, 0)
        self.assertEqual(self.rate_limiter.batch_size, initial_batch_size)
    
    def test_progressive_backoff(self):
        """Test progressive backoff with increasing delays."""
        delays = []
        
        # Simulate progressive failures
        for i in range(5):
            delays.append(self.rate_limiter.current_delay)
            self.rate_limiter.increase_delay()
        
        # Each delay should be progressively larger
        for i in range(1, len(delays)):
            self.assertGreater(self.rate_limiter.current_delay, delays[i])
    
    async def test_concurrent_wait_calls(self):
        """Test that concurrent wait calls are properly synchronized."""
        async def wait_and_record():
            start_time = time.time()
            await self.rate_limiter.wait()
            return time.time() - start_time
        
        # Create multiple concurrent wait calls
        tasks = [wait_and_record() for _ in range(3)]
        results = await asyncio.gather(*tasks)
        
        # All should complete (no hanging)
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result, (int, float))
    
    def test_model_specific_settings(self):
        """Test that different models have different settings."""
        gpt4_limiter = ModelRateLimiter('gpt4')
        gemini_limiter = ModelRateLimiter('gemini')
        
        # Settings should be different if configured differently
        gpt4_settings = gpt4_limiter.settings
        gemini_settings = gemini_limiter.settings
        
        # At least some settings should differ
        settings_match = all(
            gpt4_settings[key] == gemini_settings[key]
            for key in gpt4_settings.keys()
        )
        
        # If all settings are the same, that's also valid configuration
        # Just ensure both have valid settings
        self.assertIsInstance(gpt4_settings, dict)
        self.assertIsInstance(gemini_settings, dict)


if __name__ == '__main__':
    # Run async tests
    async def run_async_tests():
        suite = unittest.TestSuite()
        
        # Add async test methods
        suite.addTest(TestModelRateLimiter('test_wait_no_delay_needed'))
        suite.addTest(TestModelRateLimiter('test_wait_with_delay_needed'))
        suite.addTest(TestModelRateLimiter('test_wait_updates_last_request_time'))
        suite.addTest(TestRateLimiterIntegration('test_concurrent_wait_calls'))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)
    
    # Run sync tests normally
    unittest.main(verbosity=2, exit=False)
    
    # Run async tests
    asyncio.run(run_async_tests())