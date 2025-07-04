def monthly_repayment(principal: float, interest_rate: float, period: int):
    interest_rate = interest_rate / 100
    return (
        principal
        * (interest_rate / 12 * (1 + interest_rate / 12) ** (period * 12))
        / ((1 + interest_rate / 12) ** (period * 12) - 1)
    ) + 3000 / 30


print(monthly_repayment(948000, 0.0585, 30))
