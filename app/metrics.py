from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from app.config import get_app_insights_conn_string

exporter = AzureMonitorMetricExporter.from_connection_string(
    get_app_insights_conn_string()
)
reader = PeriodicExportingMetricReader(
    exporter, export_interval_millis=5 * 60 * 1000
)  # on échantillone toutes les 5 minutes

provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)

COMPTEUR_TOTAL_INGESTIONS_TICKET = meter.create_counter(
    name="ingestions.tickets.total",
    description="Nombre total d'ingestions de ticket",
    unit="1",
)
COMPTEUR_INGESTIONS_TICKET_ERREUR = meter.create_counter(
    name="ingestions.tickets.erreurs",
    description="Nombre d'erreur d'ingestion de tickets",
    unit="1",
)
