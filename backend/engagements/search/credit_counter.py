from time import time

CREDIT_LIMIT = 100
HOUR = 60 * 60
RESET_TIME = 24 * HOUR


class OutOfCreditsException(Exception):
    def __init__(self, *args):
        super().__init__("Credit counter is out of credits", *args)


class CreditCounter:
    def reset_credits(self) -> None:
        """
        Set credits back to the maximum.
        """
        self.credits = CREDIT_LIMIT

    def reset_time(self) -> None:
        """
        Set time back to the current epoch time in seconds.
        """
        self.time = time()

    def __init__(self) -> None:
        """
        Reset credits and time.
        """
        self.credits = None
        self.time = None
        self.reset_credits()
        self.reset_time()

    def get_credits(self) -> int:
        """
        Update counter and get credit count.
        :return: Credit count.
        """
        self.update_counter()
        return self.credits

    def get_elapsed_time(self) -> float:
        """
        Get time elapsed since last reset in seconds.
        :return: Time elapsed.
        """
        current_time = time()
        return current_time - self.time

    def credits_available(self) -> bool:
        """
        Check if there are credits available.
        :return: True if available, False otherwise.
        """
        return self.get_credits() > 0

    def credits_available_for(self, amount: int) -> bool:
        """
        Check if there are enough credits available for a given amount.
        :param amount: Amount to compare with.
        """
        return self.get_credits() >= amount

    def reset_time_elapsed(self) -> bool:
        """
        Check if enough time elapsed since last reset.
        :return: True if enough time elapsed, False otherwise.
        """
        return self.get_elapsed_time() >= RESET_TIME

    def update_counter(self) -> None:
        """
        Reset credits and time if enough time has elapsed.
        """
        if self.reset_time_elapsed():
            self.reset_time()
            self.reset_credits()

    def decrement_credits(self) -> None:
        """
        Decrement credits if there are credits available.
        Otherwise, raise OutOfCreditsException.
        """
        self.update_counter()
        if self.credits_available():
            self.credits -= 1
        else:
            raise OutOfCreditsException()
