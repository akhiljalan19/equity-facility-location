#########
# LOAD DATA
##########
cc_health_ins_orig_df = pd.read_csv('all-data/census-datasets/contra-costa/cc_health_ins_binarized.csv').sort_values(by='Latitude')
cc_race_orig_df = pd.read_csv('all-data/census-datasets/contra-costa/ethnicity_cc_split.csv').sort_values(by='Latitude')

DATA_PATH = 'all-data/'

# Alameda split dataframes
al_race_split_df = pd.read_csv(DATA_PATH + 'census-datasets/alameda/ethnicity_alameda_tr_split_unknown_removed.csv')
al_health_ins_split_df = pd.read_csv(DATA_PATH + 'census-datasets/alameda/health_ins_binarized_unknown_removed.csv')
al_income_df = pd.read_csv(DATA_PATH + 'census-datasets/alameda/poverty_level_alameda_tr_split.csv')

# Contra Costa split dataframes.
cc_race_split_df = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/ethnicity_cc_split_unknown_removed.csv')
cc_health_ins_split_df = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/cc_health_ins_binarized_unknown_removed.csv')
cc_income_df = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/poverty_level_cc_split.csv')

# Non-split dataframes. 
al_race_df_no_split = pd.read_csv(DATA_PATH + 'census-datasets/alameda/ethnicity_alameda_tr.csv')
cc_race_df_no_split = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/ethnicity_contracostacounty_tr.csv')

# Remove unnecessary first column.
cc_race_df_no_split = cc_race_df_no_split.iloc[:-1, :].copy()

# Sort entries by Latitude to ensure consistency of tract numbering across dataframes.
al_race_df_no_split.sort_values(by = 'Latitude', inplace=True)
cc_race_df_no_split.sort_values(by = 'Latitude', inplace=True)
cc_race_split_df.sort_values(by=['Latitude', 'Variable'], inplace=True)
cc_health_ins_split_df.sort_values(by=['Latitude', 'Variable'], inplace=True)
cc_income_df.sort_values(by=['Latitude', 'Variable'], inplace=True)

# Load population long/lat
al_population_long_lat = np.array(al_race_df_no_split[['Longitude', 'Latitude']])
cc_population_long_lat = np.array(cc_race_df_no_split[['Longitude', 'Latitude']])
population_long_lat = np.vstack((al_population_long_lat, cc_population_long_lat))
total_population_by_tract = np.hstack((np.array(al_race_df_no_split['Tot_Population_ACS_10_14']), 
           np.array(cc_race_df_no_split['Tot_Population_ACS_10_14'])))

# Load Facilities data.
al_fac_df = pd.read_csv(DATA_PATH + 'hospital-data/alameda-emergency-facilites.csv').iloc[:18, :].copy()
cc_fac_df = pd.read_csv(DATA_PATH + 'hospital-data/cc-healthcare-dataset.csv')
al_facilites_long_lats = np.array(al_fac_df[['LONGITUDE', 'LATITUDE']])
cc_facilites_long_lats = np.array(cc_fac_df[['LONGITUDE', 'LATITUDE']])
facilites_long_lats = np.vstack((al_facilites_long_lats, cc_facilites_long_lats))

# Merge dataframes for Alameda/Contra Costa counties. 

# Rename columns for consistency of column names. Needed before merging.
al_health_ins_split_df.rename(columns={'value': 'Value', 'variable': 'Variable'}, inplace=True)

# Merge to create unified dataframes. 
race_split_df_all = al_race_split_df[['Latitude', 'Longitude', 'Value', 'Variable']]\
                                                                .copy().append(cc_race_split_df)
income_split_df_all = al_income_df[['Latitude', 'Longitude', 'Value', 'Variable']]\
                                                                .copy().append(cc_income_df)
health_ins_split_df_all = al_health_ins_split_df[['Latitude', 'Longitude', 'Value', 'Variable']]\
                                                        .copy().append(cc_health_ins_split_df)

# Load tract-facility distance matrix, computed via the Google Maps API. 
# Distances refer to the driving distance between pairs of locations. 
gmaps_distance_matrix = pd.read_csv(DATA_PATH + 'all_travel_distance_matrix.csv')

# Remove unnecessary first column.
gmaps_distance_matrix = gmaps_distance_matrix.iloc[:, 1:].copy()

# Convert to numpy array, and divide by 1000 to convert meters to kilometers. 
tract_facility_distance_matrix = np.array(gmaps_distance_matrix)[:, :] / 1000.0

###############
## Health ins.
##############

os.listdir(DATA_PATH + 'census-datasets/contra-costa/')
cc_race_df_with_unknown = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/ethnicity_cc_split.csv')
cc_health_ins_df_with_unknown = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/cc_health_ins_binarized.csv')

cc_health_ins_orig_df = pd.read_csv(DATA_PATH + 'census-datasets/contra-costa/health_ins_contracostacounty_tr.csv')

# Add unknown column.
cc_health_ins_orig_df['Unknown'] = cc_health_ins_orig_df['Tot_Population_ACS_10_14'] - np.sum(cc_health_ins_orig_df[['No_Health_Ins_ACS_10_14', 'One_Health_Ins_ACS_10_14', 'Two_Plus_Health_Ins_ACS_10_14']], axis=1)
cc_health_ins_orig_df['Known_Group_Counts'] = np.sum(cc_health_ins_orig_df[['No_Health_Ins_ACS_10_14', 'One_Health_Ins_ACS_10_14', 'Two_Plus_Health_Ins_ACS_10_14']], axis=1)
known_grp_names = ['No_Health_Ins_ACS_10_14', 'One_Health_Ins_ACS_10_14', 'Two_Plus_Health_Ins_ACS_10_14']
cc_health_ins_orig_df.dropna(inplace=True)
percentages = []
for name in known_grp_names: 
    percents = np.divide(np.array(cc_health_ins_orig_df[name]), np.array(cc_health_ins_orig_df['Known_Group_Counts']))
    percentages.append(percents)

for index, name in enumerate(known_grp_names): 
    grp_percentages = percentages[index]
    augment_arr = np.multiply(np.array(grp_percentages), cc_health_ins_orig_df['Unknown'])
    cc_health_ins_orig_df[name + '_Augmented'] = cc_health_ins_orig_df[name] + augment_arr

augment_names = ['No_Health_Ins_ACS_10_14_Augmented', 
                 'One_Health_Ins_ACS_10_14_Augmented', 'Two_Plus_Health_Ins_ACS_10_14_Augmented']

cc_health_ins_orig_df['One_Plus_Health_Ins'] = np.sum(cc_health_ins_orig_df[['One_Health_Ins_ACS_10_14_Augmented', 
                                                      'Two_Plus_Health_Ins_ACS_10_14_Augmented']], axis=1) 

cc_health_ins_orig_df.to_csv(DATA_PATH + 'census-datasets/contra-costa/contra_costra_health_ins_tr_post_processed.csv')

melt_df = pd.melt(cc_health_ins_orig_df[['Latitude', 'Longitude', 'No_Health_Ins_ACS_10_14_Augmented', 'One_Plus_Health_Ins']], 
       var_name='Variable', value_name='Value', id_vars=['Latitude', 'Longitude'],
        value_vars=['No_Health_Ins_ACS_10_14_Augmented', 'One_Plus_Health_Ins'])

melt_df.sort_values(by='Latitude', inplace=True)
melt_df['Variable'] = melt_df['Variable'].apply(lambda x: x if x == 'One_Plus_Health_Ins' else 'No_Health_Ins_ACS_10_14')
melt_df.to_csv(DATA_PATH + 'census-datasets/contra-costa/cc_health_ins_binarized_unknown_augmented.csv')






###########
# Race
##########
cc_race_df_with_unknown.sort_values(by='Latitude', inplace=True)
all_race_names = list(cc_race_df_with_unknown['variable'].unique())
race_names = [x for x in all_race_names if x != 'Other']
other_pop_df = cc_race_df_with_unknown[cc_race_df_with_unknown['variable'] == 'Other']


known_pop_count = np.zeros(shape = (other_pop_df.shape[0],))
for name in race_names: 
    known_pop_count += np.array(cc_race_df_with_unknown[cc_race_df_with_unknown['variable'] == name]['value'])

cc_race_df_with_unknown.sort_values(by=['Latitude', 'variable'], inplace=True)

new_value_col = np.zeros(shape=(cc_race_df_with_unknown.shape[0],))

for index, name in enumerate(sorted(race_names)): 
    print(name)
    
    group_pop = np.array(cc_race_df_with_unknown[cc_race_df_with_unknown['variable'] == name]['value'])
    group_percentage = np.divide(group_pop, known_pop_count)
    unknown_pop = np.multiply(group_percentage, np.array(other_pop_df['value']))
    
    for i in range(other_pop_df.shape[0]): 
        row_index = (7 * i) + index
        new_pop = unknown_pop[i] + cc_race_df_with_unknown.iloc[row_index]['value']
        new_value_col[row_index] = new_pop

cc_race_df_processed = pd.DataFrame.copy(cc_race_df_with_unknown)
cc_race_df_processed['value'] = new_value_col
cc_race_df_augmented = pd.DataFrame.copy(cc_race_df_processed[cc_race_df_processed['variable'] != 'Other'])
cc_race_df_augmented.to_csv(DATA_PATH + 'census-datasets/contra-costa/cc_ethnicity_unknown_augmented.csv')

##################
# Rename and sort
##################

cc_race_df_augmented.rename(columns={'value': 'Value', 'variable': 'Variable'}, inplace=True)
cc_race_df_augmented.sort_values(by=['Latitude', 'Value'], inplace=True)
cc_health_ins_df.sort_values(by=['Latitude', 'Value'], inplace=True)
cc_income_df.sort_values(by=['Latitude', 'Value'], inplace=True)

# Merge dataframes for Alameda/Contra Costa counties. 

race_split_df_all = al_race_split_df[['Latitude', 'Longitude', 'Value', 'Variable']]\
                        .copy().append(cc_race_df_augmented[['Latitude', 'Longitude', 'Value', 'Variable']].copy())
income_split_df_all = al_income_df[['Latitude', 'Longitude', 'Value', 'Variable']]\
                        .copy().append(cc_income_df[['Latitude', 'Longitude', 'Value', 'Variable']].copy())
health_ins_split_df_all = al_health_ins_split_df[['Latitude', 'Longitude', 'Value', 'Variable']]\
                        .copy().append(cc_health_ins_df[['Latitude', 'Longitude', 'Value', 'Variable']].copy())










