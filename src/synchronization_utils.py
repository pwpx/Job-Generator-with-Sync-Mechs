import threading

# Mutexes for printer and scanner
printer_lock = threading.Lock()
scanner_lock = threading.Lock()

# Semaphore to control job switching
switching_semaphore = threading.Semaphore(1)


peterson_flags = [False, False]  # Flags for two users (0 and 1)
peterson_turn = [0]              # Shared turn variable


# Additional utilities for Peterson’s Solution can be added here if implemented
