"""Prometheus metrics for KoalaTech services (Task 10.2D).

Records request rate, latency and errors per endpoint and exposes them at /metrics.
Uses the route template (e.g. /students/{student_id}) rather than the raw URL,
so metric labels stay low-cardinality.
"""
import time

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests handled",
    ["method", "path", "status"],
)

HTTP_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", "unmatched")


def setup_metrics(app: FastAPI) -> None:
    @app.middleware("http")
    async def record_metrics(request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        start = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            path = _route_template(request)
            HTTP_REQUESTS.labels(request.method, path, str(status_code)).inc()
            HTTP_LATENCY.labels(request.method, path).observe(time.perf_counter() - start)

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)