'''
Model testing

This module contains tests to confirm whether the simulation model is
producing consistent results. To minimise the run time of the tests, only some
of the model scenarios are included as tests.
'''

import pandas as pd
from pathlib import Path
import pytest
from scripts import model


# Name of folder with expected results
EXP_FOLDER = 'exp_results'

# Parameters for different runs of the model
parameters = [
    {
        'shift_day': [1],
        'rest_day': False,
        'filename': 'output_base15_norest.csv'
    },
    {
        'secondary_attack_rate': 0.15*0.09,
        'filename': 'output_base15_n95mask.csv'
    }
]


# Create fixture with path to folder with expected results
# (Fixtures can be used to provide information to tests)
@pytest.fixture
def exp_folder():
    return EXP_FOLDER


# Run this function as separate tests on each of the files
# Use 'filename' from each dictionary as the ID for that run
@pytest.mark.parametrize('param', parameters,
                         ids=[d['filename'] for d in parameters])
def test_equal_df(param, exp_folder):
    '''
    Test that results are consistent with the expected results (which are
    from the computational reproducibility assessment).

    Parameters:
    -----------
    param : list
        List of dictionaries containing parameters for model and filename that
        contains expected results
    exp_folder : fixture
        Fixture providing path to expected results
    '''
    # Get the model inputs (i.e. drop filename from dict)
    inputs = {k: param[k] for k in set(list(param.keys())) - {'filename'}}

    # Run model (with ** to enable it to take dictionary as input)
    test_result = model.run_scenarios(**inputs)

    # Set 'prop_infected' to float (as that's what save and import csv will do)
    test_result['prop_infected'] = test_result['prop_infected'].astype(float)

    # Import expected result
    exp_result = pd.read_csv(
        Path(__file__).parent.joinpath(exp_folder, param['filename']))

    # Check that the dataframes are equal
    pd.testing.assert_frame_equal(test_result, exp_result)
