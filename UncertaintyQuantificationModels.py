class UncertaintyQuantificationModels:
    """
    Mathematical models for quantifying different types of uncertainty
    Implements statistical and probabilistic methods
    """
    def __init__(self):
        self.statistical_models = StatisticalModels()
        self.bayesian_models = BayesianModels()
        self.probability_models = ProbabilityModels()
        self.propagation_models = PropagationModels()
        self.fuzzy_models = FuzzyLogicModels()

class StatisticalModels:
    """
    Classical statistical models for uncertainty quantification
    """
    def calculate_statistical_uncertainty(self, data):
        return {
            'confidence_intervals': self.compute_confidence_intervals(data),
            'prediction_intervals': self.compute_prediction_intervals(data),
            'variance_components': self.compute_variance_components(data)
        }

    def compute_confidence_intervals(self, data, confidence_level=0.95):
        """
        Calculates confidence intervals using multiple methods
        CI = point_estimate ± (critical_value * standard_error)
        """
        n = len(data)
        point_estimate = np.mean(data)
        std_error = np.std(data, ddof=1) / np.sqrt(n)
        critical_value = stats.t.ppf((1 + confidence_level) / 2, df=n-1)
        
        ci_lower = point_estimate - critical_value * std_error
        ci_upper = point_estimate + critical_value * std_error
        
        return {
            'interval': (ci_lower, ci_upper),
            'point_estimate': point_estimate,
            'standard_error': std_error,
            'degrees_freedom': n-1
        }

class BayesianModels:
    """
    Bayesian models for uncertainty quantification
    """
    def calculate_bayesian_uncertainty(self, data, prior):
        return {
            'posterior_distribution': self.compute_posterior(data, prior),
            'credible_intervals': self.compute_credible_intervals(data),
            'bayes_factors': self.compute_bayes_factors(data)
        }

    def compute_posterior(self, data, prior):
        """
        Computes posterior distribution using Bayes' theorem
        P(θ|D) ∝ P(D|θ) * P(θ)
        """
        likelihood = self._compute_likelihood(data)
        posterior = likelihood * prior
        normalization = np.trapz(posterior)  # Normalize posterior
        
        return {
            'distribution': posterior / normalization,
            'parameters': self._estimate_posterior_parameters(posterior),
            'mode': self._find_posterior_mode(posterior),
            'hpd_interval': self._compute_hpd_interval(posterior)
        }

class ProbabilityModels:
    """
    Probability models for uncertainty representation
    """
    def calculate_probabilistic_uncertainty(self, data):
        return {
            'probability_distributions': self.fit_distributions(data),
            'mixture_models': self.fit_mixture_models(data),
            'copula_models': self.fit_copula_models(data)
        }

    def fit_distributions(self, data):
        """
        Fits probability distributions to data
        Tests multiple distributions and selects best fit
        """
        distributions = ['normal', 'lognormal', 'gamma', 'weibull']
        fits = {}
        
        for dist in distributions:
            params = self._estimate_parameters(data, dist)
            goodness_of_fit = self._compute_goodness_of_fit(data, dist, params)
            fits[dist] = {
                'parameters': params,
                'goodness_of_fit': goodness_of_fit,
                'aic': self._compute_aic(data, dist, params),
                'bic': self._compute_bic(data, dist, params)
            }
        
        return {
            'best_fit': self._select_best_fit(fits),
            'all_fits': fits
        }

class PropagationModels:
    """
    Models for uncertainty propagation through systems
    """
    def calculate_propagated_uncertainty(self, input_uncertainties, model):
        return {
            'analytical_propagation': self.compute_analytical_propagation(input_uncertainties, model),
            'numerical_propagation': self.compute_numerical_propagation(input_uncertainties, model),
            'monte_carlo_propagation': self.compute_monte_carlo_propagation(input_uncertainties, model)
        }

    def compute_monte_carlo_propagation(self, input_uncertainties, model, n_samples=10000):
        """
        Propagates uncertainty using Monte Carlo simulation
        """
        samples = self._generate_samples(input_uncertainties, n_samples)
        results = np.array([model(sample) for sample in samples])
        
        return {
            'mean': np.mean(results),
            'std': np.std(results),
            'percentiles': np.percentile(results, [2.5, 97.5]),
            'distribution': self._fit_output_distribution(results),
            'sensitivity': self._compute_sensitivity_indices(samples, results)
        }

class FuzzyLogicModels:
    """
    Fuzzy logic models for handling uncertainty
    """
    def calculate_fuzzy_uncertainty(self, data):
        return {
            'membership_functions': self.compute_membership_functions(data),
            'fuzzy_rules': self.define_fuzzy_rules(data),
            'defuzzification': self.compute_defuzzification(data)
        }

    def compute_membership_functions(self, data):
        """
        Computes fuzzy membership functions
        """
        membership_types = ['triangular', 'gaussian', 'trapezoidal']
        functions = {}
        
        for type_ in membership_types:
            params = self._optimize_membership_parameters(data, type_)
            functions[type_] = {
                'parameters': params,
                'membership_values': self._compute_membership_values(data, type_, params),
                'overlap': self._compute_overlap_degree(data, type_, params),
                'coverage': self._compute_coverage(data, type_, params)
            }
        
        return functions
