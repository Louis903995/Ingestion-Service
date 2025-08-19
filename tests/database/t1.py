# import os
# from dotenv import load_dotenv
# from opentelemetry import metrics
# from opentelemetry.sdk.metrics import MeterProvider
# from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# import time

# load_dotenv(dotenv_path=".env", override=False)


# exporter = AzureMonitorMetricExporter.from_connection_string(
#     os.environ["APP_INSIGHT_CONNECTION_STRING"]
# )
# reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

# provider = MeterProvider(metric_readers=[reader])
# metrics.set_meter_provider(provider)

# meter = metrics.get_meter(__name__)

# COMPTEUR_TOTAL_INGESTIONS_TICKET = meter.create_counter(
#     name="ingestions.tickets.total",
#     description="Nombre total d'ingestions de ticket",
#     unit="1"
# )
# COMPTEUR_INGESTIONS_TICKET_ERREUR = meter.create_counter(
#     name="ingestions.tickets.erreurs",
#     description="Nombre d'échecs d'ingestion de tickets",
#     unit="1"
# )

# COMPTEUR_TOTAL_INGESTIONS_TICKET.add(1, {"status": "success"})

# # Ingestion ratée, avec cause
# COMPTEUR_TOTAL_INGESTIONS_TICKET.add(1, {"status": "failure"})
# COMPTEUR_INGESTIONS_TICKET_ERREUR.add(1, {"cause": "cause1"})
