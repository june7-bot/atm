import random
# import requests as requests

BASE_URL = "BANK_API"
RETURN_CODE = {100: 'Success',
               200: 'It is not card', 201: 'It is not appropriate card',
               202: 'It is not appropriate pin', 203: 'It is not matched pin',
               204: 'There are no registered accounts.',
               205: 'Please try again in a moment',
               206: 'The deposit is only available for more than a dollar.', 207: 'Please try again in a moment',
               208: 'The withdraw is only available for more than a dollar.', 209: 'Please try again in a moment',
               210: 'Money is scarce. Please use another ATM.',
               211: 'You cannot withdraw more than the amount you have.'
               }
# Account balance for testing
ACCOUNTS = {'A': 100, 'B': 10, 'C': 0}


class Atm:
    def __init__(self):
        self.__money = 10000000000

    def check_card(self, card):
        # If it is not a card (paper etc.)
        if card != 'CARD':
            return RETURN_CODE[200]

        # If it is proper card (Unregistered card etc.)
        # return 0 if not appropriate else 1
        # response = requests.post(f"{BASE_URL}/is_card_appropriate", json={"card": card})
        response = 1
        if not response:
            return RETURN_CODE[201]

        return RETURN_CODE[100]

    def check_pin(self, card, pin):
        if pin < 1000 or pin > 9999:
            return RETURN_CODE[202]

        # If it is matched card pin
        # return 0 if not matched else 1
        # response = requests.post(f"{BASE_URL}/is_pin_appropriate", json={"card" : card, "pin": pin})
        response = 1
        if not response:
            return RETURN_CODE[203]

        return RETURN_CODE[100]

    def get_accounts(self, card):
        # return 0 if fail else 1
        # response = requests.post(f"{BASE_URL}/get_accounts", json={"card": card})
        response = 1

        # if no registered accounts
        if not response:
            return RETURN_CODE[204], ''

        accounts = ['A', 'B', 'C']
        return RETURN_CODE[100], accounts

    def get_balance(self, account):
        # return 0 if fail else 1
        # response = requests.post(f"{BASE_URL}/get_balance", json={"account": account})
        response = 1

        if not response:
            return RETURN_CODE[205], ''

        balance = random.randint(0, 100)
        if balance < 0:
            return RETURN_CODE[205], ''

        return RETURN_CODE[100], ACCOUNTS[account]

    def do_deposit(self, account, amount):
        if amount <= 0:
            return RETURN_CODE[206], ''

        # return 0 if fail else 1
        # response = requests.post(f"{BASE_URL}/deposit", json={"account": account, "amount" : amount})
        response = 1
        if not response:
            return RETURN_CODE[207], ''

        balance_after_deposit = ACCOUNTS[account] + amount
        if balance_after_deposit <= 0:
            return RETURN_CODE[207], ''

        ACCOUNTS[account] += amount
        return RETURN_CODE[100], balance_after_deposit

    def do_withdraw(self, account, amount):
        if amount <= 0:
            return RETURN_CODE[208], ''

        # When withdrawing more than account money
        if amount > ACCOUNTS[account]:
            return RETURN_CODE[211], ''

        # When withdrawing more than ATM money
        if amount > self.__money:
            return RETURN_CODE[210], ''

        # return 0 if fail else 1
        # response = requests.post(f"{BASE_URL}/withdraw", json={"account": account, "amount" : amount})
        response = 1
        if not response:
            return RETURN_CODE[209], ''

        balance_after_withdraw = ACCOUNTS[account] - amount
        if balance_after_withdraw < 0:
            return RETURN_CODE[209], ''

        ACCOUNTS[account] -= amount
        return RETURN_CODE[100], balance_after_withdraw


if __name__ == "__main__":
    atm = Atm()

    # Insert card
    card = 'CARD'
    res = atm.check_card(card)
    if res != RETURN_CODE[100]:
        raise Exception(res)

    # Check pin
    pin = random.randint(1000, 9999)
    res = atm.check_pin(card, pin)
    if res != RETURN_CODE[100]:
        raise Exception(res)

    # Get Accounts
    res, card_accounts = atm.get_accounts(card)
    if res != RETURN_CODE[100]:
        raise Exception(res)

    # show accounts to user for select
    print('Please enter an account only "A" or "B" or "C"')

    account = input()
    if account not in ACCOUNTS.keys():
        raise Exception('enter Wrong account')

    while 1:
        # show options to user for select
        print('Please enter an option only "balance" or "deposit" or "withdraw" or "exit"')
        action = input()
        if action == 'exit':
            break
        if action not in ['balance', 'deposit', 'withdraw']:
            raise Exception('enter Wrong option')

        # Get balance'
        if action == 'balance':
            res, balance = atm.get_balance(account)
            if res != RETURN_CODE[100]:
                raise Exception(res)
            # show balance to user
            print(f'Your balance is {balance}')

        # do deposit
        elif action == 'deposit':

            print('Please enter deposit amount only integer')
            deposit_amount = input()

            if not deposit_amount.isdigit():
                raise Exception('Wrong deposit amount')
            deposit_amount = int(deposit_amount)

            res, balance_after_deposit = atm.do_deposit(account, deposit_amount)
            if res != RETURN_CODE[100]:
                if res == RETURN_CODE[207]:
                    # return deposit_amount to user
                    pass
                raise Exception(res)

            print(f'Deposit success! Your balance is {ACCOUNTS[account]}')

        # do withdraw
        elif action == 'withdraw':

            print('Please enter withdraw amount only integer')
            withdraw_amount = input()

            if not withdraw_amount.isdigit():
                raise Exception('Wrong withdraw amount')
            withdraw_amount = int(withdraw_amount)

            res, balance_after_withdraw = atm.do_withdraw(account, withdraw_amount)
            if res != RETURN_CODE[100]:
                raise Exception(res)
            print(f'Withdraw success! Your balance is {balance_after_withdraw}')
        print()