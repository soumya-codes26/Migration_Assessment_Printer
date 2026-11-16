from flask import Flask, render_template, request
from assessment import recommend_instance
from pricing import get_hourly_price, estimate_monthly_cost

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            cpu = int(request.form.get("cpu", "2"))
            ram = float(request.form.get("ram", "2"))
            storage = int(request.form.get("storage", "20"))
            region = request.form.get("region", "ap-south-1")
            os_name = request.form.get("os", "Linux")

            if cpu < 1 or ram <= 0 or storage < 1:
                raise ValueError("CPU, RAM, and storage must be positive values.")

            instance = recommend_instance(cpu, ram)
            hourly, source = get_hourly_price(instance["type"], region, os_name)
            monthly = estimate_monthly_cost(hourly)

            result = {
                "cpu": cpu,
                "ram": ram,
                "storage": storage,
                "region": region,
                "os": os_name,
                "instance": instance,
                "hourly": hourly,
                "monthly": monthly,
                "price_source": source,
            }
        except (ValueError, TypeError) as exc:
            error = str(exc)
        except Exception as exc:
            error = f"Assessment failed: {exc}"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
