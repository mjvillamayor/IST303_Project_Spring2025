<<<<<<< HEAD
# Medication Management and Error Reduction System

## Product
The system is designed to significantly reduce medication errors in healthcare settings by effectively integrating real-time barcode scanning alerts related to prescription management, medication dispensements, and dangerous drug-drug interactions from the perspective of medical providers.

=======
# Application
- Medication Management and Error Reduction System
## Product
- The system is designed to significantly reduce medication errors in healthcare settings by effectively integrating real-time barcode scanning alerts related to prescription management, medication dispensements, and dangerous drug-drug interactions from the perspective of medical providers.
>>>>>>> 8ea69baf6411ad1e154769ad9d9d89a3619ee194
## Team Members
- Ben Morehead
- Jade Sleiman
- Mark Villamayor
- Millicent Wanyeki
<<<<<<< HEAD

## How to Run the Program

1. Install required dependencies:
   ```bash
   pip install flask flask-cors requests
   ```

2. Start the Flask application:
   ```bash
   python simple_app.py
   ```

3. Open your web browser and navigate to:
   http://127.0.0.1:5000

4. Enter medication names separated by commas (e.g., "aspirin, warfarin")
   and click "Check Interactions" to view potential drug interactions.

## How to Test It

1. Manual Testing:
   - Test with common medications like "aspirin, warfarin" or "lisinopril, spironolactone"
   - Test error handling with non-existent medications
   - Test with single medications and multiple medications

2. Automated Testing (to be implemented):
   - Run the test suite with: pytest tests/
   - Tests cover API endpoint functionality, error handling, and data processing

## How to Report Test Coverage

1. Install coverage tools:
   ```bash
   pip install pytest pytest-cov
   ```

2. Run tests with coverage:
   ```bash
   pytest --cov=. tests/
   ```

3. Generate HTML coverage report:
   ```bash
   pytest --cov=. --cov-report=html tests/
   ```

4. View the coverage report by opening htmlcov/index.html in your browser

## Three Most Important Things Learned about Software Development from this Application

1. **API Integration Complexity**: Integrating with external healthcare APIs requires careful error handling and data validation to ensure reliable medication information, especially when patient safety is at stake.

2. **User-Centered Design for Clinical Workflows**: Designing for healthcare providers requires balancing comprehensive information with simplicity and speed, as decisions made at the point of care directly impact patient outcomes.

3. **Importance of Robust Error Management**: In healthcare applications, graceful degradation and clear error messaging are critical - the system must provide useful information even when faced with incomplete data or API failures.
=======
## How to Run

## How to Test

## How to Report Test Coverage

## Three Most Important Things Learned about Software Development from this Application
- 
- 
- 
>>>>>>> 8ea69baf6411ad1e154769ad9d9d89a3619ee194
