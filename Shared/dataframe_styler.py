from typing import List, Protocol

import pandas as pd
from pandas.io.formats.style import Styler


class Data(Protocol):
    data: pd.DataFrame
    multiindex_cols: List[str]


def style_df(data: Data) -> Styler:
    style_list = [{'selector': '.level0', 'props': [('border-top', '2px solid black')]},
                  {'selector': '.level1', 'props': [('border-bottom', '2px solid black')]}]

    # Calculate where the changes are in the multi level column index
    change_indices = [i + 2 for i in range(1, len(data.multiindex_cols)) if data.multiindex_cols[i] !=
                      data.multiindex_cols[i - 1]]
    # Reverse list so new columns are added from the end backwards
    change_indices.reverse()

    for num in change_indices:
        data.data.insert(num, ' ', '')

    for i in range(data.data.shape[1] + 1):
        # Center all columns
        style_list.append({'selector': f'th.col{i}', 'props': [('text-align', 'center')]})

    added_columns = 0
    for i in range(len(set(data.multiindex_cols)) + len(change_indices)):
        # Add bottom borders to high level column headers
        style_list.append({'selector': f'.level0:nth-child({i + 2 + added_columns})',
                           'props': [('border-bottom', '2px solid black')]}, )

        if change_indices:
            added_columns += 1

    styled_df = data.data.style.set_table_styles(style_list).hide(axis='index')

    return styled_df
