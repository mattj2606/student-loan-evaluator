# Student Loan Evaluator

## Objective

The Student Loan Evaluator aims to assist users in managing multiple student loans by providing a comprehensive overview, repayment strategies, and AI-driven insights. Users can input details about their loans, set repayment preferences, and get recommendations on how to manage their repayments effectively.

## Features

### Loan Information Entry
- **Inputs:**
  - Year the loan was taken out
  - Loan Type (Subsidized, Unsubsidized, Private)
  - Loan Amount
  - Interest Rate (automatically populated for federal loans based on year and loan type)
- **Functionality:**
  - Add or remove multiple loans dynamically
  - Validations to ensure correct input formats
  - Automatic population of interest rates for federal loans based on the selected year and loan type

### Repayment Preferences
- **Inputs:**
  - Total Repayment Period (Slider)
  - Loan Prioritization Method (Dropdown/Radio Buttons)
- **Functionality:**
  - Select the desired repayment period using a slider
  - Choose the loan prioritization method (e.g., highest interest rate first, smallest balance first)

### Analysis and AI Insights (Future Update)
- **Features:**
  - Calculate if the repayment amount is feasible based on the user's salary
  - Determine if the repayment duration is too long or too short
  - Provide AI-driven insights on the repayment strategy
  - Display potential savings and costs over different repayment strategies

## Current Status

### Completed
- Basic UI for entering loan details and repayment preferences
- Functionality to add and remove loan rows dynamically
- Basic validation for loan inputs

### To Do
- Automatically populate interest rates for federal loans based on the selected year and loan type (Currently not functional)
- Display source note for interest rates
- Add functionality to adjust repayment strategy
- Implement AI-driven financial advice
- Improve overall UI/UX

## Future Updates
- Implement backend calculations for total cost of loans, monthly repayment amount, and total repayment amount
- Integrate machine learning models for personalized financial advice
- Enhance the user interface for better user experience
- Add functionality to save and load loan data

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/mattj2606/student-loan-evaluator.git
