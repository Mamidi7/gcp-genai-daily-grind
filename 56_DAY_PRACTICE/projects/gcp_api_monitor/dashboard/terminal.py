"""
dashboard/terminal.py — Beautiful terminal UI using rich.
This is the NICE-TO-HAVE code. Completely separate from core/ logic.

CORE RULE: dashboard/ imports from core/, never the other way around.
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
import sys
import time
from datetime import datetime

sys.path.insert(0, "/tmp/gcp_api_monitor")

from core.models import EndpointHealth, HealthSummary, HealthStatus
from core.analyzer import compute_summary, get_recommendations, categorize_endpoints


console = Console()


def render_health_dashboard(endpoints: list[EndpointHealth]) -> None:
    """
    Main dashboard renderer.
    Takes core models → uses rich to display beautifully.
    Zero changes to core/ logic needed.
    """
    summary = compute_summary(endpoints)
    recommendations = get_recommendations(summary)
    from core.models import SLAThresholds
    thresholds = SLAThresholds()
    healthy, degraded, critical = categorize_endpoints(endpoints, thresholds)

    console.clear()

    # ─── Header ────────────────────────────────────────────────────────────────
    console.print(Panel.fit(
        "[bold white on #1a1a2e]   🚀 GCP API HEALTH DASHBOARD   [/bold white on #1a1a2e]",
        border_style="bright_blue",
        padding=(0, 2)
    ))
    console.print()

    # ─── Insights Panel ───────────────────────────────────────────────────────
    insight_lines = []

    if summary.critical_count > 0:
        insight_lines.append(
            f"  🚨 [bold red]{summary.critical_count} CRITICAL[/bold red] — immediate action needed"
        )
    if summary.degraded_count > 0:
        insight_lines.append(
            f"  ⚠️  [bold yellow]{summary.degraded_count} DEGRADED[/bold yellow] — monitor closely"
        )
    if summary.critical_count == 0 and summary.degraded_count == 0:
        insight_lines.append(f"  ✅ [bold green]ALL SYSTEMS NOMINAL[/bold green]")

    insight_lines.extend([
        f"  📊 Total Requests: [cyan]{summary.total_requests:,}[/cyan]",
        f"  📈 Avg Error Rate: [cyan]{summary.avg_error_rate:.2f}%[/cyan]",
        f"  ⏱️  Avg Latency: [cyan]{summary.avg_latency_ms:.0f}ms[/cyan]",
    ])

    console.print(Panel(
        "\n".join(insight_lines),
        title="[b]📋 INSIGHTS[/b]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()

    # ─── Main Table ─────────────────────────────────────────────────────────────
    table = Table(
        title="[b]🔍 Endpoint Health Details[/b]",
        header_style="bold white on #2d2d44",
        border_style="#4a4a6a",
        show_lines=True,
    )

    table.add_column("Endpoint", style="cyan bold", width=32)
    table.add_column("Region", style="magenta", width=15)
    table.add_column("Latency", justify="right", width=12)
    table.add_column("Error Rate", justify="right", width=12)
    table.add_column("Requests", justify="right", width=12)
    table.add_column("Status", justify="center", width=12)

    SLA_LATENCY_MS = 500.0
    SLA_ERROR_RATE = 1.0

    for ep in endpoints:
        lat = ep.latency_ms
        err = ep.error_rate

        # Latency cell
        if lat > 1000:
            lat_str = f"[red bold]{lat}ms[/red bold]"
        elif lat > SLA_LATENCY_MS:
            lat_str = f"[yellow bold]{lat}ms[/yellow bold]"
        else:
            lat_str = f"[green]{lat}ms[/green]"

        # Error rate cell
        if err > 3.0:
            err_str = f"[red bold]{err}%[/red bold]"
        elif err > SLA_ERROR_RATE:
            err_str = f"[yellow bold]{err}%[/yellow bold]"
        else:
            err_str = f"[green]{err}%[/green]"

        # Status badge
        if lat > 1000 or err > 3.0:
            status = "[red]🔴 DOWN[/red]"
        elif lat > SLA_LATENCY_MS or err > SLA_ERROR_RATE:
            status = "[yellow]🟡 SLOW[/yellow]"
        else:
            status = "[green]🟢 OK[/green]"

        req_str = f"[dim]{ep.requests:,}[/dim]"

        table.add_row(ep.endpoint, ep.region, lat_str, err_str, req_str, status)

    console.print(table)
    console.print()

    # ─── Recommendations Panel ────────────────────────────────────────────────
    rec_lines = ["[bold yellow]Recommendations:[/bold yellow]"]
    for i, rec in enumerate(recommendations, 1):
        rec_lines.append(f"  {i}. {rec}")

    console.print(Panel(
        "\n".join(rec_lines),
        title="💡 [b]NEXT STEPS[/b]",
        border_style="yellow",
        padding=(1, 2)
    ))

    console.print()
    console.print(
        f"[dim]Generated at {datetime.now().strftime('%H:%M:%S')} | "
        f"SLA: Latency < {SLA_LATENCY_MS}ms | Error Rate < {SLA_ERROR_RATE}%[/dim]"
    )


# ─── Entry point when run directly ───────────────────────────────────────────
if __name__ == "__main__":
    # Sample data — same as what your FastAPI app would return
    sample_endpoints = [
        EndpointHealth(endpoint="/v1/gemini/generate", region="us-central1",
                       latency_ms=245, error_rate=0.2, requests=15234),
        EndpointHealth(endpoint="/v1/text/embeddings", region="us-east1",
                       latency_ms=89, error_rate=0.1, requests=28456),
        EndpointHealth(endpoint="/v1/images/generate", region="europe-west1",
                       latency_ms=1203, error_rate=4.7, requests=4521),
        EndpointHealth(endpoint="/v1/audio/transcribe", region="asia-east1",
                       latency_ms=567, error_rate=1.2, requests=8923),
        EndpointHealth(endpoint="/v1/models/list", region="us-central1",
                       latency_ms=45, error_rate=0.0, requests=67890),
        EndpointHealth(endpoint="/v1/moderation/classify", region="us-east1",
                       latency_ms=312, error_rate=0.8, requests=12345),
    ]

    render_health_dashboard(sample_endpoints)
