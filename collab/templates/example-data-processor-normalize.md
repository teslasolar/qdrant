# DataProcessor Normalization Methods

**Module:** data-processor-normalize
**Purpose:** Data normalization (min-max, z-score, robust)
**Tokens:** ~240

## Code

```python
class DataProcessor:
    # ... (core and stats in other modules)

    def normalize_data(self, data, method="min_max"):
        """Normalize data using specified method"""

        if not data or len(data) == 0:
            return ArrayList()

        normalized = ArrayList()

        if method == "min_max":
            # Min-max normalization (0-1 range)
            min_val = min(data)
            max_val = max(data)
            range_val = max_val - min_val

            if range_val == 0:
                for _ in data:
                    normalized.add(0.5)
            else:
                for value in data:
                    norm_value = (value - min_val) / range_val
                    normalized.add(norm_value)

        elif method == "z_score":
            # Z-score normalization (mean=0, std=1)
            mean = self.calculate_mean(data)
            std = self.calculate_std(data, mean)

            if std == 0:
                for _ in data:
                    normalized.add(0.0)
            else:
                for value in data:
                    norm_value = (value - mean) / std
                    normalized.add(norm_value)

        elif method == "robust":
            # Robust normalization using median and IQR
            sorted_data = ArrayList(data)
            Collections.sort(sorted_data)

            median = self.calculate_median(sorted_data)
            q1 = self.calculate_percentile(sorted_data, 25)
            q3 = self.calculate_percentile(sorted_data, 75)
            iqr = q3 - q1

            if iqr == 0:
                for _ in data:
                    normalized.add(0.0)
            else:
                for value in data:
                    norm_value = (value - median) / iqr
                    normalized.add(norm_value)

        return normalized
```

## Methods
- `normalize_data(data, method)` - Normalize data using min_max, z_score, or robust

## Tokens
~240 tokens
