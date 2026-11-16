"""Local stand-in for the ESP32 + OLED + IoT Core.

This script demonstrates the kind of JSON message the simulated device sends.
It does not connect to AWS IoT Core. AWS MQTT connectivity can be added later
using the AWS IoT Device SDK and device certificates.
"""
import json

sample_request = {
    "device": "ESP32-SIMULATOR",
    "topic": "migration/assessment/request",
    "requirements": {
        "cpu": 2,
        "ram": 2,
        "storage": 20,
        "os": "Linux",
        "region": "ap-south-1"
    }
}

def main():
    print("=== MIGRATION ASSESSMENT DEVICE SIMULATOR ===")
    print("Simulated OLED: MIGRATION ASSESSMENT")
    print("\nMQTT-style request payload:")
    print(json.dumps(sample_request, indent=2))
    print("\nSimulated OLED: Request ready to send")
    print("(Local simulation only; AWS IoT Core is not contacted.)")

if __name__ == "__main__":
    main()
