import threading

# Mutexes for printer and scanner
printer_lock = threading.Lock()
scanner_lock = threading.Lock()

# Semaphore to control job switching
switching_semaphore = threading.Semaphore(1)

# Additional utilities for Peterson’s Solution can be added here if implemented
