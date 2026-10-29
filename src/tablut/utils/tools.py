import time

from tablut.utils.logger import Logger


class Timer:
    """Simple timer to track elapsed and remaining time."""

    def __init__(self, timeout: float) -> None:
        """
        Initialize timer with timeout in seconds.

        Args:
            timeout: Maximum time allowed in seconds
        """
        self.__start_time = time.perf_counter()
        self.__timeout = timeout

    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        return time.perf_counter() - self.__start_time

    def remaining(self) -> float:
        """Get remaining time in seconds (min 0)."""
        return max(0, self.__timeout - self.elapsed())

    def is_timeout(self) -> bool:
        """Check if timeout exceeded."""
        return self.elapsed() >= self.__timeout

    def reset(self) -> None:
        """Reset the timer start time to current time."""
        self.__start_time = time.perf_counter()


class Benchmark:
    """Performance benchmarking utilities."""

    @staticmethod
    def run() -> float:
        """
        Run benchmark to estimate operations per second.

        Returns:
            Operations per second
        """
        logger = Logger("Benchmark")

        logger.info("Benchmarking: How many operations in 1 second?")

        start = time.perf_counter()
        count = 0
        while time.perf_counter() - start < 1.0:
            count += 1
        elapsed = time.perf_counter() - start

        ops_per_sec = count / elapsed
        logger.info(f"Operations/sec: {ops_per_sec:.2e}")

        return ops_per_sec


class Tools:
    @staticmethod
    def pos_to_symbol(row: int, col: int) -> str:
        """
        Convert board position to symbol notation (e.g., (1, 2) -> 'c2')
        chess_board[row][col] in symbol notation (e.g., (1, 2) -> 'c2')
        """
        COLUMN = "abcdefghi"
        ROW = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # Throw the error automatically if row or col is out of bounds
        symbol = f"{COLUMN[col]}{ROW[row]}"
        return symbol
