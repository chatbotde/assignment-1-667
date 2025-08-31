# Flight Simulation Test Suite

This folder contains comprehensive tests for your flight simulation system, allowing you to test everything working together and identify areas for improvement.

## Test Files

### `test_components.py`
Tests individual components in isolation:
- Atmosphere module
- Airfoil module  
- Rotor module
- Inflow module

### `test_main.py`
Integration tests for the complete flight simulation:
- Basic integration of all components
- Rotor performance at different conditions
- End-to-end simulation runs

### `test_mission_integration.py`
Tests integration between flight sim and mission planner:
- Flight sim + mission planner compatibility
- Performance scenarios (hover, forward flight, high altitude)

### `run_all_tests.py`
Master test runner that executes all tests and provides a summary.

## How to Run Tests

### Run All Tests
```bash
python test_integration/run_all_tests.py
```

### Run Individual Test Files
```bash
python test_integration/test_components.py
python test_integration/test_main.py
python test_integration/test_mission_integration.py
```

## What These Tests Help You With

1. **Verify Integration**: Ensure all your flight sim components work together
2. **Identify Issues**: Catch problems before they affect your main simulation
3. **Performance Testing**: Test different flight scenarios and conditions
4. **Mission Planning**: Verify compatibility with your mission planner
5. **Continuous Improvement**: Easy way to test changes and improvements

## Expected Output

- ✓ Green checkmarks indicate passing tests
- ✗ Red X marks indicate failing tests
- Detailed error messages help you fix issues

## Next Steps

After running tests:
1. Fix any failing components
2. Add more test scenarios as needed
3. Integrate with mission planner
4. Optimize performance based on test results

## Adding New Tests

To add new tests:
1. Create new test functions in existing files
2. Or create new test files following the naming pattern `test_*.py`
3. Update `run_all_tests.py` to include new test files