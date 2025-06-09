#!/usr/bin/env python3
"""
Performance analysis script for the XSS Validator application.

This script runs a series of performance tests and analyzes the results
to identify potential bottlenecks in the application.
"""

import asyncio
import time
import statistics
import argparse
import sys
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import numpy as np

import httpx

# Test website URL
TEST_WEBSITE_URL = "http://hackme.ifflaender-family.de:4010/"

# XSS payload that should trigger a popup
XSS_PAYLOAD = "<Script>success()</Script>"

# URL with XSS payload
XSS_URL = "http://hackme.ifflaender-family.de:4010/search?q=%3CScript%3Esuccess%28%29%3C%2FScript%3E"

# API base URL
API_BASE_URL = "http://localhost:8000"


async def measure_response_time(client: httpx.AsyncClient, endpoint: str, params: Dict[str, str]) -> float:
    """Measure the response time for a single request."""
    start_time = time.time()
    try:
        response = await client.get(f"{API_BASE_URL}{endpoint}", params=params, timeout=60.0)
        response.raise_for_status()
    except Exception as e:
        print(f"Error during request: {e}")
        return float('inf')  # Return infinity for failed requests
    end_time = time.time()
    return end_time - start_time


async def run_concurrent_requests(
    endpoint: str, params_list: List[Dict[str, str]], concurrency: int
) -> List[float]:
    """Run multiple requests concurrently and measure response times."""
    async with httpx.AsyncClient() as client:
        # Create batches of requests to control concurrency
        results = []
        for i in range(0, len(params_list), concurrency):
            batch = params_list[i:i+concurrency]
            batch_tasks = [measure_response_time(client, endpoint, params) for params in batch]
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)
            
            # Print progress
            print(f"Completed {min(i+concurrency, len(params_list))}/{len(params_list)} requests")
            
        return results


def analyze_results(response_times: List[float], title: str) -> Dict[str, float]:
    """Analyze response times and print statistics."""
    # Filter out failed requests (infinity)
    valid_times = [t for t in response_times if t != float('inf')]
    failed_count = len(response_times) - len(valid_times)
    
    if not valid_times:
        print(f"All {len(response_times)} requests failed!")
        return {
            "min": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "p95": 0,
            "p99": 0,
            "std_dev": 0,
            "failure_rate": 100.0
        }
    
    # Calculate statistics
    min_time = min(valid_times)
    max_time = max(valid_times)
    mean_time = statistics.mean(valid_times)
    median_time = statistics.median(valid_times)
    p95 = np.percentile(valid_times, 95) if len(valid_times) >= 20 else max_time
    p99 = np.percentile(valid_times, 99) if len(valid_times) >= 100 else max_time
    std_dev = statistics.stdev(valid_times) if len(valid_times) > 1 else 0
    failure_rate = (failed_count / len(response_times)) * 100
    
    # Print results
    print(f"\n=== {title} ===")
    print(f"Total requests: {len(response_times)}")
    print(f"Successful requests: {len(valid_times)}")
    print(f"Failed requests: {failed_count} ({failure_rate:.2f}%)")
    print(f"Min response time: {min_time:.4f} seconds")
    print(f"Max response time: {max_time:.4f} seconds")
    print(f"Mean response time: {mean_time:.4f} seconds")
    print(f"Median response time: {median_time:.4f} seconds")
    print(f"95th percentile: {p95:.4f} seconds")
    print(f"99th percentile: {p99:.4f} seconds")
    print(f"Standard deviation: {std_dev:.4f} seconds")
    
    return {
        "min": min_time,
        "max": max_time,
        "mean": mean_time,
        "median": median_time,
        "p95": p95,
        "p99": p99,
        "std_dev": std_dev,
        "failure_rate": failure_rate
    }


def plot_results(results: Dict[str, Dict[str, float]], output_file: str = None):
    """Generate plots for the performance results."""
    try:
        # Create figure with multiple subplots
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('XSS Validator Performance Analysis', fontsize=16)
        
        # Extract test names and metrics
        test_names = list(results.keys())
        means = [results[test]["mean"] for test in test_names]
        medians = [results[test]["median"] for test in test_names]
        p95s = [results[test]["p95"] for test in test_names]
        failure_rates = [results[test]["failure_rate"] for test in test_names]
        
        # Plot mean and median response times
        x = np.arange(len(test_names))
        width = 0.35
        axs[0, 0].bar(x - width/2, means, width, label='Mean')
        axs[0, 0].bar(x + width/2, medians, width, label='Median')
        axs[0, 0].set_ylabel('Time (seconds)')
        axs[0, 0].set_title('Mean and Median Response Times')
        axs[0, 0].set_xticks(x)
        axs[0, 0].set_xticklabels(test_names)
        axs[0, 0].legend()
        
        # Plot 95th percentile
        axs[0, 1].bar(test_names, p95s)
        axs[0, 1].set_ylabel('Time (seconds)')
        axs[0, 1].set_title('95th Percentile Response Times')
        
        # Plot failure rates
        axs[1, 0].bar(test_names, failure_rates)
        axs[1, 0].set_ylabel('Failure Rate (%)')
        axs[1, 0].set_title('Request Failure Rates')
        
        # Plot min/max/mean/median for each test
        for i, test in enumerate(test_names):
            data = [
                results[test]["min"],
                results[test]["mean"],
                results[test]["median"],
                results[test]["p95"],
                results[test]["max"]
            ]
            labels = ['Min', 'Mean', 'Median', '95th', 'Max']
            axs[1, 1].boxplot([data], positions=[i], labels=[test])
        
        axs[1, 1].set_ylabel('Time (seconds)')
        axs[1, 1].set_title('Response Time Distribution')
        
        plt.tight_layout()
        
        # Save or show the plot
        if output_file:
            plt.savefig(output_file)
            print(f"Plot saved to {output_file}")
        else:
            plt.show()
            
    except Exception as e:
        print(f"Error generating plots: {e}")
        print("Matplotlib may not be installed or configured correctly.")
        print("Install it with: pip install matplotlib")


async def test_input_endpoint(num_requests: int, concurrency: int) -> List[float]:
    """Test the performance of the input endpoint."""
    print(f"\nTesting input endpoint with {num_requests} requests (concurrency: {concurrency})...")
    
    # Create a list of parameters for each request
    params_list = []
    for i in range(num_requests):
        # Alternate between XSS and non-XSS payloads
        payload = XSS_PAYLOAD if i % 2 == 0 else "No XSS here"
        params_list.append({"url": TEST_WEBSITE_URL, "payload": payload})
    
    # Run the requests and measure response times
    return await run_concurrent_requests("/check/input", params_list, concurrency)


async def test_url_endpoint(num_requests: int, concurrency: int) -> List[float]:
    """Test the performance of the URL endpoint."""
    print(f"\nTesting URL endpoint with {num_requests} requests (concurrency: {concurrency})...")
    
    # Create a list of parameters for each request
    params_list = []
    for i in range(num_requests):
        # Alternate between XSS and non-XSS URLs
        url = XSS_URL if i % 2 == 0 else f"{TEST_WEBSITE_URL}search?q=No+XSS+here"
        params_list.append({"url": url})
    
    # Run the requests and measure response times
    return await run_concurrent_requests("/check/url", params_list, concurrency)


async def test_mixed_endpoints(num_requests: int, concurrency: int) -> Tuple[List[float], List[float]]:
    """Test the performance of both endpoints simultaneously."""
    print(f"\nTesting both endpoints with {num_requests} requests each (concurrency: {concurrency})...")
    
    # Create parameter lists for each endpoint
    input_params_list = []
    url_params_list = []
    
    for i in range(num_requests):
        # Alternate between XSS and non-XSS payloads/URLs
        payload = XSS_PAYLOAD if i % 2 == 0 else "No XSS here"
        url = XSS_URL if i % 2 == 0 else f"{TEST_WEBSITE_URL}search?q=No+XSS+here"
        
        input_params_list.append({"url": TEST_WEBSITE_URL, "payload": payload})
        url_params_list.append({"url": url})
    
    # Run the requests for both endpoints concurrently
    input_task = run_concurrent_requests("/check/input", input_params_list, concurrency // 2)
    url_task = run_concurrent_requests("/check/url", url_params_list, concurrency // 2)
    
    input_results, url_results = await asyncio.gather(input_task, url_task)
    
    return input_results, url_results


async def main():
    """Run the performance tests and analyze the results."""
    parser = argparse.ArgumentParser(description="Performance analysis for XSS Validator")
    parser.add_argument("--requests", type=int, default=10, help="Number of requests per test")
    parser.add_argument("--concurrency", type=int, default=5, help="Number of concurrent requests")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000", help="Base URL for the API")
    parser.add_argument("--plot", action="store_true", help="Generate plots of the results")
    parser.add_argument("--output", type=str, help="Output file for the plot (requires --plot)")
    
    args = parser.parse_args()
    
    global API_BASE_URL
    API_BASE_URL = args.api_url
    
    print("=== XSS Validator Performance Analysis ===")
    print(f"API URL: {API_BASE_URL}")
    print(f"Requests per test: {args.requests}")
    print(f"Concurrency level: {args.concurrency}")
    
    try:
        # Check if the API is available
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{API_BASE_URL}/", timeout=5.0)
                response.raise_for_status()
                print("✅ API is available")
            except Exception as e:
                print(f"❌ API is not available: {e}")
                print("Make sure the XSS Validator API is running at the specified URL.")
                sys.exit(1)
        
        # Run the performance tests
        input_times = await test_input_endpoint(args.requests, args.concurrency)
        url_times = await test_url_endpoint(args.requests, args.concurrency)
        mixed_input_times, mixed_url_times = await test_mixed_endpoints(args.requests, args.concurrency)
        
        # Analyze the results
        results = {}
        results["Input Endpoint"] = analyze_results(input_times, "Input Endpoint Performance")
        results["URL Endpoint"] = analyze_results(url_times, "URL Endpoint Performance")
        results["Mixed (Input)"] = analyze_results(mixed_input_times, "Mixed Endpoints - Input Performance")
        results["Mixed (URL)"] = analyze_results(mixed_url_times, "Mixed Endpoints - URL Performance")
        
        # Print overall summary
        print("\n=== Performance Summary ===")
        print(f"{'Test':<20} {'Mean (s)':<10} {'Median (s)':<10} {'95th (s)':<10} {'Failure %':<10}")
        print("-" * 60)
        for test, stats in results.items():
            print(f"{test:<20} {stats['mean']:<10.4f} {stats['median']:<10.4f} {stats['p95']:<10.4f} {stats['failure_rate']:<10.2f}")
        
        # Identify bottlenecks
        print("\n=== Potential Bottlenecks ===")
        
        # Check for high failure rates
        high_failure_tests = [test for test, stats in results.items() if stats['failure_rate'] > 5]
        if high_failure_tests:
            print(f"❌ High failure rates in: {', '.join(high_failure_tests)}")
            print("   This may indicate resource constraints or timeout issues.")
        
        # Check for slow response times
        slow_tests = [test for test, stats in results.items() if stats['median'] > 5]
        if slow_tests:
            print(f"❌ Slow response times in: {', '.join(slow_tests)}")
            print("   This may indicate performance issues in the browser automation.")
        
        # Check for high variability
        variable_tests = [test for test, stats in results.items() if stats['std_dev'] > stats['mean'] / 2]
        if variable_tests:
            print(f"❌ High variability in: {', '.join(variable_tests)}")
            print("   This may indicate inconsistent performance or resource contention.")
        
        # Check for concurrency issues
        if results["Mixed (Input)"]["median"] > results["Input Endpoint"]["median"] * 1.5:
            print("❌ Performance degrades significantly when running both endpoints concurrently.")
            print("   This may indicate resource contention or concurrency issues.")
        
        if not high_failure_tests and not slow_tests and not variable_tests:
            print("✅ No significant bottlenecks detected!")
        
        # Generate plots if requested
        if args.plot:
            plot_results(results, args.output)
        
    except Exception as e:
        print(f"Error during performance testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())