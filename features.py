from parse_conditions_for_restrictions import ClassParser

import numpy as np
import re
from datetime import datetime
from dateutil import relativedelta


def is_blank(value):
    if value is None or value == 'NULL' or (isinstance(value, np.float) and np.isnan(value)):
        return True
    else:
        return False


def parse_conditions(condition_string):
    race_info = {
        'cond_race_class': 'NULL',
        'purse_string': 'NULL',
        'purse': 'NULL',
        'race_conditions': 'NULL',
        'weight_info': 'NULL',
        'standard_weight': 'NULL',
        'three_yo_weight': 'NULL',
        'cond_rail_distance': 'NULL',
        'weight_allowance_0_amt': 'NULL',
        'weight_allowance_0_condition': 'NULL',
        'weight_allowance_1_amt': 'NULL',
        'weight_allowance_1_condition': 'NULL',
        'weight_allowance_2_amt': 'NULL',
        'weight_allowance_2_condition': 'NULL',
        'weight_allowance_3_amt': 'NULL',
        'weight_allowance_3_condition': 'NULL',
        'cond_left_on_string': 'NULL',
    }

    # Race class
    try:
        race_class = re.match(r'[\w. ]+(?=\. )', condition_string)
        race_info['cond_race_class'] = race_class.group(0).strip()
        condition_string = condition_string[:race_class.regs[0][0]] + \
                           condition_string[race_class.regs[0][1]:]
        condition_string = condition_string[2:]
    except AttributeError:
        pass

    # Race purse info
    try:
        purse_data = re.match('Purse \$([\d;]+) (\(.+?\) )?', condition_string)
        all_purse_data = re.sub(';', '', purse_data.group(0))
        race_info['purse'] = re.sub(';', '', purse_data.group(1))
        race_info['purse_string'] = all_purse_data
        condition_string = condition_string[purse_data.end(0):]
    except AttributeError:
        pass

    # Race conditions
    try:
        race_conditions = re.match(r'[A-Z0-9 ;\$-]+. ', condition_string)
        condition_string = condition_string[race_conditions.end(0):]
    except AttributeError:
        pass

    # Weight amounts
    try:
        weight_info = re.search(r'(Weight|Three).+?\.( |$)', condition_string)
        # print(weight_info.group(0))
        race_info['weight_info'] = weight_info.group(0)

    except AttributeError:
        pass

        # Single-weight amount
    try:
        one_weight = re.match(r'[Ww]eight.+?(\d+)', weight_info.group(0))
        race_info['standard_weight'] = one_weight.group(1)
    except AttributeError:
        pass

        # Special 3-year-old weight amount
    try:
        three_yo_weights = re.search(r'[Tt]hree.+?(\d+).+?(\d+)', condition_string)
        race_info['three_yo_weight'] = three_yo_weights.group(1)
        race_info['standard_weight'] = three_yo_weights.group(2)
    except AttributeError:
        pass

    try:
        condition_string = condition_string[:weight_info.regs[0][0]] + condition_string[weight_info.regs[0][1]:]
    except AttributeError:
        pass

    # Rail distance
    try:
        rail_info = re.search(r'\(?[Rr]ail.+?(\d+).*\.', condition_string)
        # print(rail_info.group(0), rail_info.group(1))
        race_info['cond_rail_distance'] = rail_info.group(1)
        condition_string = condition_string[:rail_info.regs[0][0]] + condition_string[rail_info.regs[0][1]:]
    except AttributeError:
        pass

    # Weight allowances
    i = 0
    while re.search(r'[^.]* [Aa]llowed \d+ [^.]*\.', condition_string):
        weight_allowance = re.search(r'[^.]* [Aa]llowed (\d+)[^.]*\.', condition_string)
        # print(weight_allowance.group(0))
        condition_string = condition_string[:weight_allowance.regs[0][0]] + \
                           condition_string[weight_allowance.regs[0][1]:]
        race_info[f'weight_allowance_{i}_amt'] = weight_allowance.group(1)
        race_info[f'weight_allowance_{i}_condition'] = weight_allowance.group(0)[:255]
        i += 1
    del i

    race_info['cond_left_on_string'] = condition_string

    return race_info


def parse_age_sex_restrictions(restriction_column):

    new_columns = ['allowed_age_two',
                   'allowed_age_three',
                   'allowed_age_four',
                   'allowed_age_five',
                   'allowed_age_older',
                   'allowed_fillies',
                   'allowed_mares',
                   'allowed_colts_geldings',
                   ]

    age_mappings = {
        'AO': ['two'],
        'AU': ['two', 'three', 'four', 'five', 'older'],
        'BO': ['three'],
        'BU': ['three', 'four', 'five', 'older'],
        'CO': ['four'],
        'CU': ['four', 'five', 'older'],
        'DO': ['five'],
        'DU': ['five', 'older'],
        'EO': ['three', 'four'],
        'FO': ['four', 'five'],
        'GO': ['three', 'four', 'five'],
        'HO': ['two', 'three', 'four', 'five', 'older'],
    }

    sex_mappings = {
        'N': ['fillies', 'mares', 'colts_geldings'],
        'M': ['fillies', 'mares'],
        'F': ['fillies'],
        'C': ['colts_geldings'],
    }

    new_column_dict = dict.fromkeys(new_columns)
    for key in new_column_dict:
        new_column_dict[key] = [0 for _ in range(len(restriction_column))]


    for i in range(len(restriction_column)):
        age_sex_string = restriction_column[i]
        if (isinstance(age_sex_string, np.float) and np.isnan(age_sex_string)):
            age_sex_string = 'NULL'
        age_code = age_sex_string[:2]
        sex_code = age_sex_string[2:]
        try:
            for item in age_mappings[age_code]:
                new_column_dict[f'allowed_age_{item}'][i] = 1
        except KeyError:
            for item in age_mappings['HO']:
                new_column_dict[f'allowed_age_{item}'][i] = 'NULL'

        try:
            for item in sex_mappings[sex_code]:
                new_column_dict[f'allowed_{item}'][i] = 1
        except KeyError:
            for item in sex_mappings['N']:
                new_column_dict[f'allowed_{item}'][i] = 'NULL'

    return new_column_dict


def add_features (table_data, extension, verbose=True):
    extension = str(extension)
    if extension == '1':
        if verbose: print('Adding features to .1 file ...')
        # Parse and flatten age/sex restriction codes
        for key, value in parse_age_sex_restrictions(table_data['age_sex_restrictions']).items():
            table_data[key] = value

        #********************
        # Parse race condition string for race restrictions and add new columns to dataframe

        # Initialize instance of parsing class
        parser = ClassParser()
        condition_columns = ['race_conditions_1', 'race_conditions_2', 'race_conditions_3',
                             'race_conditions_4', 'race_conditions_5']

        # Create list of full race conditions text for processing
        condition_list = []
        for i in range(len(table_data)):
            condition_text = ''
            for column in condition_columns:
                if not is_blank(table_data[column][i]):
                    condition_text += str(table_data[column][i])
            condition_list.append(condition_text)

        # Create a list of race dates for use by the conditions_parser in computing time limits
        date_list = []
        for date in table_data['date']:
            date_list.append(datetime.strptime(str(date), '%Y%m%d'))

        # Process condition strings and add resulting columns to table
        condition_data = parser.process_condition_list(condition_list, date_list)
        for key, value in condition_data.items():
            table_data[key] = value



            ##############NEED TO ADD TO DBs AND TABLE STRUCTURE DICTS. ALSO ADD TO OTHER TABLES WITH CONDITION DATA


    if extension == '2':
        if verbose: print('Adding features to .2 file ...')

        # ************************************************
        # Flatten medication codes into individual columns
        #
        medication_col = table_data.columns.get_loc('medication_codes')
        bleeder_meds = [0 for _ in range(len(table_data))]
        bute = [0 for _ in range(len(table_data))]
        lasix = [0 for _ in range(len(table_data))]
        for i in range(len(table_data)):
            try:
                code = table_data.iloc[i, medication_col].upper()
            except AttributeError:
                code = ''
            if 'A' in code:
                bleeder_meds[i] = 1
            if 'B' in code or 'C' in code:
                bute[i] = 1
            if 'L' in code or 'M' in code:
                lasix[i] = 1
        table_data['meds_adjunct_bleeder'] = bleeder_meds
        table_data['meds_bute'] = bute
        table_data['meds_lasix'] = lasix

        # ***********************************************
        # Flatten equipment codes into individual columns
        #
        equipment_col = table_data.columns.get_loc('equipment_code')
        equipment_list = {
            '1': 'running_ws',
            '2': 'screens',
            '3': 'shields',
            'A': 'aluminum_pads',
            'B': 'blinkers',
            'C': 'mud_calks',
            'D': 'glued_shoes',
            'E': 'inner_rims',
            'F': 'front_bandages',
            'G': 'goggles',
            'H': 'outer_rims',
            'I': 'inserts',
            'J': 'aluminum_pad',
            'K': 'flipping_halter',
            'L': 'bar_shoes',
            'M': 'blocks',
            'N': 'no_whip',
            'O': 'blinkers_off',
            'P': 'pads',
            'Q': 'nasal_strip_off',
            'R': 'bar_shoe',
            'S': 'nasal_strip',
            'T': 'turndowns',
            'U': 'spurs',
            'V': 'cheek_piece',
            'W': 'queens_plates',
            'X': 'cheek_piece_off',
            'Y': 'no_shoes',
            'Z': 'tongue_tie',
        }
        equipment_dict = dict.fromkeys(list(equipment_list.values()))
        for key in equipment_dict.keys():
            equipment_dict[key] = [0 for _ in range(len(table_data))]

        for i in range(len(table_data)):
            code = table_data.iloc[i, equipment_col]
            if is_blank(code):
                continue
            for letter in code:
                equipment_dict[equipment_list[letter]][i] = 1
        for key, value in equipment_dict.items():
            table_data[key] = value

        # ***********************************************
        # Combine lead/beaten lengths columns into single column,
        # with a positive value for the leader and a negative
        # value for all trailing horses
        calls = ['start', '1st_call', '2d_call', '3d_call', 'stretch_call', 'finish']
        for call in calls:
            column_data = list()
            lead_column = table_data.columns.get_loc(f'{call}_lead')
            beaten_column = table_data.columns.get_loc(f'{call}_beaten')
            for i in range(len(table_data)):
                if not np.isnan(table_data.iloc[i, lead_column]):
                    column_data.append(table_data.iloc[i, lead_column])
                elif np.isnan(table_data.iloc[i, beaten_column]):
                    column_data.append('NULL')
                elif table_data.iloc[i, beaten_column] == 0:
                    column_data.append('NULL')
                elif table_data.iloc[i, beaten_column] != 0:
                    column_data.append(table_data.iloc[i, beaten_column] * -1)
                else:
                    print(f'logic leak\nRow: {i}')
            table_data[f'lead_or_beaten_lengths_{call}'] = column_data

    if extension == '3':
        if verbose: print('Adding features to .3 file ...')
    if extension == '4':
        if verbose: print('Adding features to .4 file ...')
    if extension == '5':
        if verbose: print('Adding features to .5 file ...')
        where_bred = list()
        foreign_bred = list(table_data['foreignbred_code'])
        state_bred = list(table_data['statebred_code'])
        foreign_bred_null = list(table_data['foreignbred_code'].isnull())

        for i in range(len(foreign_bred)):
            if foreign_bred_null[i]:
                where_bred.append(state_bred[i])
            else:
                where_bred.append(foreign_bred[i])
        table_data['where_bred'] = where_bred

    if extension == '6':
        if verbose: print('Adding features to .6 file ...')
    if extension == 'DRF':
        if verbose: print('Adding features to .DRF file ...')

        for i in range(1, 11):
            past_bullet_flag = list()
            for j in range(len(table_data)):
                if table_data[f'workout_time_{i}'][j] < 0:
                    past_bullet_flag.append(1)
                else:
                    past_bullet_flag.append(0)
            table_data[f'workout_time_{i}_bullet'] = past_bullet_flag

        for i in range(1, 11):
            table_data[f'workout_time_{i}'] = table_data[f'workout_time_{i}'].abs()

        for i in range(1, 11):
            past_about_distance = list()
            for j in range(len(table_data)):
                if table_data[f'past_distance_{i}'][j] < 0:
                    past_about_distance.append(1)
                else:
                    past_about_distance.append(0)
            table_data[f'past_distance_{i}_about_flag'] = past_about_distance
        for i in range(1, 11):
            table_data[f'past_distance_{i}'] = table_data[f'past_distance_{i}'].abs()
        for i in range(1, 11):
            table_data[f'workout_distance_{i}'] = table_data[f'workout_distance_{i}'].abs()
        table_data['distance'] = table_data['distance'].abs()


        # Extract whether there was a off turf distance change for the PP race, and add a column with a flag for that
        for i in range(1, 11):
            past_off_turf_dist_change = list()
            for j in range(len(table_data)):
                if table_data[f'past_start_code_{i}'][j] == 'x':
                    past_off_turf_dist_change.append(1)
                else:
                    past_off_turf_dist_change.append(0)
            table_data[f'past_{i}_off_turf_dist_change'] = past_off_turf_dist_change

        # Extract whether the horse used a nasal string for the PP race; add a column with a flag for that info
        # Extract whether there was a off turf distance change for the PP race, and add a column with a flag for that
        for i in range(1, 11):
            past_nasal_strip = list()
            for j in range(len(table_data)):
                if table_data[f'past_start_code_{i}'][j] == 's':
                    past_nasal_strip.append(1)
                else:
                    past_nasal_strip.append(0)
            table_data[f'past_{i}_nasal_strip'] = past_nasal_strip

        if verbose: print('Flattening medication columns')
        # Flatten medication column (this is a data_column_{} entry)
        for i in range(1, 11):
            medication_col = table_data.columns.get_loc(f'past_medication_{i}')
            bute = [0 for _ in range(len(table_data))]
            lasix = [0 for _ in range(len(table_data))]

            for j in range(len(table_data)):
                if table_data.iloc[j, medication_col] == 1:
                    lasix[j] = 1
                if table_data.iloc[j, medication_col] == 2:
                    bute[j] = 1
                if table_data.iloc[j, medication_col] == 3:
                    lasix[j] = 1
                    bute[j] = 1
            table_data[f'past_medication_{i}_lasix'] = lasix
            table_data[f'past_medication_{i}_bute'] = bute

        # ***********************************************
        # Combine lead/beaten lengths columns into single column,
        # with a positive value for the leader and a negative
        # value for all trailing horses
        if verbose: print('Combining lead/beaten lengths columns into a single column')
        calls = ['start', 'first_call', 'second_call', 'stretch_call', 'finish']
        for call in calls:
            for j in range(1, 11):
                column_data = list()
                lead_beaten_col = table_data.columns.get_loc(f'past_lead_margin_{call}_{j}')
                beaten_only_col = table_data.columns.get_loc(f'past_beaten_lengths_{call}_{j}')

                for i in range(len(table_data)):
                    if not np.isnan(table_data.iloc[i, beaten_only_col]):
                        column_data.append(table_data.iloc[i, beaten_only_col] * -1)
                    else:
                        column_data.append(table_data.iloc[i, lead_beaten_col])
                table_data[f'past_lead_or_beaten_lengths_{call}_{j}'] = column_data

        # ***********************************************
        # Parse the race conditions to add:
        #   (1) weight allowance conditions:
        #       - weight_allowance_0_amt
        #       - weight_allowance_0_condition
        #       - weight_allowance_0_amt
        #       - weight_allowance_0_condition
        #       - weight_allowance_0_amt
        #       - weight_allowance_0_condition
        #       - weight_allowance_0_amt
        #       - weight_allowance_0_condition
        # (2) weight conditions:
        #       - standard_weight
        #       - three_yo_weight
        # (3) race_class (probably duplicative of other previously provided columns)
        #       - cond_race_class
        # (4) rail distance (to confirm with previously provided column)
        #       - cond_rail_distance
        # (5) remaining unparsed portion of conditions string (for diagnostic purposes)
        #       - cond_left_on_string
        condition_fields = {
            'cond_race_class': list(),
            'standard_weight': list(),
            'three_yo_weight': list(),
            'cond_rail_distance': list(),
            'weight_allowance_0_amt': list(),
            'weight_allowance_0_condition': list(),
            'weight_allowance_1_amt': list(),
            'weight_allowance_1_condition': list(),
            'weight_allowance_2_amt': list(),
            'weight_allowance_2_condition': list(),
            'weight_allowance_3_amt': list(),
            'weight_allowance_3_condition': list(),
            'cond_left_on_string': list(),
        }
        if verbose: print('running parse_conditions')
        for i in range(len(table_data)):
            race_conditions = ['race_conditions_1', 'race_conditions_2', 'race_conditions_3',
                               'race_conditions_4', 'race_conditions_5', 'race_conditions_6', ]
            condition_string = ''
            for condition in race_conditions:
                race_condition_data = table_data[condition][i]
                if not is_blank(race_condition_data):
                    condition_string += str(race_condition_data)
                # print(condition_string)
            parsed_data = parse_conditions(condition_string)
            for key in condition_fields.keys():
                condition_fields[key].append(parsed_data[key])
        for key, value in condition_fields.items():
            table_data[key] = value

        # Parse and flatten age_sex_restriction codes, both for current race
        # and for past performance races

        for key, value in parse_age_sex_restrictions(table_data['age_sex_restricts']).items():
            table_data[key] = value

        for i in range(1, 11):
            for key, value in parse_age_sex_restrictions(table_data[f'past_age_sex_restrictions_{i}']).items():
                table_data[f'past_{key}_{i}'] = value


        #********************
        # Parse race condition string for race restrictions and add new columns to dataframe
        if verbose: print('Parsing race conditions')
        # Initialize instance of parsing class
        parser = ClassParser()
        condition_columns = ['race_conditions_1', 'race_conditions_2', 'race_conditions_3',
                             'race_conditions_4', 'race_conditions_5', 'race_conditions_6']

        # Create list of full race conditions text for processing
        condition_list = list()
        for i in range(len(table_data)):
            condition_text = ''
            for column in condition_columns:
                if not is_blank(table_data[column][i]):
                    condition_text += str(table_data[column][i])
            condition_list.append(condition_text)

        # Create a list of race dates for use by the conditions parser in computing time limits
        date_list = list()
        for date in table_data['date']:
            date_list.append(datetime.strptime(str(date), '%Y%m%d'))

        # Process condition strings and add resulting columns to table
        condition_data = parser.process_condition_list(condition_list, date_list)
        for key, value in condition_data.items():
            table_data[key] = value

    # Cover internal error values with None so that they can be put into the SQL table without throwing an error
    table_data.replace('ERROR!', np.nan, inplace=True)
    table_data.replace('ERROR!--NEGATIVE NUM', np.nan, inplace=True)
    table_data.replace('ISSUE!', np.nan, inplace=True)

    return table_data


