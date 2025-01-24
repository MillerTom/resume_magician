import os
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import requests
import asyncio
from django.views.decorators.csrf import csrf_exempt

# Set Azure App Insights connection string
APP_INSIGHTS_CONNECTION_STRING = (
    "InstrumentationKey=d1cf04de-2ec6-4822-9cf4-62e1b4089ad5;"
    "IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;"
    "LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;"
    "ApplicationId=9e2f2054-e7e1-4425-9978-c84422ad3bc5"
)

@method_decorator(csrf_exempt, name='dispatch')
class LogView(View):
    async def post(self, request):
        try:
            # Parse request parameters
            message = request.POST.get("Message")
            severity = request.POST.get("Severity")
            consuming_app = request.POST.get("ConsumingApp")

            if not message or not severity or not consuming_app:
                return JsonResponse({"error": "Missing parameters."}, status=400)

            # Prepare log data
            log_data = {
                "Message": message,
                "Severity": severity,
                "ConsumingApp": consuming_app
            }

            # Send log data to Azure App Insights
            ingestion_url = f"{APP_INSIGHTS_CONNECTION_STRING.split(';')[1].split('=')[1]}v2/track"
            headers = {"Content-Type": "application/json"}

            response = await asyncio.to_thread(requests.post, ingestion_url, json=log_data, headers=headers)
            response.raise_for_status()

            return JsonResponse({"status": "Log sent successfully."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
