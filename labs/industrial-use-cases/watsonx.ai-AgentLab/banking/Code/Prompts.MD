1. First we're going to try making an LLM call on a new standard without having any access to tools. Try the following prompt in AgentLab without any tools. 
`Summarise the changes in ASIC's enhanced Banking Code of Practice?`

2. Now we'll add the Google Tool and try the same prompt. You should see that it is now referencing the latest changes to the code of practice. 

3. What if we wanted to get details from a specific website, well Billie could use the webscraping tool. Try the prompt below, it will summarise the details from that specific website by crawling that page directly. 
`Summarise CommBank's LMI policy from here: https://www.commbank.com.au/home-loans/lenders-mortgage-insurance.html`

4. But Billie needs some more details, what if she had a specific document that she wanted to ground her answers in. Rather than using a site what if there was an internal policy. 

File: lenders_mortgage_insurance.pdf
Name: Lenders Mortgage Insurance
Description: The following document contains details about CommBank's lenders mortgage insurance policy. When it might apply, product disclosures, faqs and provides an overall guide.

`when would LMI apply?`
`what is the minimum deposit that would not require lmi?`

5. What if Billie, got a question from a customer on a loan product that they'd newly inherited. The customer has asked what is the APR on the following loan: $2,000 with a 5% interest rate and $200 in fees for two years. How might she go about calculating it. We could try adding a Python tool to perform calculations. 
`What are the monthly repayments on a $948,000 loan at an interest rate of 5.85% over 30 years.`

6. Now let's say that the Bank introduces a new wealth builder fee of $3000 over the life of the loan which gets added onto monthly payments, how could Billie factor this into her agent? This is where custom tools come in. 

<code>
def monthly_repayment(principal: float, interest_rate: float, period: int):
    interest_rate = interest_rate / 100
    return (
        principal
        * (interest_rate / 12 * (1 + interest_rate / 12) ** (period * 12))
        / ((1 + interest_rate / 12) ** (period * 12) - 1)
    ) + 3000 / 30

{
  "principal": {
    "title": "Principal loan amount",
    "description": "The total loan amount",
    "type": "number"
  },
  "interest_rate": {
    "title": "Yearly interest rate",
    "description": "The yearly interest rate to be charged",
    "type": "number"
  },
  "period": {
    "title": "Loan Period",
    "description": "The length of the loan in years.",
    "type": "integer"
  }
}
</code>





