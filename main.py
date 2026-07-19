"""
Faultline — a tiny FastAPI service with an INTENTIONAL bug, so you can see
the full Nozie loop in two minutes: crash -> AI investigation -> fix PR ->
(after merge) auto-redeploy.

`/crash` always fails with a ZeroDivisionError (averaging an empty list).
The Nozie agent running alongside this container catches it from the logs
and kicks off an investigation.
"""
import logging

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("faultline")

app = FastAPI(title="Faultline")


def calculate_average(numbers):
    # BUG (intentional): no guard against an empty list -> ZeroDivisionError.
    return sum(numbers) / len(numbers)


@app.get("/")
def root():
    return {"status": "ok", "service": "faultline"}


@app.get("/crash")
def crash():
    logger.info("Handling /crash — about to compute average of []")
    return {"average": calculate_average([])}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
