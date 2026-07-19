"""Starts the Nozie agent, which watches the `faultline` container."""
import logging
import os
import threading

from nozie import NozieAgent

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    NozieAgent(
        api_key=os.environ["NOZIE_API_KEY"],
        dashboard_url=os.environ.get("NOZIE_DASHBOARD_URL", "https://nozie.xyz"),
        container="faultline",
    ).start()
    threading.Event().wait()  # keep the process alive
