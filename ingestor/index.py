
import signal
import sys
import os
from data_ingestor import Ingestor

if __name__ == "__main__":

  ingestor = Ingestor()
  ingestor.start_ingestor()

  # Register signal handlers for termination signals
  def signal_handler(signal, frame):
    print("Termination signal received")
    ingestor.stop_ingestor()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)  # SIGINT: Ctrl+C
  signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM: Termination signal

  