if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(data, data2, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    n_features = 10
    columns_to_keep = ["x" + str(i) for i in range(1, n_features+1)]
    # Specify your transformation logic here
    df_reference = pd.DataFrame(data)
#    df_reference = df_reference.drop(columns=['date', 'persona'])
    df_reference = df_reference[columns_to_keep]
    df_current = pd.DataFrame(data2)
#    df_current = df_current.drop(columns=['date', 'persona'])
    df_current = df_current[columns_to_keep]
    return {
        'reference': df_reference,
        'current': df_current
        }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
