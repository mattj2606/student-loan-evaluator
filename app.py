from flask import Flask, render_template, request, jsonify
import math
import json
import os

app = Flask(__name__)

# Load data files
def load_json_data(filename):
    try:
        with open(os.path.join('data', filename), 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": f"Could not load {filename}"}

# Load majors and schools data
majors_data = load_json_data('majors.json')
schools_data = load_json_data('schools.json')

def calculate_loan_payment(principal, annual_rate, years):
    """Calculate monthly loan payment using the loan amortization formula."""
    monthly_rate = annual_rate / 12 / 100
    num_payments = years * 12
    
    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - principal
    
    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_payment': round(total_payment, 2),
        'total_interest': round(total_interest, 2),
        'years': years,
        'months': 0  # Will be calculated in the frontend
    }

def calculate_payoff_time(principal, annual_rate, monthly_payment):
    """Calculate how long it will take to pay off a loan with a fixed monthly payment."""
    monthly_rate = annual_rate / 12 / 100
    
    if monthly_rate == 0:
        # If there's no interest, simply divide principal by monthly payment
        num_payments = math.ceil(principal / monthly_payment)
        years = num_payments / 12
    else:
        # Use the loan amortization formula solved for time
        # t = log(1 + (P*r)/M) / log(1 + r) where:
        # P = principal, r = monthly rate, M = monthly payment
        try:
            num_payments = math.log(1 + (principal * monthly_rate) / monthly_payment) / math.log(1 + monthly_rate)
            years = num_payments / 12
        except (ValueError, ZeroDivisionError):
            # Handle edge cases
            return {'error': 'Invalid input values or payment too low to ever pay off the loan'}
    
    total_payment = monthly_payment * math.ceil(num_payments)
    total_interest = total_payment - principal
    
    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_payment': round(total_payment, 2),
        'total_interest': round(total_interest, 2),
        'years': round(years, 2),
        'months': round((years % 1) * 12, 0)  # Calculate remaining months
    }

def calculate_loan_burden(monthly_payment, annual_salary):
    """Calculate loan burden as a percentage of monthly income."""
    if annual_salary <= 0:
        return {
            'burden_percentage': 0,
            'category': 'unknown'
        }
        
    monthly_salary = annual_salary / 12
    burden_percentage = (monthly_payment / monthly_salary) * 100
    
    # Determine burden category
    if burden_percentage < 8:
        category = 'green'
    elif burden_percentage < 15:
        category = 'yellow'
    else:
        category = 'red'
    
    return {
        'burden_percentage': round(burden_percentage, 2),
        'category': category
    }

def calculate_minimum_salary(monthly_payment):
    """Calculate the minimum annual salary needed to keep loan burden under 8%."""
    if monthly_payment <= 0:
        return 0
        
    # To keep burden under 8%, monthly payment should be less than 8% of monthly salary
    # So monthly salary = monthly_payment / 0.08
    monthly_salary = monthly_payment / 0.08
    annual_salary = monthly_salary * 12
    
    return round(annual_salary, 2)

def calculate_education_cost(school_id, is_in_state, years, grants=0):
    """Calculate the total cost of education."""
    if school_id not in [school['id'] for school in schools_data.get('schools', [])]:
        return {"error": "School not found"}
        
    school = next((s for s in schools_data.get('schools', []) if s['id'] == school_id), None)
    
    if not school:
        return {"error": "School not found"}
        
    tuition = school['in_state_tuition'] if is_in_state else school['out_of_state_tuition']
    room_and_board = school['room_and_board']
    fees = school['fees']
    
    annual_cost = tuition + room_and_board + fees
    total_cost = annual_cost * years
    out_of_pocket = max(0, total_cost - grants)
    
    return {
        'annual_cost': round(annual_cost, 2),
        'total_cost': round(total_cost, 2),
        'out_of_pocket': round(out_of_pocket, 2),
        'grants': round(grants, 2)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/majors', methods=['GET'])
def get_majors():
    return jsonify(majors_data)

@app.route('/api/schools', methods=['GET'])
def get_schools():
    return jsonify(schools_data)

@app.route('/api/major/<major_id>', methods=['GET'])
def get_major(major_id):
    major = next((m for m in majors_data.get('majors', []) if m['id'] == major_id), None)
    if major:
        return jsonify(major)
    return jsonify({"error": "Major not found"}), 404

@app.route('/api/school/<school_id>', methods=['GET'])
def get_school(school_id):
    school = next((s for s in schools_data.get('schools', []) if s['id'] == school_id), None)
    if school:
        return jsonify(school)
    return jsonify({"error": "School not found"}), 404

@app.route('/api/calculate_education_cost', methods=['POST'])
def api_calculate_education_cost():
    try:
        data = request.get_json()
        school_id = data.get('school_id')
        is_in_state = data.get('is_in_state', True)
        years = float(data.get('years', 4))
        grants = float(data.get('grants', 0))
        
        result = calculate_education_cost(school_id, is_in_state, years, grants)
        
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify(result)
        
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input values'}), 400

@app.route('/api/calculate_minimum_salary', methods=['POST'])
def api_calculate_minimum_salary():
    try:
        data = request.get_json()
        monthly_payment = float(data.get('monthly_payment', 0))
        
        minimum_salary = calculate_minimum_salary(monthly_payment)
        
        return jsonify({
            'minimum_salary': minimum_salary
        })
        
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input values'}), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        calculation_type = data.get('calculation_type', 'payment')
        
        if calculation_type == 'payment':
            # Calculate payment based on term
            principal = float(data.get('loan_amount', 0))
            annual_rate = float(data.get('interest_rate', 0))
            years = float(data.get('loan_term', 0))
            
            if principal <= 0 or annual_rate < 0 or years <= 0:
                return jsonify({'error': 'All values must be greater than 0'}), 400
                
            result = calculate_loan_payment(principal, annual_rate, years)
            
        elif calculation_type == 'term':
            # Calculate term based on payment
            principal = float(data.get('loan_amount', 0))
            annual_rate = float(data.get('interest_rate', 0))
            monthly_payment = float(data.get('monthly_payment', 0))
            
            if principal <= 0 or annual_rate < 0 or monthly_payment <= 0:
                return jsonify({'error': 'All values must be greater than 0'}), 400
                
            result = calculate_payoff_time(principal, annual_rate, monthly_payment)
            
            if 'error' in result:
                return jsonify(result), 400
        
        # Add income analysis if salary is provided
        annual_salary = data.get('annual_salary')
        if annual_salary and annual_salary > 0:
            burden = calculate_loan_burden(result['monthly_payment'], float(annual_salary))
            result.update(burden)
            
            # Calculate minimum salary needed
            minimum_salary = calculate_minimum_salary(result['monthly_payment'])
            result['minimum_salary'] = minimum_salary
            
        return jsonify(result)
        
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input values'}), 400

@app.route('/calculate_multiple', methods=['POST'])
def calculate_multiple():
    try:
        data = request.get_json()
        loans = data.get('loans', [])
        annual_salary = float(data.get('annual_salary', 0))
        
        if not loans:
            return jsonify({'error': 'No loans provided'}), 400
            
        total_monthly_payment = 0
        total_principal = 0
        total_interest = 0
        max_years = 0
        max_months = 0
        
        for loan in loans:
            principal = float(loan.get('loan_amount', 0))
            annual_rate = float(loan.get('interest_rate', 0))
            years = float(loan.get('loan_term', 0))
            
            if principal <= 0 or annual_rate < 0 or years <= 0:
                return jsonify({'error': 'All loan values must be greater than 0'}), 400
                
            result = calculate_loan_payment(principal, annual_rate, years)
            
            total_monthly_payment += result['monthly_payment']
            total_principal += principal
            total_interest += result['total_interest']
            
            # Track the longest loan term
            if result['years'] > max_years:
                max_years = result['years']
                max_months = result.get('months', 0)
            elif result['years'] == max_years and result.get('months', 0) > max_months:
                max_months = result.get('months', 0)
        
        result = {
            'total_monthly_payment': round(total_monthly_payment, 2),
            'total_principal': round(total_principal, 2),
            'total_interest': round(total_interest, 2),
            'max_years': round(max_years, 2),
            'max_months': round(max_months, 0)
        }
        
        # Add income analysis if salary is provided
        if annual_salary > 0:
            burden = calculate_loan_burden(total_monthly_payment, annual_salary)
            result.update(burden)
            
            # Calculate minimum salary needed
            minimum_salary = calculate_minimum_salary(total_monthly_payment)
            result['minimum_salary'] = minimum_salary
            
        return jsonify(result)
        
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input values'}), 400

if __name__ == '__main__':
    app.run(debug=True) 