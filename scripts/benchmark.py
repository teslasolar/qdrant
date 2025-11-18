#!/usr/bin/env python3
"""
Comprehensive Performance Benchmarking for Medical Imaging System
Tests embedding generation, search speed, and throughput
"""

import time
import statistics
import sys
import os
import requests
import base64
import io
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'os', 'backend'))

def create_test_image(size=(224, 224)):
    """Create a test medical image"""
    image = np.random.randint(100, 200, (*size, 3), dtype=np.uint8)

    # Add a circular "abnormality"
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = 30
    for x in range(size[0]):
        for y in range(size[1]):
            if (x - center_x)**2 + (y - center_y)**2 < radius**2:
                image[x, y] = [255, 255, 255]

    return image


def image_to_base64(image_array):
    """Convert numpy array to base64"""
    image = Image.fromarray(image_array.astype('uint8'))
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


class Benchmarks:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.results = {}

    def check_api_health(self):
        """Check if API is available"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API is healthy")
                print(f"   Model: {data.get('image_model', 'unknown')}")
                print(f"   GPU: {data.get('gpu_available', False)}")
                return True
            return False
        except Exception as e:
            print(f"❌ API health check failed: {e}")
            return False

    def benchmark_embedding_generation(self, num_images=100):
        """Benchmark embedding generation speed"""
        print(f"\n{'='*60}")
        print(f"📊 Benchmark: Embedding Generation ({num_images} images)")
        print(f"{'='*60}")

        from api import generate_image_embedding, load_image_model, IMAGE_MODEL_TYPE

        # Load model
        load_image_model()
        print(f"Model loaded: {IMAGE_MODEL_TYPE}")

        # Warm up
        test_image = create_test_image()
        generate_image_embedding(test_image)

        # Benchmark
        times = []
        for i in range(num_images):
            test_image = create_test_image()

            start = time.time()
            embedding = generate_image_embedding(test_image)
            elapsed = (time.time() - start) * 1000  # milliseconds

            times.append(elapsed)

            if (i + 1) % 10 == 0:
                print(f"   Processed {i+1}/{num_images} images...")

        # Results
        results = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'throughput': 1000 / statistics.mean(times)  # images/sec
        }

        print(f"\n📈 Results:")
        print(f"   Mean:       {results['mean']:.2f} ms/image")
        print(f"   Median:     {results['median']:.2f} ms/image")
        print(f"   Min:        {results['min']:.2f} ms/image")
        print(f"   Max:        {results['max']:.2f} ms/image")
        print(f"   Std Dev:    {results['stdev']:.2f} ms")
        print(f"   Throughput: {results['throughput']:.2f} images/sec")

        self.results['embedding_generation'] = results
        return results

    def benchmark_api_upload(self, num_uploads=50):
        """Benchmark API upload endpoint"""
        print(f"\n{'='*60}")
        print(f"📊 Benchmark: API Upload ({num_uploads} images)")
        print(f"{'='*60}")

        times = []
        for i in range(num_uploads):
            # Create test image
            test_image = create_test_image()
            image_base64 = image_to_base64(test_image)

            # Prepare payload
            data = {
                'patient_id': f'BENCH-{i:04d}',
                'body_part': 'CHEST',
                'modality': 'XRAY',
                'diagnosis': 'Test Case'
            }

            # Create file-like object
            image_bytes = base64.b64decode(image_base64)
            files = {'file': ('test.png', io.BytesIO(image_bytes), 'image/png')}

            # Upload
            start = time.time()
            try:
                response = requests.post(
                    f"{self.api_url}/medical/upload",
                    files=files,
                    data=data,
                    timeout=30
                )
                elapsed = (time.time() - start) * 1000

                if response.status_code == 200:
                    times.append(elapsed)
                else:
                    print(f"   ⚠️  Upload {i+1} failed: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️  Upload {i+1} error: {e}")

            if (i + 1) % 10 == 0:
                print(f"   Uploaded {i+1}/{num_uploads} images...")

        # Results
        if times:
            results = {
                'mean': statistics.mean(times),
                'median': statistics.median(times),
                'min': min(times),
                'max': max(times),
                'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                'throughput': 1000 / statistics.mean(times),
                'success_rate': len(times) / num_uploads * 100
            }

            print(f"\n📈 Results:")
            print(f"   Mean:         {results['mean']:.2f} ms/upload")
            print(f"   Median:       {results['median']:.2f} ms/upload")
            print(f"   Min:          {results['min']:.2f} ms/upload")
            print(f"   Max:          {results['max']:.2f} ms/upload")
            print(f"   Std Dev:      {results['stdev']:.2f} ms")
            print(f"   Throughput:   {results['throughput']:.2f} uploads/sec")
            print(f"   Success Rate: {results['success_rate']:.1f}%")

            self.results['api_upload'] = results
            return results
        else:
            print("❌ No successful uploads")
            return None

    def benchmark_search_speed(self, num_searches=50):
        """Benchmark search endpoint speed"""
        print(f"\n{'='*60}")
        print(f"📊 Benchmark: Search Speed ({num_searches} searches)")
        print(f"{'='*60}")

        # Get collection stats
        try:
            stats_response = requests.get(f"{self.api_url}/medical/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()
                total_images = stats.get('total_images', 0)
                print(f"   Database size: {total_images} images")
            else:
                print("   ⚠️  Could not get database stats")
        except Exception as e:
            print(f"   ⚠️  Stats error: {e}")

        times = []
        for i in range(num_searches):
            # Create test image
            test_image = create_test_image()
            image_base64 = image_to_base64(test_image)

            # Search
            start = time.time()
            try:
                response = requests.post(
                    f"{self.api_url}/medical/search",
                    json={
                        'image_base64': image_base64,
                        'limit': 5
                    },
                    timeout=30
                )
                elapsed = (time.time() - start) * 1000

                if response.status_code == 200:
                    times.append(elapsed)
                    data = response.json()
                    num_results = data.get('count', 0)
                else:
                    print(f"   ⚠️  Search {i+1} failed: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️  Search {i+1} error: {e}")

            if (i + 1) % 10 == 0:
                print(f"   Completed {i+1}/{num_searches} searches...")

        # Results
        if times:
            results = {
                'mean': statistics.mean(times),
                'median': statistics.median(times),
                'min': min(times),
                'max': max(times),
                'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                'throughput': 1000 / statistics.mean(times),
                'success_rate': len(times) / num_searches * 100
            }

            print(f"\n📈 Results:")
            print(f"   Mean:         {results['mean']:.2f} ms/search")
            print(f"   Median:       {results['median']:.2f} ms/search")
            print(f"   Min:          {results['min']:.2f} ms/search")
            print(f"   Max:          {results['max']:.2f} ms/search")
            print(f"   Std Dev:      {results['stdev']:.2f} ms")
            print(f"   Throughput:   {results['throughput']:.2f} searches/sec")
            print(f"   Success Rate: {results['success_rate']:.1f}%")

            # Performance grading
            mean_time = results['mean']
            if mean_time < 100:
                grade = "🔥 EXCELLENT"
            elif mean_time < 500:
                grade = "✅ GOOD"
            elif mean_time < 1000:
                grade = "⚠️  ACCEPTABLE"
            else:
                grade = "❌ SLOW"

            print(f"   Performance:  {grade}")

            self.results['search_speed'] = results
            return results
        else:
            print("❌ No successful searches")
            return None

    def benchmark_concurrent_load(self, num_concurrent=10, duration_sec=30):
        """Benchmark concurrent request handling"""
        print(f"\n{'='*60}")
        print(f"📊 Benchmark: Concurrent Load ({num_concurrent} concurrent, {duration_sec}s)")
        print(f"{'='*60}")

        import threading
        import queue

        results_queue = queue.Queue()
        start_time = time.time()

        def worker():
            while time.time() - start_time < duration_sec:
                # Create test image
                test_image = create_test_image()
                image_base64 = image_to_base64(test_image)

                # Search
                req_start = time.time()
                try:
                    response = requests.post(
                        f"{self.api_url}/medical/search",
                        json={'image_base64': image_base64, 'limit': 5},
                        timeout=30
                    )
                    elapsed = (time.time() - req_start) * 1000

                    if response.status_code == 200:
                        results_queue.put(('success', elapsed))
                    else:
                        results_queue.put(('error', elapsed))
                except Exception:
                    results_queue.put(('error', 0))

        # Start workers
        threads = []
        for i in range(num_concurrent):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        # Wait for completion
        for t in threads:
            t.join()

        # Collect results
        successes = []
        errors = 0
        while not results_queue.empty():
            status, elapsed = results_queue.get()
            if status == 'success':
                successes.append(elapsed)
            else:
                errors += 1

        total_requests = len(successes) + errors

        if successes:
            results = {
                'total_requests': total_requests,
                'successful': len(successes),
                'failed': errors,
                'mean': statistics.mean(successes),
                'median': statistics.median(successes),
                'throughput': len(successes) / duration_sec,
                'success_rate': len(successes) / total_requests * 100
            }

            print(f"\n📈 Results:")
            print(f"   Total requests:  {results['total_requests']}")
            print(f"   Successful:      {results['successful']}")
            print(f"   Failed:          {results['failed']}")
            print(f"   Mean response:   {results['mean']:.2f} ms")
            print(f"   Median response: {results['median']:.2f} ms")
            print(f"   Throughput:      {results['throughput']:.2f} req/sec")
            print(f"   Success rate:    {results['success_rate']:.1f}%")

            self.results['concurrent_load'] = results
            return results
        else:
            print("❌ No successful requests")
            return None

    def print_summary(self):
        """Print summary of all benchmarks"""
        print(f"\n{'='*60}")
        print(f"📊 BENCHMARK SUMMARY")
        print(f"{'='*60}")

        if 'embedding_generation' in self.results:
            emb = self.results['embedding_generation']
            print(f"\n🔧 Embedding Generation:")
            print(f"   {emb['mean']:.2f} ms/image ({emb['throughput']:.2f} img/sec)")

        if 'api_upload' in self.results:
            upl = self.results['api_upload']
            print(f"\n📤 API Upload:")
            print(f"   {upl['mean']:.2f} ms/upload ({upl['throughput']:.2f} uploads/sec)")
            print(f"   Success rate: {upl['success_rate']:.1f}%")

        if 'search_speed' in self.results:
            search = self.results['search_speed']
            print(f"\n🔍 Search Speed:")
            print(f"   {search['mean']:.2f} ms/search ({search['throughput']:.2f} searches/sec)")
            print(f"   Success rate: {search['success_rate']:.1f}%")

        if 'concurrent_load' in self.results:
            conc = self.results['concurrent_load']
            print(f"\n⚡ Concurrent Load:")
            print(f"   {conc['throughput']:.2f} req/sec")
            print(f"   Success rate: {conc['success_rate']:.1f}%")

        print(f"\n{'='*60}")


def main():
    print("=" * 60)
    print("🏁 CHAZON Medical Imaging Performance Benchmarks")
    print("=" * 60)

    bench = Benchmarks()

    # Check API health first
    if not bench.check_api_health():
        print("\n❌ API is not available. Start the backend first:")
        print("   docker-compose up -d")
        print("   OR")
        print("   python os/backend/api.py")
        return 1

    # Run benchmarks
    try:
        # 1. Embedding generation (local, no API)
        bench.benchmark_embedding_generation(num_images=100)

        # 2. API upload
        bench.benchmark_api_upload(num_uploads=25)

        # 3. Search speed
        bench.benchmark_search_speed(num_searches=50)

        # 4. Concurrent load
        bench.benchmark_concurrent_load(num_concurrent=5, duration_sec=15)

        # Summary
        bench.print_summary()

        print("\n✅ Benchmarks complete!")
        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmarks interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Benchmark error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
