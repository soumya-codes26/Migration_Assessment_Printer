"""EC2 pricing helper.

By default the app uses clearly-labelled DEMO prices so it works without AWS credentials.
To query AWS Pricing API, set USE_LIVE_PRICING=1 and configure AWS credentials.
The AWS Price List API endpoint is commonly us-east-1; the requested product
region is supplied separately as a location filter.
"""
import os
import boto3

# Illustrative Linux On-Demand rates in USD/hour for a classroom demo only.
# They are NOT live quotes and may differ by region, date, tenancy and options.
DEMO_HOURLY_PRICES = {
    "t3.micro": 0.0104,
    "t3.small": 0.0208,
    "t3.medium": 0.0416,
    "t3.large": 0.0832,
    "m5.large": 0.096,
    "m5.xlarge": 0.192,
    "c5.xlarge": 0.17,
}

REGION_NAMES = {
    "ap-south-1": "Asia Pacific (Mumbai)",
    "us-east-1": "US East (N. Virginia)",
    "us-west-2": "US West (Oregon)",
}

def get_hourly_price(instance_type: str, region: str, os_name: str = "Linux"):
    """Return (hourly USD price, source label)."""
    if os.environ.get("USE_LIVE_PRICING") != "1":
        return DEMO_HOURLY_PRICES[instance_type], "Demo estimate (not live AWS pricing)"

    location = REGION_NAMES.get(region)
    if not location:
        raise ValueError("Live pricing is configured only for the regions listed in pricing.py.")

    client = boto3.client("pricing", region_name="us-east-1")
    filters = [
        {"Type": "TERM_MATCH", "Field": "ServiceCode", "Value": "AmazonEC2"},
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
        {"Type": "TERM_MATCH", "Field": "location", "Value": location},
        {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": os_name},
        {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
        {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
        {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
    ]
    response = client.get_products(
        ServiceCode="AmazonEC2",
        Filters=filters,
        MaxResults=100,
    )

    import json
    for item in response.get("PriceList", []):
        product = json.loads(item)
        terms = product.get("terms", {}).get("OnDemand", {})
        for term in terms.values():
            for dimension in term.get("priceDimensions", {}).values():
                price = dimension.get("pricePerUnit", {}).get("USD")
                if price is not None:
                    return float(price), "AWS Pricing API"

    raise RuntimeError(
        "No matching On-Demand price was returned. Check region, OS, permissions, "
        "or try demo mode."
    )

def estimate_monthly_cost(hourly_price: float) -> float:
    """Approximate monthly compute cost using 730 hours."""
    return round(hourly_price * 730, 2)
