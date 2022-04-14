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

# from decimal import Decimal

# def first_taxable():
#     if 11100000 <= 88000:
#         return 0

# fir = 280000
# def second_taxable() -> Decimal:
#     if 11100 - 300000 < 300000 or 1536448 >= 300000:
#         return (300000 * 7/100)

        
# def third_taxable():
#     if (1536448-600000) <= 300000:
#         return(300000 * 11/100)
#     elif (1536448)

        
# def fourth_taxable():
#     if (1536448-600000)  >= 500000:
#         return(500000 * 15/100)


# def fifth_taxable():    
#     if (1536448-1100000) <= 500000:
#         return((1536448-1100000) * 19/100)
        
        
# def payee_logic():
#     if 1624000 <= 88000:
#         return first_taxable()
#     elif 1624000 <= 300000:
#         return second_taxable()
#     elif 1624000 > 300000:
#         return second_taxable() + third_taxable()
#     elif 1624000 >600000:
#         return second_taxable() + third_taxable() + fourth_taxable()
#     elif 1624000 >1100000:
#         return second_taxable() + third_taxable() + fourth_taxable() + fifth_taxable()

# print(third_taxable())
# print(second_taxable())
# print(fourth_taxable())
# print(fifth_taxable())

import datetime
from dateutil.relativedelta import relativedelta

def initial_date(request, months=12):
    #  gets the initial last three months or the session date
    date_now = datetime.datetime.today()
    current_year = f'01/01/{datetime.date.today().year} - 12/31/{datetime.date.today().year}'
    date_range = request.GET.get('date_range', current_year)
    date_start, date_end = None, None

    if date_range:
        try:
            date_range = date_range.split('-')
            date_range[0] = date_range[0].replace(' ','')
            date_range[1] = date_range[1].replace(' ','')
            date_start = datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
            date_end = datetime.datetime.strptime(date_range[1],'%m/%d/%Y')
        except:
            print('except hitted')
            date_three_months_ago = date_now - relativedelta(months=months)
            date_start = date_three_months_ago
            date_end = date_now
            date_range = '%s - %s' % (str(date_three_months_ago).split(' ')[0].replace('-','/'),str(date_now).split(' ')[0].replace('-','/'))
            request.session['date_range'] = '%s - %s'%(str(date_three_months_ago).split(' ')[0].replace('-','/'),str(date_now).split(' ')[0].replace('-','/'))
    return [date_start, date_end, date_range]




""" I found the solution. As I had expected, it was a very trivial overlook. 
Just including subject as a parameter into the function allowed its use in the Entry model for querying purposes. 
The working function is depicted below.
 """
def get_obj_orlist(request, subject):
model = Entry
try:
    entry = Entry.objects.get(subject=subject)
except Entry.DoesNotExist:
    entries = Entry.objects.filter(subject__icontains=subject)
    return render(request, 'wikiencyc/searchencyc.html', {'entries':entries,'searchtoken':subject} )
return redirect(entry)