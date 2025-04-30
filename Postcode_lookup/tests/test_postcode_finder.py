import pytest
import pandas as pd
from typing import List
from Postcode_lookup.main import format_columns, append_output_area_to_postcode_list, combine_postcode_census_data, \
    MissingData, group_postcodes, create_multi_index, find_missing_data


class MockData:
    def __init__(self):
        self.postcode_output_area_mapping = pd.DataFrame({
            'pcd': ['AB1 0AA', 'AB1 0AB', 'AB1 0AC', 'AB1 0AD'],
            'oa21': ['E01', 'E02', 'E03', 'E03']
        })
        self.postcode_list = pd.DataFrame({
            'Postcode': ['AB1 0AA', 'AB1 0AB', 'AB1 0AC', 'AB1 0AD', 'ZZZ ZZZ']
        })
        self.variable_files = [
            pd.DataFrame({
                'Output Areas': ['E01', 'E02'],
                'Observation': [100, 200]
            })
        ]


@pytest.fixture(scope="module")
def mock_data() -> MockData:
    return MockData()


def test_format_columns(mock_data: MockData) -> None:
    mock_data = format_columns(mock_data)

    assert 'pcd_clean' in mock_data.postcode_output_area_mapping.columns
    assert 'Postcode_clean' in mock_data.postcode_list.columns
    assert mock_data.postcode_output_area_mapping['pcd_clean'].iloc[0] == 'AB10AA'
    assert mock_data.postcode_list['Postcode_clean'].iloc[0] == 'AB10AA'


def test_merge_dfs(mock_data: MockData) -> None:
    mock_data = append_output_area_to_postcode_list(mock_data)

    postcode_list = mock_data.postcode_list

    # Check if 'AB1 0AA' has 'E01' and 'AB10AB' has 'E02'
    check_1 = postcode_list[(postcode_list['Postcode'] == 'AB1 0AA') & (postcode_list['oa21'] == 'E01')].shape[0] > 0
    check_2 = postcode_list[(postcode_list['Postcode_clean'] == 'AB10AB') & (postcode_list['oa21'] == 'E02')].shape[
                  0] > 0

    # Check the checks
    assert check_1, "AB1 0AA does not have E01"
    assert check_2, "AB10AB does not have E02"


def test_group_postcodes(mock_data: MockData) -> None:
    joined_postcodes = group_postcodes(mock_data)

    assert joined_postcodes.loc[joined_postcodes['oa21'] == 'E01']['Postcode'].to_list() == ['AB1 0AA']
    assert joined_postcodes.loc[joined_postcodes['oa21'] == 'E03']['Postcode'].to_list() == ['AB1 0AC, AB1 0AD']


def test_create_multi_index(mock_data: MockData) -> None:
    combined_data = combine_postcode_census_data(mock_data)
    multi_index, multiindex_cols = create_multi_index(mock_data.variable_files, combined_data)

    assert multi_index.equals(pd.MultiIndex.from_tuples([('', 'Postcode'), ('', 'Output Area'),
                                                         ('Observation', 100), ('Observation', 200)]))
    assert multiindex_cols == ['Observation', 'Observation']


def test_find_missing_data(mock_data: MockData) -> None:
    missing_data = find_missing_data(mock_data)

    assert isinstance(missing_data, MissingData)
    assert missing_data.postcodes_missing_oas == {'ZZZ ZZZ'}
    assert missing_data.suppressed_oas == {'AB1 0AD', 'AB1 0AC'}
