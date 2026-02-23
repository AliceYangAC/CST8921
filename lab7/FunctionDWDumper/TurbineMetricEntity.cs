namespace FunctionDWDumper
{
    public class TurbineMetricEntity
    {
        public string PartitionKey { get; set; }
        public string RowKey { get; set; }
        public double WindSpeed { get; set; }
        public double GeneratedPower { get; set; }
        public double TurbineSpeed { get; set; }
        public string Status { get; set; }
    }

    public class TelemetryPayload
    {
        public string DeviceId { get; set; }
        public string Timestamp { get; set; }
        public double WindSpeed { get; set; }
        public double GeneratedPower { get; set; }
        public double TurbineSpeed { get; set; }
    }
}