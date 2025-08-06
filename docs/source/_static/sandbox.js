// Interactive Sandbox JavaScript

// Simulated Gatenet API for demonstration purposes
const GatenetAPI = {
  // HTTP Client simulation
  http: {
    get: async (url) => {
      await sleep(500);
      return {
        status: 200,
        data: {
          url: url,
          method: "GET",
          headers: { "Content-Type": "application/json" },
          origin: "sandbox-demo",
        },
      };
    },
    post: async (url, data) => {
      await sleep(750);
      return {
        status: 200,
        data: {
          url: url,
          method: "POST",
          json: data,
          headers: { "Content-Type": "application/json" },
        },
      };
    },
  },

  // DNS simulation
  dns: {
    lookup: async (domain) => {
      await sleep(300);
      const mockIPs = {
        "google.com": "142.250.185.78",
        "github.com": "140.82.113.3",
        "cloudflare.com": "104.16.124.96",
        "stackoverflow.com": "151.101.1.69",
      };
      return mockIPs[domain] || "203.0.113.1";
    },
  },

  // Geo IP simulation
  geo: {
    lookup: async (ip) => {
      await sleep(400);
      const mockGeo = {
        "8.8.8.8": { country: "US", city: "Mountain View", org: "Google LLC" },
        "1.1.1.1": { country: "US", city: "San Francisco", org: "Cloudflare" },
        "208.67.222.222": {
          country: "US",
          city: "San Francisco",
          org: "OpenDNS",
        },
      };
      return (
        mockGeo[ip] || { country: "Unknown", city: "Unknown", org: "Unknown" }
      );
    },
  },

  // Ping simulation
  ping: {
    test: async (host, count = 1) => {
      await sleep(count * 200);
      return {
        host: host,
        packets_sent: count,
        packets_received: count,
        packet_loss: 0,
        avg_time: Math.random() * 50 + 10,
      };
    },
  },

  // Service Discovery simulation
  discovery: {
    identify: (port, banner) => {
      const services = {
        22: {
          "SSH-2.0-OpenSSH": "OpenSSH Server",
          "SSH-2.0-libssh": "LibSSH Server",
        },
        80: {
          nginx: "Nginx HTTP Server",
          Apache: "Apache HTTP Server",
          "Server:": "HTTP Server",
        },
        443: { "": "HTTPS Server" },
        25: { Postfix: "Postfix SMTP", "220": "SMTP Server" },
        3306: { MySQL: "MySQL Database Server" },
        5432: { PostgreSQL: "PostgreSQL Database" },
      };

      if (services[port]) {
        for (const [key, value] of Object.entries(services[port])) {
          if (key === "" || banner.includes(key)) {
            return value;
          }
        }
      }
      return `Unknown Service (Port ${port})`;
    },
  },
};

// Utility functions
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function formatOutput(data, type = "json") {
  if (type === "json") {
    return JSON.stringify(data, null, 2);
  }
  return String(data);
}

function setOutput(elementId, content, isError = false) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = content;
    element.className = isError ? "error" : "success";
  }
}

function setLoading(elementId, isLoading = true) {
  const element = document.getElementById(elementId);
  if (element) {
    if (isLoading) {
      element.textContent = "Running...";
      element.className = "loading";
    }
  }
}

// HTTP Example Functions
async function runHttpExample() {
  const outputId = "http-output";
  setLoading(outputId);

  try {
    // Simulate the HTTP client example
    const getResponse = await GatenetAPI.http.get("https://httpbin.org/json");
    const postData = { message: "Hello from Gatenet!", user: "sandbox" };
    const postResponse = await GatenetAPI.http.post(
      "https://httpbin.org/post",
      postData
    );

    const output = `GET Response: ${formatOutput(getResponse.data)}

POST Response: ${formatOutput(postResponse.data)}`;

    setOutput(outputId, output);
  } catch (error) {
    setOutput(outputId, `Error: ${error.message}`, true);
  }
}

function resetHttpExample() {
  const originalCode = `# HTTP Client Example - Try it out!
from gatenet.http_.client import HTTPClient

# Create a client
client = HTTPClient("https://httpbin.org")

# Make a GET request
response = client.get("/json")
print("GET Response:", response["data"])

# Make a POST request
payload = {"message": "Hello from Gatenet!", "user": "sandbox"}
post_response = client.post("/post", data=payload)
print("POST Response:", post_response["data"]["json"])`;

  document.getElementById("http-code").value = originalCode;
  setOutput("http-output", 'Click "Run Code" to see the output...');
}

// Diagnostics Example Functions
async function runDiagnosticsExample() {
  const outputId = "diagnostics-output";
  setLoading(outputId);

  try {
    // Simulate diagnostics
    const ip = await GatenetAPI.dns.lookup("google.com");
    const geo = await GatenetAPI.geo.lookup("8.8.8.8");
    const pingResult = await GatenetAPI.ping.test("1.1.1.1", 3);

    const output = `google.com resolves to: ${ip}

8.8.8.8 location: ${formatOutput(geo)}

Ping result: ${formatOutput(pingResult)}`;

    setOutput(outputId, output);
  } catch (error) {
    setOutput(outputId, `Error: ${error.message}`, true);
  }
}

function resetDiagnosticsExample() {
  const originalCode = `# Network Diagnostics Example
from gatenet.diagnostics.dns import dns_lookup
from gatenet.diagnostics.geo import get_geo_info
from gatenet.diagnostics.ping import ping

# DNS Lookup
ip = dns_lookup("google.com")
print(f"google.com resolves to: {ip}")

# Geo IP Information
geo = get_geo_info("8.8.8.8")
print(f"8.8.8.8 location: {geo}")

# Ping test (simulated in browser)
result = ping("1.1.1.1", count=3)
print(f"Ping result: {result}")`;

  document.getElementById("diagnostics-code").value = originalCode;
  setOutput("diagnostics-output", 'Click "Run Code" to see the output...');
}

// Discovery Example Functions
async function runDiscoveryExample() {
  const outputId = "discovery-output";
  setLoading(outputId);

  try {
    await sleep(500); // Simulate processing time

    const services = [
      { port: 22, banner: "SSH-2.0-OpenSSH_8.9p1" },
      { port: 80, banner: "Server: nginx/1.18.0" },
      { port: 443, banner: "" },
      { port: 25, banner: "220 Postfix SMTP" },
      { port: 3306, banner: "MySQL Server 8.0.25" },
    ];

    let output = "Port 22 service: OpenSSH Server\n";
    output += "Port 80 service: Nginx HTTP Server\n";
    output += "SSH detector result: OpenSSH Server\n\n";

    services.forEach((service) => {
      const identified = GatenetAPI.discovery.identify(
        service.port,
        service.banner
      );
      output += `Port ${service.port}: ${identified}\n`;
    });

    setOutput(outputId, output);
  } catch (error) {
    setOutput(outputId, `Error: ${error.message}`, true);
  }
}

function resetDiscoveryExample() {
  const originalCode = `# Service Discovery Example
from gatenet.discovery.ssh import _identify_service, SSHDetector

# Basic service identification
service = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
print(f"Port 22 service: {service}")

# HTTP service detection
http_service = _identify_service(80, "Server: nginx/1.18.0")
print(f"Port 80 service: {http_service}")

# Using individual detectors
ssh_detector = SSHDetector()
result = ssh_detector.detect(22, "SSH-2.0-OpenSSH_8.9p1")
print(f"SSH detector result: {result}")

# Multiple service tests
services = [
    (443, ""),  # HTTPS
    (25, "220 Postfix SMTP"),
    (3306, "MySQL Server 8.0.25")
]

for port, banner in services:
    identified = _identify_service(port, banner)
    print(f"Port {port}: {identified}")`;

  document.getElementById("discovery-code").value = originalCode;
  setOutput("discovery-output", 'Click "Run Code" to see the output...');
}

// Quick Playground Functions
async function quickHttpTest() {
  const resultId = "quick-http-result";
  setLoading(resultId);

  try {
    const response = await GatenetAPI.http.get("/status");
    setOutput(resultId, `✅ Success: ${formatOutput(response.data)}`);
  } catch (error) {
    setOutput(resultId, `❌ Error: ${error.message}`, true);
  }
}

async function quickDnsTest() {
  const domain = document.getElementById("dns-input").value || "google.com";
  const resultId = "quick-dns-result";
  setLoading(resultId);

  try {
    const ip = await GatenetAPI.dns.lookup(domain);
    setOutput(resultId, `✅ ${domain} → ${ip}`);
  } catch (error) {
    setOutput(resultId, `❌ Error: ${error.message}`, true);
  }
}

async function quickServiceTest() {
  const select = document.getElementById("service-select");
  const [port, banner] = select.value.split(",");
  const resultId = "quick-service-result";
  setLoading(resultId);

  try {
    await sleep(300);
    const service = GatenetAPI.discovery.identify(parseInt(port), banner);
    setOutput(resultId, `✅ Port ${port}: ${service}`);
  } catch (error) {
    setOutput(resultId, `❌ Error: ${error.message}`, true);
  }
}

async function quickGeoTest() {
  const ip = document.getElementById("ip-input").value || "8.8.8.8";
  const resultId = "quick-geo-result";
  setLoading(resultId);

  try {
    const geo = await GatenetAPI.geo.lookup(ip);
    setOutput(resultId, `✅ ${ip}: ${geo.city}, ${geo.country} (${geo.org})`);
  } catch (error) {
    setOutput(resultId, `❌ Error: ${error.message}`, true);
  }
}

// Initialize sandbox when page loads
document.addEventListener("DOMContentLoaded", function () {
  console.log("🚀 Gatenet Interactive Sandbox Loaded!");

  // Add some visual feedback for interactive elements
  const buttons = document.querySelectorAll(
    ".run-button, .reset-button, .playground-button"
  );
  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      this.style.transform = "scale(0.95)";
      setTimeout(() => {
        this.style.transform = "";
      }, 150);
    });
  });
});

// Export functions for global access
window.runHttpExample = runHttpExample;
window.resetHttpExample = resetHttpExample;
window.runDiagnosticsExample = runDiagnosticsExample;
window.resetDiagnosticsExample = resetDiagnosticsExample;
window.runDiscoveryExample = runDiscoveryExample;
window.resetDiscoveryExample = resetDiscoveryExample;
window.quickHttpTest = quickHttpTest;
window.quickDnsTest = quickDnsTest;
window.quickServiceTest = quickServiceTest;
window.quickGeoTest = quickGeoTest;
