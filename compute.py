# from datetime import datetime

# date = datetime.today().strftime("%Y-%m")

#class TaxCompute:

#     def __init__(self,gross):
#         self.gross = gross

#     def get_housing(self, amount):

#         housing = 0.15 * amount
#         return f"Your Housing allowance is #{housing} for the Month"
    
#     def get_transport(self) -> float:

#         transport = 0.15 * self.gross
#         return f"Your Transport allowance is #{transport} for the Month"

#     def get_basic(self, amount, housing, transport) -> int:
#         basic = self.gross - housing - transport
#         return f"Your Basic allowance is #{basic} for the Month"

#     # def get_pension_8_percent(self, percentage) -> float:
#     #     """ 
#     #         Compute Pension contribution for staff at 8% of basic salary

#     #      """
        
#     #     percent = percentage / 100
#     #     tax =  * percent
#         return f"your pension contribution is #{tax} for the Month of {date}"

#     def get_payee_amount(self):
#         """ 
#         Compute Payee Income tax deductable in accordance with the financial act
        
#          """
#         payee = 0
#         if self.basic <= 299999:
#             rate = 0.07
#             payee = rate * self.basic
#             return f"your PAYEE for the Month of {date} is #{payee}"
#         elif self.basic >=30000:
#             rate = 0.12
#             payee = rate * self.basic
#             return f"your PAYEE for the Month of {date} is #{payee}"
#         return payee

# # tax_1 = TaxCompute(50000,10000,10000)

# # print(str(tax_1))
# # print(tax_1.basic)
# # # print(tax_1.get_housing())

# # print(tax_1.get_pension_8_percent(8))
# # print(tax_1.get_payee_amount())
# # # print(tax_1.__dir__())
# # print(tax_1.__str__) 

# gross= 2000000
# twe_percent = 0.2*gross
# if 0.01*gross > 200000:
#     print(0.01*gross+twe_percent)

# else:
#     print(200000+twe_percent)

# tw = 30000

# basic = tw * 40/100
# housing = tw * 10/100
# trans = tw * 10/100

# pension = basic + housing+trans * 8/100


# print(basic)
# print(housing)
# print(trans)
# print(pension)



