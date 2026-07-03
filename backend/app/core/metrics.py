
# Counters for system monitoring
metrics_data = {
    "http_requests_total": {},  # (method, endpoint) -> count
    "rate_limit_trips_total": 0,
    "model_inferences_total": 0
}

def increment_request_count(method: str, endpoint: str):
    key = (method, endpoint)
    metrics_data["http_requests_total"][key] = metrics_data["http_requests_total"].get(key, 0) + 1

def increment_rate_limit_trips():
    metrics_data["rate_limit_trips_total"] += 1

def increment_model_inferences():
    metrics_data["model_inferences_total"] += 1

def generate_prometheus_report() -> str:
    """
    Constructs a plain-text Prometheus exporter report.
    """
    lines = []
    
    # HTTP requests counter
    lines.append("# HELP http_requests_total Total number of HTTP requests processed.")
    lines.append("# TYPE http_requests_total counter")
    for (method, endpoint), val in metrics_data["http_requests_total"].items():
        lines.append(f'http_requests_total{{method="{method}",endpoint="{endpoint}"}} {val}')
        
    # Rate limit counter
    lines.append("# HELP rate_limit_trips_total Total requests blocked by rate limiter.")
    lines.append("# TYPE rate_limit_trips_total counter")
    lines.append(f'rate_limit_trips_total {metrics_data["rate_limit_trips_total"]}')
    
    # Model inference counter
    lines.append("# HELP model_inferences_total Total LLM tokens or inference queries executed.")
    lines.append("# TYPE model_inferences_total counter")
    lines.append(f'model_inferences_total {metrics_data["model_inferences_total"]}')
    
    return "\n".join(lines) + "\n"
