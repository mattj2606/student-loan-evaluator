# Student Loan Evaluator

A comprehensive tool to help students evaluate their college financing options, expected debt burden, and post-graduation salary outcomes.

## Features

- **Loan Calculator**: Calculate monthly payments, total repayment amount, and total interest paid
- **Multiple Loan Support**: Add and manage multiple loans (private and federal)
- **Flexible Repayment Analysis**: 
  - Fix monthly payment and calculate payoff time
  - Fix payoff time and calculate required monthly payment
- **Income Analysis**: Evaluate loan burden against expected salary
- **Visual Indicators**: Color-coded results to show loan burden severity

## Getting Started

### Prerequisites

- Python 3.8+
- Flask

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/mattj2606/student-loan-evaluator.git
   cd student-loan-evaluator
   ```

2. Create and activate a virtual environment:
   ```
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Deployment

This application is designed to be deployed on Render. Follow these steps:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn app:app`
5. Deploy!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for the UI components
- Flask for the web framework 