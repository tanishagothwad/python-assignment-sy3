# Strategy Classes

class CreditCard:
    def pay(self, amount):
        print(f"Payment of ₹{amount} made using Credit Card.")


class DebitCard:
    def pay(self, amount):
        print(f"Payment of ₹{amount} made using Debit Card.")


class UPI:
    def pay(self, amount):
        print(f"Payment of ₹{amount} made using UPI.")


class NetBanking:
    def pay(self, amount):
        print(f"Payment of ₹{amount} made using Net Banking.")


# Context Class
class PaymentProcessor:

    def __init__(self, payment_method):
        self.payment_method = payment_method

    def process_payment(self, amount):
        self.payment_method.pay(amount)


# Main Program

print("===== Payment Processing System =====")
print("1. Credit Card")
print("2. Debit Card")
print("3. UPI")
print("4. Net Banking")

choice = int(input("Enter your choice: "))
amount = float(input("Enter Amount: ₹"))

if choice == 1:
    payment = CreditCard()
elif choice == 2:
    payment = DebitCard()
elif choice == 3:
    payment = UPI()
elif choice == 4:
    payment = NetBanking()
else:
    print("Invalid Choice")
    exit()

processor = PaymentProcessor(payment)
processor.process_payment(amount)