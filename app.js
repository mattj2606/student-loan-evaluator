document.getElementById('loanForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const loanType = document.getElementById('loanType').value;
    const interestRate = parseFloat(document.getElementById('interestRate').value) / 100 / 12;
    const repaymentPeriod = parseInt(document.getElementById('repaymentPeriod').value) * 12;
    const expectedSalary = parseFloat(document.getElementById('expectedSalary').value);
    const currentDebt = parseFloat(document.getElementById('currentDebt').value);
    const futureBorrowing = parseFloat(document.getElementById('futureBorrowing').value);
    
    const principal = currentDebt + futureBorrowing;
    const monthlyRepayment = (principal * interestRate * Math.pow((1 + interestRate), repaymentPeriod)) / (Math.pow((1 + interestRate), repaymentPeriod) - 1);
    const totalRepayment = monthlyRepayment * repaymentPeriod;
    const totalCost = totalRepayment - principal;
    
    const otherLoans = calculateOtherLoans(principal, repaymentPeriod);
    
    displayResults(loanType, monthlyRepayment, totalRepayment, totalCost, otherLoans);
  });
  
  function calculateOtherLoans(principal, repaymentPeriod) {
    const publicSubsidizedRate = 0.05 / 12; // Example rate
    const publicUnsubsidizedRate = 0.06 / 12; // Example rate
    
    const publicSubsidizedMonthly = (principal * publicSubsidizedRate * Math.pow((1 + publicSubsidizedRate), repaymentPeriod)) / (Math.pow((1 + publicSubsidizedRate), repaymentPeriod) - 1);
    const publicUnsubsidizedMonthly = (principal * publicUnsubsidizedRate * Math.pow((1 + publicUnsubsidizedRate), repaymentPeriod)) / (Math.pow((1 + publicUnsubsidizedRate), repaymentPeriod) - 1);
    
    return {
      publicSubsidized: {
        monthlyRepayment: publicSubsidizedMonthly,
        totalRepayment: publicSubsidizedMonthly * repaymentPeriod,
        totalCost: (publicSubsidizedMonthly * repaymentPeriod) - principal
      },
      publicUnsubsidized: {
        monthlyRepayment: publicUnsubsidizedMonthly,
        totalRepayment: publicUnsubsidizedMonthly * repaymentPeriod,
        totalCost: (publicUnsubsidizedMonthly * repaymentPeriod) - principal
      }
    };
  }
  
  function displayResults(loanType, monthlyRepayment, totalRepayment, totalCost, otherLoans) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
      <h2 class="text-xl font-bold">Results for ${loanType.replace('_', ' ')}:</h2>
      <p>Monthly Repayment: $${monthlyRepayment.toFixed(2)}</p>
      <p>Total Repayment: $${totalRepayment.toFixed(2)}</p>
      <p>Total Cost of Loan: $${totalCost.toFixed(2)}</p>
      <h2 class="text-xl font-bold mt-4">Comparative Analysis:</h2>
      <h3 class="text-lg font-bold">Public Subsidized Loan:</h3>
      <p>Monthly Repayment: $${otherLoans.publicSubsidized.monthlyRepayment.toFixed(2)}</p>
      <p>Total Repayment: $${otherLoans.publicSubsidized.totalRepayment.toFixed(2)}</p>
      <p>Total Cost of Loan: $${otherLoans.publicSubsidized.totalCost.toFixed(2)}</p>
      <h3 class="text-lg font-bold">Public Unsubsidized Loan:</h3>
      <p>Monthly Repayment: $${otherLoans.publicUnsubsidized.monthlyRepayment.toFixed(2)}</p>
      <p>Total Repayment: $${otherLoans.publicUnsubsidized.totalRepayment.toFixed(2)}</p>
      <p>Total Cost of Loan: $${otherLoans.publicUnsubsidized.totalCost.toFixed(2)}</p>
    `;
    resultsDiv.classList.remove('hidden');
  }
  