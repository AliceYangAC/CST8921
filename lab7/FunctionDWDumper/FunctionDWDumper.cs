using Azure.Data.Tables;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using System.Text;

namespace FunctionDWDumper
{
    public class FunctionDWDumper
    {
        private readonly ILogger<FunctionDWDumper> _logger;
        private static readonly HttpClient _httpClient = new HttpClient();

        public FunctionDWDumper(ILogger<FunctionDWDumper> logger)
        {
            _logger = logger;
        }

        [Function("FunctionDWDumper")]
        public async Task Run(
            [EventHubTrigger("turbine-telemetry", Connection = "EventHubConnection", IsBatched = false)] string eventData,
            FunctionContext context)
        {
            try
            {
                _logger.LogInformation($"Event received: {eventData}");

                var telemetry = JsonSerializer.Deserialize<TelemetryPayload>(eventData,
                    new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

                if (telemetry == null)
                {
                    _logger.LogError("Failed to deserialize telemetry payload.");
                    return;
                }

                // Health scoring rule
                string status = (telemetry.WindSpeed > 15 && telemetry.GeneratedPower < 5)
                    ? "URGENT"
                    : "HEALTHY";

                // Connect to Table Storage and write the row
                string connectionString = Environment.GetEnvironmentVariable("AzureWebJobsStorage");
                var tableClient = new TableClient(connectionString, "TurbineMetrics");
                await tableClient.CreateIfNotExistsAsync();

                // Make RowKey safe by replacing colons (not allowed in Table Storage keys)
                string safeRowKey = telemetry.Timestamp.Replace(":", "-");

                var entity = new TableEntity(telemetry.DeviceId, safeRowKey)
                {
                    { "WindSpeed", telemetry.WindSpeed },
                    { "GeneratedPower", telemetry.GeneratedPower },
                    { "TurbineSpeed", telemetry.TurbineSpeed },
                    { "Status", status }
                };

                await tableClient.AddEntityAsync(entity);
                _logger.LogInformation($"Saved: DeviceId={telemetry.DeviceId}, Status={status}");

                // If URGENT, call the Logic App
                if (status == "URGENT")
                {
                    string logicAppUrl = Environment.GetEnvironmentVariable("LogicAppUrl");
                    var payload = new
                    {
                        DeviceId = telemetry.DeviceId,
                        Timestamp = telemetry.Timestamp,
                        WindSpeed = telemetry.WindSpeed,
                        GeneratedPower = telemetry.GeneratedPower,
                        TurbineSpeed = telemetry.TurbineSpeed,
                        Status = status
                    };

                    var json = JsonSerializer.Serialize(payload);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");
                    var response = await _httpClient.PostAsync(logicAppUrl, content);
                    _logger.LogInformation($"Logic App response: {response.StatusCode}");
                    _logger.LogInformation($"URGENT alert sent to Logic App for DeviceId={telemetry.DeviceId}");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error processing event: {ex.Message}");
                _logger.LogError($"Stack trace: {ex.StackTrace}");
            }
        }
    }
}