
import signal
import sys
import os
from data_ingestor import DataIngestor

if __name__ == "__main__":

  ingestor = DataIngestor()
  ingestor.start_ingestor()

  # Register signal handlers for termination signals
  def signal_handler(signal, frame):
    print("Termination signal received. Stopping the ingestor...")
    #ingestor.stop_ingestor()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)  # SIGINT: Ctrl+C
  signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM: Termination signal

  