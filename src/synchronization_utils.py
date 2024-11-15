import threading

printer_lock = threading.Lock()
scanner_lock = threading.Lock()

switching_semaphore = threading.Semaphore(1)


peterson_flags = [False, False]
peterson_turn = [0]

