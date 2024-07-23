// Fetch public loan rates from the JSON file
let publicLoanRates = [];
fetch('public_loan_rates.json')
  .then(response => response.json())
  .then(data => {
    publicLoanRates = data.rates;
    console.log('Public loan rates loaded:', publicLoanRates); // Debugging statement
  });

// Function to get interest rate based on loan type and year
function getInterestRate(loanType, year) {
  const rate = publicLoanRates.find(rate => rate.year == year);
  if (!rate) return null;

  switch (loanType) {
    case 'subsidized':
      return rate.subsidized_undergraduate;
    case 'unsubsidized':
      return rate.unsubsidized_undergraduate;
    default:
      return null;
  }
}

// Populate year dropdown with years from 2006 to 2024
function populateYearDropdown() {
  const years = [];
  for (let year = 2006; year <= 2024; year++) {
    years.push(year);
  }
  const yearDropdownOptions = years.map(year => `<option value="${year}">${year}</option>`).join('');
  return yearDropdownOptions;
}

const yearDropdownOptions = populateYearDropdown();
console.log('Year dropdown options:', yearDropdownOptions); // Debugging statement

// Add row for loan inputs
function addLoanRow(container, loanTypeOptions, yearDropdownOptions) {
  const newLoanDiv = document.createElement('div');
  newLoanDiv.className = 'loan flex flex-row items-center mb-2 p-2 border-b space-x-4';
  newLoanDiv.innerHTML = `
    <div class="w-1/12 flex items-center justify-center">
      <button type="button" class="removeLoan">-</button>
    </div>
    <div class="w-2/12">
      <input type="number" list="yearList" class="loanYear w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Year" min="2006" max="2024">
      <datalist id="yearList">
        ${yearDropdownOptions}
      </datalist>
    </div>
    <div class="w-3/12">
      <select class="loanType w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        ${loanTypeOptions}
      </select>
    </div>
    <div class="w-3/12">
      <input type="number" class="loanAmount w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" step="0.01" min="0" placeholder="Loan Amount">
    </div>
    <div class="w-3/12">
      <input type="number" class="interestRate w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" step="0.01" placeholder="Interest Rate" readonly>
    </div>
  `;

  container.appendChild(newLoanDiv);

  // Event listener to update interest rate based on loan type and year
  newLoanDiv.querySelector('.loanYear').addEventListener('input', function() {
    const loanYear = this.value;
    const loanType = newLoanDiv.querySelector('.loanType').value;
    const interestRateInput = newLoanDiv.querySelector('.interestRate');

    const interestRate = getInterestRate(loanType, loanYear);
    interestRateInput.value = interestRate !== null ? interestRate : '';
    interestRateInput.readOnly = interestRate !== null;
    
    const sourceNote = document.getElementById('sourceNote');
    if (interestRate !== null) {
      sourceNote.classList.remove('hidden');
    }
  });

  newLoanDiv.querySelector('.loanType').addEventListener('change', function() {
    const loanYear = newLoanDiv.querySelector('.loanYear').value;
    const loanType = this.value;
    const interestRateInput = newLoanDiv.querySelector('.interestRate');

    const interestRate = getInterestRate(loanType, loanYear);
    interestRateInput.value = interestRate !== null ? interestRate : '';
    interestRateInput.readOnly = interestRate !== null;
    
    const sourceNote = document.getElementById('sourceNote');
    if (interestRate !== null) {
      sourceNote.classList.remove('hidden');
    }
  });

  // Allow editing interest rate if clicked
  newLoanDiv.querySelector('.interestRate').addEventListener('click', function() {
    this.readOnly = false;
  });

  // Ensure only numbers are allowed in loan amount and format on paste
  newLoanDiv.querySelector('.loanAmount').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');
  });
  newLoanDiv.querySelector('.loanAmount').addEventListener('paste', function(event) {
    event.preventDefault();
    const paste = (event.clipboardData || window.clipboardData).getData('text');
    this.value = paste.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');
  });

  // Event listener to remove loan row
  newLoanDiv.querySelector('.removeLoan').addEventListener('click', function() {
    newLoanDiv.remove();
  });
}

// Event listener for adding loans
document.getElementById('addLoan').addEventListener('click', function() {
  const loansContainer = document.getElementById('loansContainer');
  const loanTypeOptions = `
    <option value="subsidized">Subsidized</option>
    <option value="unsubsidized">Unsubsidized</option>
    <option value="private">Private</option>
  `;
  addLoanRow(loansContainer, loanTypeOptions, yearDropdownOptions);
});

// Event listener to update the repayment period value
document.getElementById('repaymentPeriod').addEventListener('input', function() {
  document.getElementById('repaymentPeriodValue').innerText = this.value;
});

// Event listener to handle the form submission
document.getElementById('loanForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  // Implement calculations and display results here.
});
