import os
from pathlib import Path

import pandas as pd
import dataframe_image as dfi

from natsort import natsorted
from typing import List, Protocol, cast
from dataclasses import dataclass, field

from Shared.dataframe_styler import style_df
from Shared.settings import DataLoader
from Shared.decorators import time_func


class Data(Protocol):
    postcode_output_area_mapping = pd.DataFrame
    postcode_list = pd.DataFrame
    variable_files: List[pd.DataFrame]


@dataclass
class MissingData:
    postcodes_missing_oas: set[str] = field(default_factory=set)
    hidden_oas: set[str] = field(default_factory=set)


@dataclass
class FinalData:
    data: pd.DataFrame = field(default_factory=pd.DataFrame)
    multiindex_cols: List[str] = field(default_factory=list)


def format_columns(data: Data) -> Data:
    """
    Formats columns by, for example, removing spaces in a postcode column.

    :param data: Class of type Data that contains attributes postcode_output_area_mapping & postcode_list
    :return: Class of type Data
    """
    data.postcode_output_area_mapping['pcd_clean'] = data.postcode_output_area_mapping['pcd'].str.replace(" ", "",
                                                                                                          regex=True)
    data.postcode_list['Postcode_clean'] = data.postcode_list['Postcode'].str.replace(" ", "",
                                                                                      regex=True)

    data.variable_files = [df.rename(columns={'Output Areas': 'Output Area'}) for df in data.variable_files]

    return data


def save_output(working_df: pd.DataFrame, wide_census_df: pd.DataFrame) -> None:
    working_df.rename(columns={'oa21': 'Output area code'}, inplace=True)
    working_df.drop(columns=['Postcode_clean', 'pcd_clean'], inplace=True)
    working_df.to_csv('output/output_area_mapping.csv', index=False)
    wide_census_df.to_csv('output/table.csv', index=False)


def merge_dfs(data: Data) -> Data:
    data.postcode_list = data.postcode_list.merge(data.postcode_output_area_mapping[['pcd_clean', 'oa21']],
                                                  left_on='Postcode_clean',
                                                  right_on='pcd_clean', how='left')

    data.postcodes_missing_oas = data.postcode_list[data.postcode_list['oa21'].isna()]['Postcode'].to_list()

    return data


def clean_census_data(data: Data) -> Data:
    for i, df in enumerate(data.variable_files):
        # Filter out columns to remove any columns ending with 'Code'
        filtered_columns = [col for col in df.columns if not col.endswith('Code')]

        data.variable_files[i] = df[filtered_columns]

    return data


def combine_postcode_census_data(data: Data) -> tuple[FinalData, MissingData]:
    """


    :param data:
    :return:
    """
    wide_df_list = []
    missing_postcode_set = set()

    multi_level_cols = []
    for i, df in enumerate(data.variable_files):
        multi_level_cols.extend([df.columns[1]] * len(df.iloc[:, 1].unique()))

        long_df = df[df['Output Area'].isin(data.postcode_list['oa21'])]

        postcode_list = data.postcode_list.groupby('oa21')['Postcode'].apply(lambda x: ', '.join(x)).reset_index()

        long_df = long_df.merge(postcode_list[['oa21', 'Postcode']],
                                left_on='Output Area', right_on='oa21',
                                how='left')
        long_df = long_df.pivot(index=['Postcode', 'Output Area'], columns=df.columns[1], values='Observation')
        long_df.columns = natsorted(long_df.columns)
        wide_df_list.append(long_df)

        # Find any output areas that are missing from the census data, and save the corresponding postcodes to a set
        missing_postcode_set.update(
            postcode_list.loc[~postcode_list['oa21'].isin(df['Output Area']), 'Postcode'].to_list())

    wide_census_data = pd.concat(wide_df_list, axis=1)

    # Reset index to set Postcode and Output area as columns
    wide_census_data = wide_census_data.reset_index()

    # Create the MultiIndex from the existing columns and new levels
    multi_index = pd.MultiIndex.from_arrays([['', ''] + multi_level_cols, wide_census_data.columns])
    wide_census_data.columns = multi_index

    return FinalData(wide_census_data, multi_level_cols), MissingData(postcodes_missing_oas=missing_postcode_set)


@time_func
def main() -> None:
    # Load data and cast to Data protocol
    data = cast(Data, DataLoader(os.path.join(os.path.dirname(__file__), '.env')))

    data = format_columns(data)
    data = merge_dfs(data)
    data = clean_census_data(data)

    final_data, missing_data = combine_postcode_census_data(data)
    styled_df = style_df(final_data)

    Path("output").mkdir(exist_ok=True)
    dfi.export(styled_df, 'output/df_wide_styled.png')
    save_output(data.postcode_list, final_data.data)

    print("Converted postcodes to output area codes.")


if __name__ == '__main__':
    main()
