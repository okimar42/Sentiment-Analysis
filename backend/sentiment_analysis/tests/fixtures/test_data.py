"""
Test data creation utilities using context7 for comprehensive testing.
"""

from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from ...models import SentimentAnalysis, SentimentResult
from .factories import (
    UserFactory,
    SentimentAnalysisFactory,
    SentimentResultFactory,
    create_mixed_sentiment_results
)


def create_test_user(username: Optional[str] = None, **kwargs) -> User:
    """
    Create a test user for authentication testing.
    
    Args:
        username: Optional username, will be generated if not provided
        **kwargs: Additional user attributes
        
    Returns:
        User: Created user instance
    """
    if username:
        kwargs['username'] = username
    return UserFactory(**kwargs)


def create_test_analysis(
    query: str = "test query",
    source: str = "reddit",
    model: str = "vader",
    status: str = "pending",
    **kwargs
) -> SentimentAnalysis:
    """
    Create a test sentiment analysis.
    
    Args:
        query: Search query for the analysis
        source: Data source (reddit/twitter)
        model: Analysis model (vader/gemma/gpt4)
        status: Analysis status
        **kwargs: Additional analysis attributes
        
    Returns:
        SentimentAnalysis: Created analysis instance
    """
    return SentimentAnalysisFactory(
        query=query,
        source=source,
        model=model,
        status=status,
        **kwargs
    )


def create_test_results(
    analysis: SentimentAnalysis,
    count: int = 10,
    sentiment_mix: bool = False,
    **kwargs
) -> List[SentimentResult]:
    """
    Create test sentiment results for an analysis.
    
    Args:
        analysis: Analysis to associate results with
        count: Number of results to create
        sentiment_mix: If True, create mix of positive/negative/neutral
        **kwargs: Additional result attributes
        
    Returns:
        List[SentimentResult]: Created result instances
    """
    if sentiment_mix:
        # Create balanced mix of sentiments
        num_each = count // 3
        return create_mixed_sentiment_results(analysis, num_each)
    else:
        # Create uniform results
        return SentimentResultFactory.create_batch(
            count,
            analysis=analysis,
            **kwargs
        )


def create_complete_test_scenario(
    num_analyses: int = 3,
    results_per_analysis: int = 15
) -> Dict[str, Any]:
    """
    Create a complete test scenario with multiple analyses and results.
    
    Args:
        num_analyses: Number of analyses to create
        results_per_analysis: Number of results per analysis
        
    Returns:
        Dict containing created test data
    """
    with transaction.atomic():
        # Create test user
        user = create_test_user(username="test_scenario_user")
        
        # Create analyses with different configurations
        analyses = []
        all_results = []
        
        for i in range(num_analyses):
            # Vary the analysis configurations
            sources = ['reddit', 'twitter', 'reddit']
            models = ['vader', 'gemma', 'gpt4']
            statuses = ['completed', 'completed', 'processing']
            
            analysis = create_test_analysis(
                query=f"test scenario {i+1}",
                source=sources[i % len(sources)],
                model=models[i % len(models)],
                status=statuses[i % len(statuses)]
            )
            analyses.append(analysis)
            
            # Create results with sentiment mix
            results = create_test_results(
                analysis,
                count=results_per_analysis,
                sentiment_mix=True
            )
            all_results.extend(results)
        
        return {
            'user': user,
            'analyses': analyses,
            'results': all_results,
            'total_analyses': len(analyses),
            'total_results': len(all_results)
        }


def create_time_series_test_data(
    analysis: SentimentAnalysis,
    days: int = 7,
    posts_per_day: int = 10
) -> List[SentimentResult]:
    """
    Create test data spread across time for time-series testing.
    
    Args:
        analysis: Analysis to associate results with
        days: Number of days to spread data across
        posts_per_day: Number of posts per day
        
    Returns:
        List[SentimentResult]: Created results with varied post dates
    """
    results = []
    base_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    for day in range(days):
        post_date = base_date + timedelta(days=day)
        
        # Create posts for this day with varied times
        for post in range(posts_per_day):
            # Spread posts throughout the day
            post_time = post_date + timedelta(
                hours=post * (24 / posts_per_day)
            )
            
            result = SentimentResultFactory(
                analysis=analysis,
                post_date=post_time
            )
            results.append(result)
    
    return results


def create_edge_case_test_data() -> Dict[str, Any]:
    """
    Create edge case test data for thorough testing.
    
    Returns:
        Dict containing various edge case scenarios
    """
    # Analysis with no results
    empty_analysis = create_test_analysis(
        query="empty analysis",
        status="completed"
    )
    
    # Analysis with single result
    single_result_analysis = create_test_analysis(
        query="single result",
        status="completed"
    )
    single_result = SentimentResultFactory(analysis=single_result_analysis)
    
    # Analysis with extreme sentiment scores
    extreme_analysis = create_test_analysis(
        query="extreme scores",
        status="completed"
    )
    extreme_results = [
        SentimentResultFactory(
            analysis=extreme_analysis,
            score=1.0,  # Maximum positive
            perceived_iq=150,
            bot_probability=0.0
        ),
        SentimentResultFactory(
            analysis=extreme_analysis,
            score=-1.0,  # Maximum negative
            perceived_iq=60,
            bot_probability=1.0
        )
    ]
    
    # Failed analysis
    failed_analysis = create_test_analysis(
        query="failed analysis",
        status="failed"
    )
    
    # Analysis with very long content
    long_content_analysis = create_test_analysis(
        query="long content test",
        status="completed"
    )
    long_content_result = SentimentResultFactory(
        analysis=long_content_analysis,
        content="This is a very long piece of content. " * 100  # 500+ chars
    )
    
    return {
        'empty_analysis': empty_analysis,
        'single_result_analysis': single_result_analysis,
        'single_result': single_result,
        'extreme_analysis': extreme_analysis,
        'extreme_results': extreme_results,
        'failed_analysis': failed_analysis,
        'long_content_analysis': long_content_analysis,
        'long_content_result': long_content_result
    }


def create_performance_test_data(
    num_analyses: int = 10,
    results_per_analysis: int = 100
) -> Dict[str, Any]:
    """
    Create large dataset for performance testing.
    
    Args:
        num_analyses: Number of analyses to create
        results_per_analysis: Number of results per analysis
        
    Returns:
        Dict containing performance test data
    """
    with transaction.atomic():
        analyses = []
        total_results = 0
        
        for i in range(num_analyses):
            analysis = create_test_analysis(
                query=f"performance test {i+1}",
                status="completed"
            )
            analyses.append(analysis)
            
            # Create results in batches for efficiency
            batch_size = 50
            for batch_start in range(0, results_per_analysis, batch_size):
                batch_end = min(batch_start + batch_size, results_per_analysis)
                batch_count = batch_end - batch_start
                
                SentimentResultFactory.create_batch(
                    batch_count,
                    analysis=analysis
                )
                total_results += batch_count
        
        return {
            'analyses': analyses,
            'total_analyses': len(analyses),
            'total_results': total_results,
            'results_per_analysis': results_per_analysis
        }


def create_api_test_data() -> Dict[str, Any]:
    """
    Create test data specifically for API endpoint testing.
    
    Returns:
        Dict containing API test data
    """
    # Create user for authenticated requests
    api_user = create_test_user(username="api_test_user")
    
    # Create analyses in different states
    pending_analysis = create_test_analysis(
        query="pending API test",
        status="pending"
    )
    
    processing_analysis = create_test_analysis(
        query="processing API test", 
        status="processing"
    )
    
    completed_analysis = create_test_analysis(
        query="completed API test",
        status="completed"
    )
    
    # Add results to completed analysis
    api_results = create_test_results(
        completed_analysis,
        count=20,
        sentiment_mix=True
    )
    
    failed_analysis = create_test_analysis(
        query="failed API test",
        status="failed"
    )
    
    return {
        'user': api_user,
        'pending_analysis': pending_analysis,
        'processing_analysis': processing_analysis,
        'completed_analysis': completed_analysis,
        'failed_analysis': failed_analysis,
        'api_results': api_results
    }


def cleanup_test_data():
    """
    Clean up all test data (for use in test teardown).
    """
    # Delete in reverse order of dependencies
    SentimentResult.objects.all().delete()
    SentimentAnalysis.objects.all().delete()
    User.objects.filter(username__startswith='test').delete()