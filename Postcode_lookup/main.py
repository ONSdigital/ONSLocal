import os
from pathlib import Path

import pandas as pd
import dataframe_image as dfi

from natsort import natsorted
from typing import List, cast
from dataclasses import dataclass, field, fields

from pandas import MultiIndex, DataFrame
from pandas.io.formats.style import Styler

from Shared.dataframe_styler import style_df
from Shared.settings import DataLoader
from Shared.decorators import time_func


@dataclass
class Data:
    postcode_output_area_mapping: DataFrame
    postcode_list: DataFrame
    variable_files: List[pd.DataFrame]


@dataclass
class MissingData:
    postcodes_missing_oas: set[str]
    suppressed_oas: set[str]


@dataclass
class FinalData:
    data: pd.DataFrame
    multiindex_cols: List[str]
    styled_df: Styler = field(default_factory=DataFrame)


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
    data.variable_files = [df.loc[:, ~df.columns.str.endswith('Code')] for df in data.variable_files]

    return data


def save_output(original_data: Data, final_data: FinalData, missing_data: MissingData) -> None:
    Path("output").mkdir(exist_ok=True)

    original_data.postcode_list.rename(columns={'oa21': 'Output area code'}, inplace=True)
    original_data.postcode_list.drop(columns=['Postcode_clean', 'pcd_clean'], inplace=True)
    original_data.postcode_list.to_csv('output/output_area_mapping.csv', index=False)

    dfi.export(final_data.styled_df, 'output/table.png')
    final_data.data.to_csv('output/table.csv', index=False)

    # Create the content for the text file
    content = ""

    # Iterate over the dataclass attributes
    for dataclass_field in fields(missing_data):
        # If the dataclass attribute contains data, save it into the content variable
        if getattr(missing_data, dataclass_field.name):
            content += f"{dataclass_field.name}: {', '.join(getattr(missing_data, dataclass_field.name))}\n"

    # Write the content to a text file if there is any content
    if content:
        with open('output/missing_data.txt', 'w') as file:
            file.write(content)

        print("Missing data found. A list of these postcodes has been saved in missing_data.txt")


def append_output_area_to_postcode_list(data: Data) -> Data:
    data.postcode_list = data.postcode_list.merge(data.postcode_output_area_mapping[['pcd_clean', 'oa21']],
                                                  left_on='Postcode_clean',
                                                  right_on='pcd_clean', how='left')

    return data


def combine_postcode_census_data(data: Data) -> pd.DataFrame:
    """

    :param data:
    :return:
    """

    joined_postcodes = group_postcodes(data)

    wide_df_list = []
    for i, df in enumerate(data.variable_files):
        # Merge the demographic information and the joined postcode list
        temp_df = df.merge(joined_postcodes[['oa21', 'Postcode']],
                           left_on='Output Area', right_on='oa21',
                           how='inner')

        # Convert to wide format
        temp_df = temp_df.pivot(index=['Postcode', 'Output Area'], columns=df.columns[1], values='Observation')

        # Sort columns
        temp_df.columns = natsorted(temp_df.columns)

        wide_df_list.append(temp_df)

    combined_data = pd.concat(wide_df_list, axis=1)

    # Reset index to set Postcode and Output area as columns
    combined_data = combined_data.reset_index()

    return combined_data


def group_postcodes(data: Data) -> DataFrame:
    """
    Combine postcodes in the same output area

    :param data:
    :return:
    """
    joined_postcodes = data.postcode_list.groupby('oa21')['Postcode'].apply(lambda x: ', '.join(x)).reset_index()

    return joined_postcodes


def create_multi_index(variable_files: List[DataFrame], combined_data: DataFrame) -> tuple[MultiIndex, list[str]]:
    multiindex_cols = []
    for i, df in enumerate(variable_files):
        # Create a list repeating the column name (such as Age) as many times as there are unique values in that column
        multiindex_cols.extend([df.columns[1]] * len(df.iloc[:, 1].unique()))

    # Create the MultiIndex from the existing columns and new levels
    multi_index = pd.MultiIndex.from_arrays([['', ''] + multiindex_cols, combined_data.columns])

    return multi_index, multiindex_cols


def create_final_data(data: Data) -> FinalData:
    combined_data = combine_postcode_census_data(data)

    multi_index, multiindex_cols = create_multi_index(data.variable_files, combined_data)
    combined_data.columns = multi_index

    final_data = FinalData(data=combined_data, multiindex_cols=multiindex_cols)
    final_data.styled_df = style_df(final_data)

    return final_data


def find_missing_data(data: Data) -> MissingData:
    # Find postcodes that do not have assigned output areas
    postcodes_missing_oas = set(data.postcode_list[data.postcode_list['oa21'].isna()]['Postcode'])

    # Find any output areas that are missing from the census data
    suppressed_data = set()
    for i, df in enumerate(data.variable_files):
        # Merge the demographic information and the joined postcode list
        merged_df = df.merge(data.postcode_list[['oa21', 'Postcode']],
                             left_on='Output Area', right_on='oa21',
                             how='right')

        non_matching_rows = merged_df[merged_df['Output Area'].isna()]['Postcode'].to_list()

        suppressed_data.update(non_matching_rows)

    return MissingData(postcodes_missing_oas=postcodes_missing_oas, suppressed_oas=suppressed_data)


@time_func
def main() -> None:
    # Load data and cast to Data dataclass
    data = cast(Data, DataLoader(os.path.join(os.path.dirname(__file__), '.env')))

    data = format_columns(data)
    data = append_output_area_to_postcode_list(data)

    final_data = create_final_data(data)
    missing_data = find_missing_data(data)

    save_output(data, final_data, missing_data)

    print("Converted postcodes to output area codes.")


if __name__ == '__main__':
    main()
