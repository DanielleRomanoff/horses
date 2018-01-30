col_1_dtypes = {
    'track_code': 'VARCHAR(255)',
    'date': 'INT',
    'race_num': 'INT',
    'day_evening_flag': 'VARCHAR(255)',
    'distance': 'FLOAT',
    'distance_units': 'VARCHAR(255)',
    'about_dist_flag': 'INT',
    'surface_old_style': 'VARCHAR(255)',
    'surface_new_style': 'VARCHAR(255)',
    'all_weather_flag': 'INT',
    'chute_start_flag': 'INT',
    'BRIS_race_type': 'VARCHAR(255)',
    'equibase_race_type': 'VARCHAR(255)',
    'race_grade': 'INT',
    'age_sex_restrictions': 'VARCHAR(255)',
    'race_restrict_code': 'VARCHAR(255)',
    'state_bred_flag': 'VARCHAR(255)',
    'abbrev_race_class': 'VARCHAR(255)',
    'breed_of_race': 'VARCHAR(255)',
    'country_code': 'VARCHAR(255)',
    'purse': 'INT',
    'total_race_value': 'INT',
    'max_claim_price': 'INT',
    'race_conditions_1': 'VARCHAR(255)',
    'race_conditions_2': 'VARCHAR(255)',
    'race_conditions_3': 'VARCHAR(255)',
    'race_conditions_4': 'VARCHAR(255)',
    'race_conditions_5': 'VARCHAR(255)',
    'field_size': 'INT',
    'track_condition': 'VARCHAR(255)',
    'fraction_1_time': 'FLOAT',
    'fraction_2_time': 'FLOAT',
    'fraction_3_time': 'FLOAT',
    'fraction_4_time': 'FLOAT',
    'fraction_5_time': 'FLOAT',
    'final_time': 'FLOAT',
    'fraction_1_dist': 'INT',
    'fraction_2_dist': 'INT',
    'fraction_3_dist': 'INT',
    'fraction_4_dist': 'INT',
    'fraction_5_dist': 'INT',
    'off_time': 'INT',
    'start_call_dist': 'INT',
    'call_dist_first': 'INT',
    'call_dist_second': 'INT',
    'call_dist_third': 'INT',
    'race_name': 'VARCHAR(255)',
    'start_description': 'VARCHAR(255)',
    'temp_rail_dist': 'INT',
    'off_turf_flag': 'INT',
    'off_turf_dist_change': 'INT',
    'weather': 'VARCHAR(255)',
    'race_temp': 'INT',
    'WPS_show_pool': 'FLOAT',
    'run_up_dist': 'INT',
}

col_2_dtypes = {
    'track_code': 'VARCHAR(255)',
    'date': 'INT',
    'race_num': 'INT',
    'day_evening_flag': 'VARCHAR(255)',
    'horse_name': 'VARCHAR(255)',
    'foreign_bred_code': 'VARCHAR(255)',
    'state_bred_code': 'VARCHAR(255)',
    'post_position': 'INT',
    'program_number': 'INT',
    'birth_year': 'INT',
    'breed': 'VARCHAR(255)',
    'coupled_flag': 'VARCHAR(255)',
    'jockey_name': 'VARCHAR(255)',
    'jockey_last_name': 'VARCHAR(255)',
    'jockey_first_name': 'VARCHAR(255)',
    'jockey_middle_name': 'VARCHAR(255)',
    'trainer_name': 'VARCHAR(255)',
    'trainer__last_name': 'VARCHAR(255)',
    'trainer_first_name': 'VARCHAR(255)',
    'trainer_middle_name': 'VARCHAR(255)',
    'trip_comment': 'VARCHAR(255)',
    'owner_name': 'VARCHAR(255)',
    'owner_first_name': 'VARCHAR(255)',
    'owner_middle_name': 'VARCHAR(255)',
    'claiming_price': 'INT',
    'medication_codes': 'VARCHAR(255)',
    'equipment_code': 'VARCHAR(255)',
    'earnings': 'INT',
    'odds': 'FLOAT',
    'nonbetting_flag': 'VARCHAR(255)',
    'favorite_flag': 'INT',
    'disqualified_flag': 'INT',
    'disqulaified_placing': 'INT',
    'weight': 'INT',
    'corrected_weight': 'INT',
    'overweight_amt': 'INT',
    'claimed_flag': 'INT',
    'claimed_trainer': 'VARCHAR(255)',
    'claimed_trainer_last': 'VARCHAR(255)',
    'claimed_trainer_first': 'VARCHAR(255)',
    'claimed_trainer_middle': 'VARCHAR(255)',
    'claimed_owner': 'VARCHAR(255)',
    'claimed_owner_last': 'VARCHAR(255)',
    'claimed_owner_first': 'VARCHAR(255)',
    'claimed_owner_middle': 'VARCHAR(255)',
    'win_payout': 'FLOAT',
    'place_payout': 'FLOAT',
    'show_payout': 'FLOAT',
    'start_call_pos': 'INT',
    '1st_call_pos': 'INT',
    '2d_call_pos': 'INT',
    '3d_call_pos': 'INT',
    'stretch_call_pos': 'INT',
    'finish_pos': 'INT',
    'official_finish_pos': 'INT',
    'start_lead': 'FLOAT',
    '1st_call_lead': 'FLOAT',
    '2d_call_lead': 'FLOAT',
    '3d_call_lead': 'FLOAT',
    'stretch_lead': 'FLOAT',
    'finish_lead': 'FLOAT',
    'start_beaten': 'FLOAT',
    '1st_call_beaten': 'FLOAT',
    '2d_call_beaten': 'FLOAT',
    '3d_call_beaten': 'FLOAT',
    'stretch_call_beaten': 'FLOAT',
    'finish_beaten': 'FLOAT',
    'start_margin': 'FLOAT',
    '1st_call_margin': 'FLOAT',
    '2d_call_margin': 'FLOAT',
    '3d_call_margin': 'FLOAT',
    'stretch_call_margin': 'FLOAT',
    'finish_margin': 'FLOAT',
    'dead_heat_flag': 'INT',
    'horse_reg_id': 'VARCHAR(255)',
    'jockey_id': 'INT',
    'trainer_id': 'INT',
    'owner_id': 'INT',
    'claimed_trainer_id': 'INT',
    'claimed_owner_id': 'INT',
}

col_3_dtypes = {
    'track_code': 'VARCHAR(255)',
    'date': 'INT',
    'race_num': 'INT',
    'day_evening_flag': 'VARCHAR(255)',
    'horse_name': 'VARCHAR(255)',
    'foreign_bred_code': 'VARCHAR(255)',
    'statebred_code': 'VARCHAR(255)',
    'program_number': 'INT',
    'win_payout': 'FLOAT',
    'place_payout': 'FLOAT',
    'show_payout': 'FLOAT',
}

col_4_dtypes = {
    'track_code': 'VARCHAR(255)',
    'date': 'INT',
    'race_num': 'INT',
    'day_evening_flag': 'VARCHAR(255)',
    'wager_type': 'VARCHAR(255)',
    'bet_amount': 'FLOAT',
    'payout_amount': 'FLOAT',
    'number_correct': 'VARCHAR(255)',
    'winning_numbers': 'VARCHAR(255)',
    'wager_pool': 'FLOAT',
    'carryover_amount': 'FLOAT'
}

col_5_dtypes = {
    'track_code': 'VARCHAR(255)',
    'date': 'INT',
    'race_num': 'INT',
    'day_evening_flag': 'VARCHAR(255)',
    'horse_name': 'VARCHAR(255)',
    'foreignbred_code': 'VARCHAR(255)',
    'statebred_code': 'VARCHAR(255)',
    'program_number': 'VARCHAR(255)',
    'breeder': 'VARCHAR(255)',
    'color': 'VARCHAR(255)',
    'foal_date': 'INT',
    'age': 'INT',
    'sex': 'VARCHAR(255)',
    'sire': 'VARCHAR(255)',
    'dam': 'VARCHAR(255)',
    'broodmare_sire': 'VARCHAR(255)',
}

col_6_dtypes = {
    'track_code': 'VARCHAR(255)',
    'date': 'INT',
    'race_num': 'INT',
    'day_evening_flag': 'VARCHAR(255)',
    'footnote_sequence': 'INT',
    'footnote_text': 'VARCHAR(255)'
}