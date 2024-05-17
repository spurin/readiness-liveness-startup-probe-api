from flask import Flask
import time
import os
import logging
import threading
import signal
import sys

# Custom logging handler that flushes immediately
class ImmediateFlushHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

# Set up logging with custom handler
logger = logging.getLogger(__name__)
handler = ImmediateFlushHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Suppress the default Flask server logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# Environment variables for each endpoint
delays = {
    'startup': int(os.getenv("STARTUP_DELAY", 0)),
    'ready': int(os.getenv("READY_DELAY", 0)),
    'healthz': int(os.getenv("HEALTHZ_DELAY", 0))
}
chaos_frequencies = {
    'startup': int(os.getenv("STARTUP_CHAOS_FREQUENCY", 0)),
    'ready': int(os.getenv("READY_CHAOS_FREQUENCY", 0)),
    'healthz': int(os.getenv("HEALTHZ_CHAOS_FREQUENCY", 0))
}
failure_thresholds = {
    'startup': int(os.getenv("STARTUP_PERMANENT_FAILURE_THRESHOLD", 0)),
    'ready': int(os.getenv("READY_PERMANENT_FAILURE_THRESHOLD", 0)),
    'healthz': int(os.getenv("HEALTHZ_PERMANENT_FAILURE_THRESHOLD", 0))
}

# Global flags and counters for probe readiness
flags = {
    'startup': False,
    'ready': False,
    'healthz': False
}
call_counts = {
    'startup': 0,
    'ready': 0,
    'healthz': 0
}
consecutive_failures = {
    'startup': 0,
    'ready': 0,
    'healthz': 0
}
permanent_failure_activated = {
    'startup': False,
    'ready': False,
    'healthz': False
}

# Function to simulate delays for each probe
def simulate_delay(endpoint):
    delay = delays[endpoint]
    logger.info(f"Simulating {endpoint.capitalize()} delay for {delay} seconds")
    time.sleep(delay)
    flags[endpoint] = True
    logger.info(f"{endpoint.capitalize()} delay complete")
    if endpoint == 'startup':
        # Start delays for ready and healthz after startup completes
        threading.Thread(target=simulate_delay, args=('ready',)).start()
        threading.Thread(target=simulate_delay, args=('healthz',)).start()

# Start the simulation for startup delay
threading.Thread(target=simulate_delay, args=('startup',)).start()

# Probe handler function for generic use
def probe_handler(endpoint):
    call_counts[endpoint] += 1
    chaos_frequency = chaos_frequencies[endpoint]
    failure_threshold = failure_thresholds[endpoint]

    if not flags[endpoint]:
        consecutive_failures[endpoint] += 1
        log_msg = f"{endpoint.capitalize()} probe failed: request_count:{call_counts[endpoint]}, consecutive_failures:{consecutive_failures[endpoint]}"
        logger.info(log_msg)
        return "Error", 500

    if failure_threshold > 0 and call_counts[endpoint] >= failure_threshold:
        permanent_failure_activated[endpoint] = True

    if permanent_failure_activated[endpoint]:
        consecutive_failures[endpoint] += 1
        log_msg = f"{endpoint.capitalize()} probe failed permanently after reaching threshold of {failure_threshold} calls: request_count:{call_counts[endpoint]}, consecutive_failures:{consecutive_failures[endpoint]}"
        logger.info(log_msg)
        return "Error", 500

    if chaos_frequency > 0 and call_counts[endpoint] % chaos_frequency == 0:
        consecutive_failures[endpoint] += 1
        log_msg = f"{endpoint.capitalize()} probe failed as per chaos frequency {chaos_frequency}: request_count:{call_counts[endpoint]}, consecutive_failures:{consecutive_failures[endpoint]}"
        logger.info(log_msg)
        return "Error", 500

    consecutive_failures[endpoint] = 0
    log_msg = f"{endpoint.capitalize()} probe successful: request_count:{call_counts[endpoint]}, consecutive_failures:{consecutive_failures[endpoint]}"
    logger.info(log_msg)
    return "OK", 200

@app.route("/startup")
def startup():
    return probe_handler('startup')

@app.route("/healthz")
def healthz():
    return probe_handler('healthz')

@app.route("/ready")
def ready():
    return probe_handler('ready')

def signal_handler(sig, frame):
    logger.info('Shutting down gracefully...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting Flask application on port {port}")
    app.run(host='0.0.0.0', port=port)

