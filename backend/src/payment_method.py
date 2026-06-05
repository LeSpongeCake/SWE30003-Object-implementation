class PaymentMethod:
	def pay(self):
		pass


class CardPayment(PaymentMethod):
	def pay(self) -> str:
		return "Paid with card."
	

class ApplePay(PaymentMethod):
	def pay(self) -> str:
		return "Paid with ApplePay."
	

class GooglePay(PaymentMethod):
	def pay(self) -> str:
		return "Paid with GooglePay."