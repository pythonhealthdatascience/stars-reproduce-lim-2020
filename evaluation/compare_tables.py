import pandas as pd


def view_tables(paper_path, model_path):
    '''
    Preview table (created function as need to sort columns so they're in the
    same order between the original and reproduction table when viewing).

    Then describe the absolute difference in values between the tables.

    Parameters:
    -----------
    paper_path : string
        Path to CSV file with result from model
    model_path : string
        Path to CSV file with result from model
    '''
    # Import dataframes
    paper_tab = pd.read_csv(paper_path)
    model_tab = pd.read_csv(model_path)

    # Get columns from paper, and use those to order and sort rows
    cols = paper_tab.columns.to_list()

    # Sort and preview both dataframes
    text = ['Preview of original', 'Preview of reproduction']
    i=0
    for df in [paper_tab, model_tab]:
        # Sort columns
        df = df[cols]
        # Sort rows
        df = df.sort_values(by=cols)
        # View first ten rows of dataframe
        display(text[i])
        display(df.head(10))
        i += 1

    # Merge the dataframes
    comp = pd.merge(
        model_tab.rename(columns={'prop_infected': 'prop_infected_model'}),
        paper_tab.rename(columns={'prop_infected': 'prop_infected_paper'}))

    # Calculate difference
    comp['diff'] = abs(comp['prop_infected_model'] -
                       comp['prop_infected_paper'])

    # Display descriptive statistics for that difference
    display('Absolute differences in proportion infected between tables')
    display(comp['diff'].describe())