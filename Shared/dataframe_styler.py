from typing import List
from pandas import DataFrame
from pandas.io.formats.style import Styler


def style_df(df: DataFrame, multiindex_cols: List) -> Styler:
    style_list = [{'selector': '.level0', 'props': [('border-top', '2px solid black')]},
                  {'selector': '.level1', 'props': [('border-bottom', '2px solid black')]}]

    # Calculate where the changes are in the multi level column index
    change_indices = [i + 2 for i in range(1, len(multiindex_cols)) if multiindex_cols[i] != multiindex_cols[i - 1]]
    # Reverse list so new columns are added from the end backwards
    change_indices.reverse()

    for num in change_indices:
        df.insert(num, ' ', '')

    for i in range(df.shape[1] + 1):
        # Center all columns
        style_list.append({'selector': f'th.col{i}', 'props': [('text-align', 'center')]})

    added_columns = 0
    for i in range(len(set(multiindex_cols)) + len(change_indices)):
        # Add bottom borders to high level column headers
        style_list.append({'selector': f'.level0:nth-child({i + 2 + added_columns})',
                           'props': [('border-bottom', '2px solid black')]}, )

        if change_indices:
            added_columns += 1

    styled_df = df.style.set_table_styles(style_list).hide(axis='index')

    return styled_df
