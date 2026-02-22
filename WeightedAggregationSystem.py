class WeightedAggregationSystem:
    """
    Comprehensive system for weighted aggregation of multiple factors
    Implements various weighting schemes and aggregation methods
    """
    def __init__(self):
        self.linear_aggregator = LinearAggregator()
        self.nonlinear_aggregator = NonlinearAggregator()
        self.hierarchical_aggregator = HierarchicalAggregator()
        self.fuzzy_aggregator = FuzzyAggregator()
        self.dynamic_aggregator = DynamicAggregator()

class LinearAggregator:
    """
    Linear weighted aggregation methods
    """
    def aggregate_linear(self, factors, weights):
        """
        Simple weighted sum: Σ(wi * xi)
        Normalized weighted average: Σ(wi * xi) / Σwi
        """
        def weighted_sum(factors, weights):
            return np.sum([w * f for w, f in zip(weights, factors)])
        
        def normalized_average(factors, weights):
            return weighted_sum(factors, weights) / np.sum(weights)
        
        return {
            'weighted_sum': weighted_sum(factors, weights),
            'normalized_average': normalized_average(factors, weights),
            'weights': weights,
            'normalization_factor': np.sum(weights)
        }

    def calculate_weights(self, importance_scores, constraints):
        """
        Calculates weights based on importance and constraints
        wi = importance_i * constraint_factor_i / Σ(importance_j * constraint_factor_j)
        """
        raw_weights = [imp * const for imp, const in zip(importance_scores, constraints)]
        normalization = sum(raw_weights)
        normalized_weights = [w / normalization for w in raw_weights]
        
        return {
            'weights': normalized_weights,
            'raw_weights': raw_weights,
            'importance_scores': importance_scores,
            'constraints': constraints
        }

class NonlinearAggregator:
    """
    Nonlinear weighted aggregation methods
    """
    def aggregate_nonlinear(self, factors, weights, parameters):
        """
        Implements various nonlinear aggregation methods
        """
        return {
            'geometric_mean': self.geometric_weighted_mean(factors, weights),
            'power_mean': self.power_weighted_mean(factors, weights, parameters['p']),
            'exponential_sum': self.exponential_weighted_sum(factors, weights, parameters['alpha']),
            'logarithmic_sum': self.logarithmic_weighted_sum(factors, weights)
        }

    def geometric_weighted_mean(self, factors, weights):
        """
        Geometric weighted mean: Π(xi^wi)
        """
        return np.prod([x**w for x, w in zip(factors, weights)])

    def power_weighted_mean(self, factors, weights, p):
        """
        Power mean: (Σ(wi * xi^p) / Σwi)^(1/p)
        """
        numerator = sum(w * (x**p) for w, x in zip(weights, factors))
        denominator = sum(weights)
        return (numerator / denominator) ** (1/p)

class HierarchicalAggregator:
    """
    Hierarchical weighted aggregation methods
    """
    def aggregate_hierarchical(self, hierarchy, weights):
        """
        Aggregates factors in hierarchical structure
        """
        def aggregate_level(level_data, level_weights):
            if isinstance(level_data, dict):
                sub_results = {
                    key: aggregate_level(value, level_weights[key])
                    for key, value in level_data.items()
                }
                return self.combine_level_results(sub_results, level_weights)
            return level_data * level_weights

        return {
            'final_score': aggregate_level(hierarchy, weights),
            'level_scores': self.calculate_level_scores(hierarchy, weights),
            'contribution_analysis': self.analyze_contributions(hierarchy, weights)
        }

    def combine_level_results(self, results, weights):
        """
        Combines results within a hierarchical level
        """
        total_weight = sum(weights.values())
        weighted_sum = sum(
            result * weights[key] / total_weight
            for key, result in results.items()
        )
        return weighted_sum

class FuzzyAggregator:
    """
    Fuzzy weighted aggregation methods
    """
    def aggregate_fuzzy(self, fuzzy_factors, fuzzy_weights):
        """
        Implements fuzzy weighted aggregation
        """
        return {
            'fuzzy_weighted_sum': self.fuzzy_weighted_sum(fuzzy_factors, fuzzy_weights),
            'fuzzy_ordered_weighted': self.fuzzy_ordered_weighted(fuzzy_factors, fuzzy_weights),
            'fuzzy_choquet': self.fuzzy_choquet_integral(fuzzy_factors, fuzzy_weights)
        }

    def fuzzy_weighted_sum(self, factors, weights):
        """
        Fuzzy weighted sum using alpha-cuts
        """
        def alpha_cut_aggregation(alpha):
            factor_cuts = [f.alpha_cut(alpha) for f in factors]
            weight_cuts = [w.alpha_cut(alpha) for w in weights]
            return self.interval_weighted_sum(factor_cuts, weight_cuts)
        
        return [alpha_cut_aggregation(a) for a in np.linspace(0, 1, 100)]

class DynamicAggregator:
    """
    Dynamic weighted aggregation methods
    """
    def aggregate_dynamic(self, time_series_factors, time_varying_weights):
        """
        Implements dynamic weighted aggregation over time
        """
        return {
            'temporal_aggregation': self.temporal_weighted_sum(time_series_factors, time_varying_weights),
            'moving_average': self.moving_weighted_average(time_series_factors, time_varying_weights),
            'exponential_smoothing': self.exponential_weighted_smoothing(time_series_factors, time_varying_weights)
        }

    def temporal_weighted_sum(self, factors, weights):
        """
        Time-dependent weighted sum
        """
        def aggregate_timestep(t):
            current_factors = [f[t] for f in factors]
            current_weights = [w[t] for w in weights]
            return sum(f * w for f, w in zip(current_factors, current_weights))
        
        return [aggregate_timestep(t) for t in range(len(factors[0]))]
