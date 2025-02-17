from time import time

CREDIT_LIMIT = 100
HOUR = 60 * 60
RESET_TIME = 24 * HOUR


class OutOfCreditsException(Exception):
    def __init__(self, *args):
        super().__init__("Credit counter is out of credits", *args)


class CreditCounter:
    def __init__(self):
        self.credits = 100
        self.time = time()

    def num_credits_remaining(self):
        return self.credits

    def credits_remaining(self):
        self.update_counter()
        if self.credits > 0:
            return True
        else:
            return False

    def update_counter(self):
        # if over a day has passed since the last time update, start the total call counter again
        current_time = time.time()
        time_elapsed = current_time - self.time
        if time_elapsed >= 86400:
            self.time = current_time
            self.reset_credits()
        return

    def reset_credits(self):
        self.credits = 100
        return

    def decrement_credit_counter(self):
        if self.credits_remaining():
            self.credits -= 1
        else:
            raise Exception("OUT OF SEARCH CREDITS (WITHIN CREDITCOUNTER)")
        return
