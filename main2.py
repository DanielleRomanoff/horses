import csv_processing_functions as processor
import df_preprocessing as cleaner
import database_functions
import file_definitions

import os
import pathlib
import re
import pandas as pd

name_files = {
    '1': file_definitions.file_1_columns,
    '2': file_definitions.file_2_columns,
    '3': file_definitions.file_3_columns,
    '4': file_definitions.file_4_columns,
    '5': file_definitions.file_5_columns,
    '6': file_definitions.file_6_columns,
    'drf': file_definitions.past_perf_columns,
}

columns_to_delete = {
    '1': [s for s in name_files['1'] if 'reserved' in s],
    '2': [s for s in name_files['2'] if 'reserved' in s],
    '3': [s for s in name_files['3'] if 'reserved' in s],
    '4': [s for s in name_files['4'] if 'reserved' in s],
    '5': [s for s in name_files['5'] if 'reserved' in s],
    '6': [s for s in name_files['6'] if 'reserved' in s],
    'drf': [s for s in name_files['drf'] if 'reserved' in s]
}

def main(file_to_process='None', path='data'):
    if file_to_process is None:
        file_paths = []
        file_paths.append(pathlib.Path(path, file_to_process))
    else:
        file_paths = [pathlib.Path(path, file) for file in os.listdir(path)]
        file_paths = [file for file in file_paths if file.is_file()]
    db = database_functions.DbHandler()
    db.initialize_db()
    i = 1
    for file in file_paths:
        print('Processing {} ({} of {})'.format(file, i, len(file_paths)))
        try:
            table_data, extension = process_csv_file(file)
        except FileNotFoundError as e:
            print('There was a problem finding the file {}:'.format(file))
            print('\t', e)
            continue
        column_dtypes = table_data.dtypes
        db.initialize_table(extension+'_data', table_data, column_dtypes)
        db.add_to_table(extension+'_data', table_data, column_dtypes)
        i += 1
        processed_dir = file.parent / (extension+'_file')
        processed_dir.mkdir(exist_ok = True)
        print('Moving {} to {}\n'.format(file.name, processed_dir))
        file.rename(processed_dir / file.name)



def process_csv_file(file):
    extension = re.search(r'(?<=\.).+$', str(file))[0]
    #   Read the data in and run it through the cleaner
    table_data = pd.read_csv(file, header=None, names=name_files[str(extension)])
    table_data = cleaner.tidy_it_up(table_data, extension)
    #   Strip out unused columns
    for column in columns_to_delete[str(extension)]:
        del table_data[column]
    return table_data, extension