# DataProcessor Statistical Methods

**Module:** data-processor-stats
**Purpose:** Statistical calculation methods (mean, std, median, percentile)
**Tokens:** ~180

## Code

```python
class DataProcessor:
    # ... (core in data-processor-core.md)

    def calculate_mean(self, data):
        """Calculate arithmetic mean"""
        if not data or len(data) == 0:
            return 0.0
        return sum(data) / len(data)

    def calculate_std(self, data, mean=None):
        """Calculate standard deviation"""
        if not data or len(data) <= 1:
            return 0.0

        if mean is None:
            mean = self.calculate_mean(data)

        variance_sum = 0.0
        for value in data:
            variance_sum += (value - mean) ** 2

        variance = variance_sum / (len(data) - 1)
        return math.sqrt(variance)

    def calculate_median(self, sorted_data):
        """Calculate median from sorted data"""
        if not sorted_data or len(sorted_data) == 0:
            return 0.0

        n = len(sorted_data)
        if n % 2 == 1:
            return sorted_data[n // 2]
        else:
            mid1 = sorted_data[n // 2 - 1]
            mid2 = sorted_data[n // 2]
            return (mid1 + mid2) / 2.0

    def calculate_percentile(self, sorted_data, percentile):
        """Calculate percentile from sorted data"""
        if not sorted_data or len(sorted_data) == 0:
            return 0.0

        n = len(sorted_data)
        index = (percentile / 100.0) * (n - 1)

        if index == int(index):
            return sorted_data[int(index)]
        else:
            lower = int(math.floor(index))
            upper = int(math.ceil(index))
            weight = index - lower

            return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
```

## Tokens
~180 tokens
