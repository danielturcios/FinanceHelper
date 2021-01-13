import payulator as pl

# frequency of payments
freq = 12
# how long it will take to pay off the loan (in years)
time = 5

# principal loan amount of first loan
l1_principal_amount = 7959.30
# interest rate of first loan
l1_interest_rate = 0.0505

l1_params = {
    'kind': 'amortized',
    'principal': l1_principal_amount,
    'interest_rate': l1_interest_rate,
    'compounding_freq': 'monthly',
    'payment_freq': 'monthly',
    'num_payments': freq*time
}

loan1 = pl.Loan(**l1_params)
print(loan1)
s1 = loan1.summarize()
print(s1)