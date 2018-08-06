from threading import Thread
from refbot import referal_bot_loop
from distbot import distribution_bot_loop
from pay_handler import payment_handler_loop
from timer import timer_loop


class ReferalBotThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        referal_bot_loop()


class DistributionBotThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        distribution_bot_loop()


class PaymentHandlerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        payment_handler_loop()


class TimerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        timer_loop()


if __name__ == "__main__":
    ReferalBotThread().start()
    print('Referal bot started')
    DistributionBotThread().start()
    print('Distribution bot started')
    PaymentHandlerThread().start()
    print('Pay handler started')
    TimerThread().start()
    print('Timer started')
