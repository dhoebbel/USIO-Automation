
#import dependencies
import pandas as pd
import numpy as np
import datetime
import math

#read in CSVs

full_lens = "Dave Files (raw)//2018 H1 Raw Full Lens.csv"
buyer_lens = "Dave Files (raw)//2018 H1 Final Buyer Lens.csv"
region_map = "region_map.csv"
josh_volumes = "2018Q2_Josh_Volume.csv"
ncreif = "ncreif_v1.csv"


full_df = pd.read_csv(full_lens, encoding = "ISO-8859-1")
buyer_df = pd.read_csv(buyer_lens, encoding = "ISO-8859-1")
region_map_df = pd.read_csv(region_map, encoding = "ISO-8859-1")
josh_volumes_df = pd.read_csv(josh_volumes, encoding = "ISO-8859-1")
cap_rates = pd.read_csv(ncreif, encoding = "ISO-8859-1")


## Data Transformation # NON Portfolio Datafile
#convert data to numeric for parsing

full_df.apply(pd.to_numeric,errors = 'ignore')
buyer_df.apply(pd.to_numeric,errors = 'ignore')

#create quarter column
full_df['Quarter'] = full_df['Quarter of transaction'].str[5:]
full_df

#Full lens Dataframe excluding portfolio headers rows
full_df_no_port = full_df[~full_df['Portfolio sale?'].isin(['Port.'])]
full_df_no_port['Portfolio sale?'].value_counts()

#Add in column that concatenates Quarter and Market Name for better table parsing
full_df_no_port["QQ_Market"] = full_df_no_port["Quarter"].map(str) + "_" + full_df_no_port["JLL Market"]

#Add in column that concatenates Quarter and Product Type for better table parsing
full_df_no_port["QQ_Product"] = full_df_no_port["Quarter"].map(str) + "_" + full_df_no_port["JLL Product Type"]

#Office
office_full_df = full_df_no_port[~full_df_no_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Industrial & Flex-R&D
industrial_full_df = full_df_no_port[~full_df_no_port['JLL Sector'].isin(['Office', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Multifamily
multifamily_full_df = full_df_no_port[~full_df_no_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Office', 'Seniors Housing', 'Retail'])]

#Retail
retail_full_df = full_df_no_port[~full_df_no_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Office'])]



######### Port. ONLY Data file ##################

#full DF filtered only for Port.
full_df_port = full_df[~full_df['Portfolio sale?'].isin(['Yes', 'No'])]

#Office
office_full_df_port = full_df_port[~full_df_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Industrial & Flex-R&D
industrial_full_df_port = full_df_port[~full_df_port['JLL Sector'].isin(['Office', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Multifamily
multifamily_full_df_port = full_df_port[~full_df_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Office', 'Seniors Housing', 'Retail'])]

#Retail
retail_full_df_port = full_df_port[~full_df_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Office'])]



############# Buyer Lens Transformation with No PORTFOLIO #######################

#create quarter column
buyer_df['Quarter'] = buyer_df['Quarter of transaction'].str[5:]
# buyer_df.head()

#buyer lens Dataframe excluding portfolio headers rows
buyer_df_no_port = buyer_df[~buyer_df['Portfolio sale?'].isin(['Port.'])]

#Office
office_buyer_df = buyer_df_no_port[~buyer_df_no_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Industrial & Flex-R&D
industrial_buyer_df = buyer_df_no_port[~buyer_df_no_port['JLL Sector'].isin(['Office', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Multifamily
multifamily_buyer_df = buyer_df_no_port[~buyer_df_no_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Office', 'Seniors Housing', 'Retail'])]

#Retail
retail_buyer_df = buyer_df_no_port[~buyer_df_no_port['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Office'])]



############################ REMOVES NULL FROM COUNTRY ##############################

buyer_df_no_port_no_null = buyer_df_no_port[buyer_df_no_port['Country'].notnull()]

#Office
office_buyer_df_no_null = buyer_df_no_port_no_null[~buyer_df_no_port_no_null['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Industrial & Flex-R&D
industrial_buyer_df_no_null = buyer_df_no_port_no_null[~buyer_df_no_port_no_null['JLL Sector'].isin(['Office', 'Multifamily', 'Seniors Housing', 'Retail'])]

#Multifamily
multifamily_buyer_df_no_null = buyer_df_no_port_no_null[~buyer_df_no_port_no_null['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Office', 'Seniors Housing', 'Retail'])]

#Retail
retail_buyer_df_no_null = buyer_df_no_port_no_null[~buyer_df_no_port_no_null['JLL Sector'].isin(['Industrial', 'Flex-R&D', 'Multifamily', 'Seniors Housing', 'Office'])]



############################# NCREIF Cap Rate Visuals ###################################

#convert cap rate df to useable format
cap_cols = cap_rates.columns.drop(cap_rates[['Market', 'Sector', 'Market Type']])
cap_rates[cap_cols] = cap_rates[cap_cols].apply(pd.to_numeric, errors='coerce')
cap_rates.fillna(0)

#consolidate to just overall metrics
cap_rates_overall = cap_rates[cap_rates['Market'].isin(['Primary', 'Secondary', 'Overall', 'Ten-Year Treasury'])]

#office overall cap rates
office_cap_rates_overall = cap_rates_overall[cap_rates_overall['Sector'].isin(['Office', 'Ten-Year Treasury'])]

#industrial overall cap rates
industrial_cap_rates_overall = cap_rates_overall[cap_rates_overall['Sector'].isin(['Industrial', 'Ten-Year Treasury'])]

#multifamily overall cap rates
multifamily_cap_rates_overall = cap_rates_overall[cap_rates_overall['Sector'].isin(['Multifamily', 'Ten-Year Treasury'])]

#retail overall cap rates
retail_cap_rates_overall = cap_rates_overall[cap_rates_overall['Sector'].isin(['Retail', 'Ten-Year Treasury'])]



#calculating retail investment volumes
retail_volumes = retail_full_df.pivot_table(index=["Year of transaction"],values=["Price ($)"],
               columns=["Quarter"],aggfunc=[np.sum],fill_value=0)
retail_volumes_billions = retail_volumes / 1000000000

####Shift pivot to normal dataframe
retail_volumes_billions.columns = retail_volumes_billions.columns.droplevel(0)
retail_volumes_billions.columns = retail_volumes_billions.columns.droplevel(0)
retail_volumes_billions.columns.name = None               #remove categories
retail_volumes_final = retail_volumes_billions.reset_index() 

##Final DFs
#retail_volumes_final




#calculating retail investment volumes by transaction type (i.e. Single Asset, Portfolio and Recapitilization)

#Annual single asset volume
retail_single_asset_volume = retail_full_df[retail_full_df['Portfolio sale?'] == 'No'].pivot_table(index=["Year of transaction"], 
                                values=["Price ($)"], columns=["Portfolio sale?"], aggfunc=[np.sum],fill_value=0)

#Annual Recap Volume
retail_recap_volume = retail_full_df[retail_full_df['Sales Type'] == 'Recapitalization'].pivot_table(index=["Year of transaction"], 
                                values=["Price ($)"], columns=["Sales Type"], aggfunc=[np.sum],fill_value=0)

#Shift single asset volumes to normal DF
retail_single_asset_volume.columns = retail_single_asset_volume.columns.droplevel(0)
retail_single_asset_volume.columns = retail_single_asset_volume.columns.droplevel(0)
retail_single_asset_volume.columns.name = None               #remove categories
retail_single_asset_volumes_final = retail_single_asset_volume.reset_index() 

#Shift Recap volumes to normal DF
retail_recap_volume.columns = retail_recap_volume.columns.droplevel(0)
retail_recap_volume.columns = retail_recap_volume.columns.droplevel(0)
retail_recap_volume.columns.name = None               #remove categories
retail_recap_volumes_final = retail_recap_volume.reset_index() 


##Final DFs
#retail_single_asset_volumes_final
#retail_recap_volumes_final
#retail_port_volume_final



#calculate portfolio volumes

#Annual Portfolio Volume - Portfolio Sale? = "Port"
retail_port_volume = retail_full_df_port[retail_full_df_port['Portfolio sale?'] == 'Port.'].pivot_table(index=["Year of transaction"], 
                                values=["Price ($)"], columns=["Portfolio sale?"], aggfunc=[np.sum],fill_value=0)

#Shift Annual Portfolio Volume to normal DF
retail_port_volume.columns = retail_port_volume.columns.droplevel(0)
retail_port_volume.columns = retail_port_volume.columns.droplevel(0)
retail_port_volume.columns.name = None               #remove categories
retail_port_volume_final = retail_port_volume.reset_index()

##final DF
#retail_port_volume_final



# Market by Market Quarterly Summary
retail_market_volumes_qtrly = retail_full_df.pivot_table(index=["JLL Market", "Quarter", "QQ_Market", "MarketType"],values=["Price ($)"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Market by Market Annual Summary
retail_market_volumes_annual = retail_full_df.pivot_table(index=["JLL Market", "MarketType"],values=["Price ($)"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Product by Product Quarterly Summary
retail_product_volumes_qtrly = retail_full_df.pivot_table(index=["JLL Product Type", "Quarter", "QQ_Product"],values=["Price ($)"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Product by Product Annual Summary
retail_product_volumes_annual = retail_full_df.pivot_table(index=["JLL Product Type"],values=["Price ($)"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)


#Convert market by market quarterly summary to normal DF
retail_market_volumes_qtrly.columns = retail_market_volumes_qtrly.columns.droplevel(0)
retail_market_volumes_qtrly.columns = retail_market_volumes_qtrly.columns.droplevel(0)
retail_market_volumes_qtrly.columns.name = None               #remove categories
retail_market_volumes_qtrly_final = retail_market_volumes_qtrly.reset_index()

#Convert market by market annual summary to normal DF
retail_market_volumes_annual.columns = retail_market_volumes_annual.columns.droplevel(0)
retail_market_volumes_annual.columns = retail_market_volumes_annual.columns.droplevel(0)
retail_market_volumes_annual.columns.name = None               #remove categories
retail_market_volumes_annual_final = retail_market_volumes_annual.reset_index()

#Convert product by product annual summary
retail_product_volumes_annual.columns = retail_product_volumes_annual.columns.droplevel(0)
retail_product_volumes_annual.columns = retail_product_volumes_annual.columns.droplevel(0)
retail_product_volumes_annual.columns.name = None               #remove categories
retail_product_volumes_annual_final = retail_product_volumes_annual.reset_index()

##Final DFs
# retail_market_volumes_qtrly_final
# retail_market_volumes_annual_final
# retail_product_volumes_annual_final



#Domestic Investment by Buyer Type
buyer_type_domestic_volume = retail_buyer_df_no_null[(retail_buyer_df_no_null['Country'] == 'United States') & (retail_buyer_df_no_null['Country'] != '<unknown>') & (retail_buyer_df_no_null['Country'] != 'NULL')].pivot_table(index=["Type"], 
                                values=["JV_Price"], columns=["Year of transaction"], aggfunc=[np.sum],fill_value=0)

#Foreign Investment by Buyer Type
buyer_type_foreign_volume = retail_buyer_df_no_null[(retail_buyer_df_no_null['Country'] != 'United States') & (retail_buyer_df_no_null['Country'] != '<unknown>') & (retail_buyer_df_no_null['Country'] != 'NULL')].pivot_table(index=["Type"], 
                                 values=["JV_Price"], columns=["Year of transaction"], aggfunc=[np.sum],fill_value=0)

#append a total column to foreign buyer type data frame
total = buyer_type_foreign_volume.apply(np.sum)
total['Year of transaction'] = 'Total'
buyer_type_foreign_volume_transform = buyer_type_foreign_volume.append(pd.DataFrame(total.values, index=total.keys()).T, ignore_index=False)


#Editing TOTAL row in DF to read 'total' instead of '0'
buyer_type_list = buyer_type_foreign_volume_transform.index.tolist()
total = buyer_type_list.index(0)
buyer_type_list[total] = 'foreign total'
buyer_type_foreign_volume_transform.index = buyer_type_list

#Convert buyer_type_foreign_volume_transform to normal DF
buyer_type_foreign_volume_transform.columns = buyer_type_foreign_volume_transform.columns.droplevel(0)
buyer_type_foreign_volume_transform.columns = buyer_type_foreign_volume_transform.columns.droplevel(0)
buyer_type_foreign_volume_transform.columns.name = None               #remove categories
buyer_type_foreign_volume_update = buyer_type_foreign_volume_transform.reset_index()
#remove blank column from DF
buyer_type_foreign_volume_final = buyer_type_foreign_volume_update.drop([''], axis=1)
buyer_type_foreign_volume_final

#Convert buyer_type_domestic_volume to normal DF
buyer_type_domestic_volume.columns = buyer_type_domestic_volume.columns.droplevel(0)
buyer_type_domestic_volume.columns = buyer_type_domestic_volume.columns.droplevel(0)
buyer_type_domestic_volume.columns.name = None               #remove categories
buyer_type_domestic_volume_final = buyer_type_domestic_volume.reset_index()

#filter out CMBS, unknown, sovereign wealth fund, and null values
buyer_type_domestic_volume_final_v2 = buyer_type_domestic_volume_final[(buyer_type_domestic_volume_final['Type'] != 'CMBS') 
                                                   & (buyer_type_domestic_volume_final['Type'] != 'Unknown') 
                                                   & (buyer_type_domestic_volume_final['Type'] != 'Sovereign Wealth Fund')
                                                    & (buyer_type_domestic_volume_final['Type'] != '(null)')]


#filter out unknown, null and CMBS from foreign figures
buyer_type_foreign_volume_final_v2 = buyer_type_foreign_volume_final[(buyer_type_foreign_volume_final['index'] != 'CMBS') 
                                                   & (buyer_type_foreign_volume_final['index'] != 'Unknown') 
                                                    & (buyer_type_foreign_volume_final['index'] != '(null)')]



#append foreign total to combined/summarized DF
buyer_volumes_final_orig = buyer_type_domestic_volume_final_v2.append(buyer_type_foreign_volume_final_v2[buyer_type_foreign_volume_final_v2['index'] == 'foreign total'])

# replace NaN with 'foreign total'
buyer_volumes_final = buyer_volumes_final_orig.replace(np.nan, 'foreign total', regex=True)

# buyer_volumes_final, replaces NaN with Total
total_v3 = buyer_volumes_final.apply(np.sum)
total_v3['Type'] = 'Total'
buyer_volumes_final_v2 = buyer_volumes_final.append(pd.DataFrame(total_v3.values, index=total_v3.keys()).T, ignore_index=False)

#set Type as INDEX
buyer_volumes_final_v2.set_index('Type', inplace=True)

#drop 'index' column - not sure why this was created
buyer_volumes_final_v3 = buyer_volumes_final_v2.drop('index', 1)

#do division to calc percentages
buyer_volumes_final_v3.loc['DevOp_percent']  = buyer_volumes_final_v3.loc['Developer-Operator'] / buyer_volumes_final_v3.loc['Total']
buyer_volumes_final_v3.loc['HNW_percent']  = buyer_volumes_final_v3.loc['High Net Worth'] / buyer_volumes_final_v3.loc['Total']
buyer_volumes_final_v3.loc['Instit_percent'] = buyer_volumes_final_v3.loc['Institution-Advisor'] / buyer_volumes_final_v3.loc['Total']
buyer_volumes_final_v3.loc['REIT_percent'] = buyer_volumes_final_v3.loc['REIT-REOC'] / buyer_volumes_final_v3.loc['Total']
buyer_volumes_final_v3.loc['User_percent'] = buyer_volumes_final_v3.loc['User-Other'] / buyer_volumes_final_v3.loc['Total']
buyer_volumes_final_v3.loc['Foreign_percent'] = buyer_volumes_final_v3.loc['foreign total'] / buyer_volumes_final_v3.loc['Total']
buyer_volumes_final_v3.loc['Total_percent'] = buyer_volumes_final_v3.loc['Total'] / buyer_volumes_final_v3.loc['Total']

# #final DF
# buyer_volumes_final_v3


################### Mapping major regions by country #######################
region_map_df
region_df = retail_buyer_df.merge(region_map_df, on='Country', how='left')



#################### Concatenate Quarter/Country for Granular Breakout #####################

#Add in column that concatenates Quarter and Market Name for better table parsing
region_df["QQ_Country"] = region_df["Quarter"].map(str) + "_" + region_df["Country"]

#Add in column that concatenates Quarter and Product Type for better table parsing
region_df["QQ_Region"] = region_df["Quarter"].map(str) + "_" + region_df["Region"]

#################### Quarterly & Annual Breakouts by Region/Country PIVOT #####################

# Regional/Country Volume Breakout - ANNUAL
regional_country_volumes = region_df.pivot_table(index=["Region", "Country"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Regional/Country Volume Breakout - QUARTERLY
regional_country_volumes_QQ = region_df.pivot_table(index=["Region", "QQ_Country"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Regional Volume - Annual
regional_volumes = region_df.pivot_table(index=["Region"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Regional Volume Breakout - QUARTERLY
regional_volumes_QQ = region_df.pivot_table(index=["Region", "QQ_Region"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)


#################### Quarterly & Annual Breakouts by Region/Country & Market PIVOT #####################

# Regional/Country Volume Breakout - ANNUAL
regional_country_volumes_market = region_df.pivot_table(index=["Region", "Country", "JLL Market"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Regional/Country Volume Breakout - QUARTERLY
regional_country_volumes_QQ_market = region_df.pivot_table(index=["Region", "QQ_Country", "JLL Market"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Regional Volume - Annual
regional_volumes_market = region_df.pivot_table(index=["Region", "JLL Market"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

# Regional Volume Breakout - QUARTERLY
regional_volumes_QQ_market = region_df.pivot_table(index=["Region", "QQ_Region", "JLL Market"],values=["JV_Price"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)



#################### Quarterly & Annual Breakouts by Region/Country & Market 'conversion to normal DF' ###########################

#Convert regional/country volume annual summary to normal DF - ANNUAL
regional_country_volumes_market.columns = regional_country_volumes_market.columns.droplevel(0)
regional_country_volumes_market.columns = regional_country_volumes_market.columns.droplevel(0)
regional_country_volumes_market.columns.name = None               #remove categories
regional_country_volumes_market_final = regional_country_volumes_market.reset_index()

#Convert regional/country volume annual summary to normal DF QUARTERLY
regional_country_volumes_QQ_market.columns = regional_country_volumes_QQ_market.columns.droplevel(0)
regional_country_volumes_QQ_market.columns = regional_country_volumes_QQ_market.columns.droplevel(0)
regional_country_volumes_QQ_market.columns.name = None               #remove categories
regional_country_volumes_QQ_market_final = regional_country_volumes_QQ_market.reset_index()

#Convert regional volume annual summary to normal DF - ANNUAL
regional_volumes_market.columns = regional_volumes_market.columns.droplevel(0)
regional_volumes_market.columns = regional_volumes_market.columns.droplevel(0)
regional_volumes_market.columns.name = None               #remove categories
regional_volumes_market_final = regional_volumes_market.reset_index()

#Convert regional volume annual summary to normal DF - QUARTERLY
regional_volumes_QQ_market.columns = regional_volumes_QQ_market.columns.droplevel(0)
regional_volumes_QQ_market.columns = regional_volumes_QQ_market.columns.droplevel(0)
regional_volumes_QQ_market.columns.name = None               #remove categories
regional_volumes_QQ_market_final = regional_volumes_QQ_market.reset_index()



#################### Quarterly & Annual Breakouts by Region/Country 'conversion to normal DF'###########################

#Convert regional/country volume annual summary to normal DF - ANNUAL
regional_country_volumes.columns = regional_country_volumes.columns.droplevel(0)
regional_country_volumes.columns = regional_country_volumes.columns.droplevel(0)
regional_country_volumes.columns.name = None               #remove categories
regional_country_volumes_final = regional_country_volumes.reset_index()

#Convert regional/country volume annual summary to normal DF QUARTERLY
regional_country_volumes_QQ.columns = regional_country_volumes_QQ.columns.droplevel(0)
regional_country_volumes_QQ.columns = regional_country_volumes_QQ.columns.droplevel(0)
regional_country_volumes_QQ.columns.name = None               #remove categories
regional_country_volumes_QQ_final = regional_country_volumes_QQ.reset_index()

#Convert regional volume annual summary to normal DF - ANNUAL
regional_volumes.columns = regional_volumes.columns.droplevel(0)
regional_volumes.columns = regional_volumes.columns.droplevel(0)
regional_volumes.columns.name = None               #remove categories
regional_volumes_final = regional_volumes.reset_index()

#Convert regional volume annual summary to normal DF - QUARTERLY
regional_volumes_QQ.columns = regional_volumes_QQ.columns.droplevel(0)
regional_volumes_QQ.columns = regional_volumes_QQ.columns.droplevel(0)
regional_volumes_QQ.columns.name = None               #remove categories
regional_volumes_QQ_final = regional_volumes_QQ.reset_index()



########################## Annual Percetage of overall investment by REGION ###################################

#create offshore dataframe that removes domestic
domestic = regional_volumes.index.isin(['Domestic'])
offshore_regional_total = regional_volumes[~domestic]

#calculate total row and append to regional volumes data frame
regional_total = offshore_regional_total.apply(np.sum)
regional_volumes_final_transform = offshore_regional_total.append(pd.DataFrame(regional_total.values, index=regional_total.keys()).T, ignore_index=False)

#Editing TOTAL row in DF to read 'total' instead of '0'
regional_volumes_list = regional_volumes_final_transform.index.tolist()
r_total = regional_volumes_list.index(0)
regional_volumes_list[r_total] = 'Off-shore total'
regional_volumes_final_transform.index = regional_volumes_list

# #do division to calc percentages
regional_volumes_final_transform.loc['Africa_percent']  = regional_volumes_final_transform.loc['Africa'] / regional_volumes_final_transform.loc['Off-shore total']
regional_volumes_final_transform.loc['Americas_percent']  = regional_volumes_final_transform.loc['Americas'] / regional_volumes_final_transform.loc['Off-shore total']
regional_volumes_final_transform.loc['Asia_percent']  = regional_volumes_final_transform.loc['Asia'] / regional_volumes_final_transform.loc['Off-shore total']
regional_volumes_final_transform.loc['Australia_percent']  = regional_volumes_final_transform.loc['Australia'] / regional_volumes_final_transform.loc['Off-shore total']
regional_volumes_final_transform.loc['Europe_percent']  = regional_volumes_final_transform.loc['Europe'] / regional_volumes_final_transform.loc['Off-shore total']
regional_volumes_final_transform.loc['Middle_East_percent']  = regional_volumes_final_transform.loc['Middle East'] / regional_volumes_final_transform.loc['Off-shore total']
regional_volumes_final_transform.loc['Off-shore_total_percent']  = regional_volumes_final_transform.loc['Off-shore total'] / regional_volumes_final_transform.loc['Off-shore total']

########################################################################################################################
########################################################################################################################

##Major DFs
# regional_country_volumes_final
# regional_country_volumes_QQ_final
# regional_volumes_final
# regional_volumes_QQ_final
# regional_country_volumes_market_final
# regional_country_volumes_QQ_market_final
# regional_volumes_market_final
# regional_volumes_QQ_market_final
#regional_volumes_final_transform



########################## Most active markets table ###################################
# retail_market_volumes_qtrly_final

# Product by Product Quarterly Summary
retail_market_volumes_qtrly_v2 = retail_full_df.pivot_table(index=["JLL Market", "Quarter", "QQ_Market"],values=["Price ($)"],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

#Convert market by market quarterly summary to normal DF
retail_market_volumes_qtrly_v2.columns = retail_market_volumes_qtrly_v2.columns.droplevel(0)
retail_market_volumes_qtrly_v2.columns = retail_market_volumes_qtrly_v2.columns.droplevel(0)
retail_market_volumes_qtrly_v2.columns.name = None               #remove categories
retail_market_volumes_qtrly_final_v2 = retail_market_volumes_qtrly_v2.reset_index()

#create framework for programatic table filter based on the 
x = datetime.date.today()

quarter_minus_one = math.ceil(x.month/3.)-1

reporting_quarter = "Q" + str(quarter_minus_one)

#programattic filter based on today's date
New_Test_DF_v1 = retail_market_volumes_qtrly_final_v2.loc[retail_market_volumes_qtrly_final_v2['Quarter'] == reporting_quarter]
New_Test_DF_v1

#convert column headers to string
New_Test_DF_v1.columns = New_Test_DF_v1.columns.map(str)

#create new columns based on historical rankings
New_Test_DF_v1['2001 Rank'] = New_Test_DF_v1['2001'].rank(method='dense', ascending=False)
New_Test_DF_v1['2002 Rank'] = New_Test_DF_v1['2002'].rank(method='dense', ascending=False)
New_Test_DF_v1['2003 Rank'] = New_Test_DF_v1['2003'].rank(method='dense', ascending=False)
New_Test_DF_v1['2004 Rank'] = New_Test_DF_v1['2004'].rank(method='dense', ascending=False)
New_Test_DF_v1['2005 Rank'] = New_Test_DF_v1['2005'].rank(method='dense', ascending=False)
New_Test_DF_v1['2006 Rank'] = New_Test_DF_v1['2006'].rank(method='dense', ascending=False)
New_Test_DF_v1['2007 Rank'] = New_Test_DF_v1['2007'].rank(method='dense', ascending=False)
New_Test_DF_v1['2008 Rank'] = New_Test_DF_v1['2008'].rank(method='dense', ascending=False)
New_Test_DF_v1['2009 Rank'] = New_Test_DF_v1['2009'].rank(method='dense', ascending=False)
New_Test_DF_v1['2010 Rank'] = New_Test_DF_v1['2010'].rank(method='dense', ascending=False)
New_Test_DF_v1['2011 Rank'] = New_Test_DF_v1['2011'].rank(method='dense', ascending=False)
New_Test_DF_v1['2012 Rank'] = New_Test_DF_v1['2012'].rank(method='dense', ascending=False)
New_Test_DF_v1['2013 Rank'] = New_Test_DF_v1['2013'].rank(method='dense', ascending=False)
New_Test_DF_v1['2014 Rank'] = New_Test_DF_v1['2014'].rank(method='dense', ascending=False)
New_Test_DF_v1['2015 Rank'] = New_Test_DF_v1['2015'].rank(method='dense', ascending=False)
New_Test_DF_v1['2016 Rank'] = New_Test_DF_v1['2016'].rank(method='dense', ascending=False)
New_Test_DF_v1['2017 Rank'] = New_Test_DF_v1['2017'].rank(method='dense', ascending=False)
New_Test_DF_v1['2018 Rank'] = New_Test_DF_v1['2018'].rank(method='dense', ascending=False)

New_Test_DF_v1['YoY Change %'] = (New_Test_DF_v1['2018'] - New_Test_DF_v1['2017']) /  New_Test_DF_v1['2017']

quarterly_market_rankings = New_Test_DF_v1.sort_values('2018 Rank', ascending=True)

# quarterly_market_rankings_ppt  
quarterly_market_rankings_ppt_v1 = quarterly_market_rankings[['2017 Rank', '2018 Rank', 'JLL Market', '2018', 'YoY Change %']].copy()
quarterly_market_rankings_ppt_v2 = quarterly_market_rankings_ppt_v1.head(10)
quarterly_market_rankings_ppt_v3 = quarterly_market_rankings_ppt_v1.head(20)


########################## Most active markets table - Annual ###################################

#convert column headers to string
retail_market_volumes_annual_final.columns = retail_market_volumes_annual_final.columns.map(str)

#remove duplicate markets
retail_market_volumes_annual_final_v2 = retail_market_volumes_annual_final.groupby("JLL Market").sum()

#convert groupby object to pandas dataframe
retail_market_volumes_annual_final_v3 = pd.DataFrame(retail_market_volumes_annual_final_v2)
retail_market_volumes_annual_final_v3.columns = retail_market_volumes_annual_final_v3.columns.map(str)
retail_market_volumes_annual_final_v3
pd.DataFrame(retail_market_volumes_annual_final_v3)

#filter out ALL OTHERS field and convert column headers to string
retail_market_volumes_annual_final_v3 = retail_market_volumes_annual_final_v3[~retail_market_volumes_annual_final_v3.index.isin(['All Others'])]
retail_market_volumes_annual_final_v3.columns = retail_market_volumes_annual_final_v3.columns.map(str)                                                                       
                                                                              
#create new columns based on historical rankings
retail_market_volumes_annual_final_v3['2001 Rank'] = retail_market_volumes_annual_final_v3['2001'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2002 Rank'] = retail_market_volumes_annual_final_v3['2002'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2003 Rank'] = retail_market_volumes_annual_final_v3['2003'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2004 Rank'] = retail_market_volumes_annual_final_v3['2004'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2005 Rank'] = retail_market_volumes_annual_final_v3['2005'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2006 Rank'] = retail_market_volumes_annual_final_v3['2006'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2007 Rank'] = retail_market_volumes_annual_final_v3['2007'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2008 Rank'] = retail_market_volumes_annual_final_v3['2008'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2009 Rank'] = retail_market_volumes_annual_final_v3['2009'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2010 Rank'] = retail_market_volumes_annual_final_v3['2010'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2011 Rank'] = retail_market_volumes_annual_final_v3['2011'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2012 Rank'] = retail_market_volumes_annual_final_v3['2012'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2013 Rank'] = retail_market_volumes_annual_final_v3['2013'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2014 Rank'] = retail_market_volumes_annual_final_v3['2014'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2015 Rank'] = retail_market_volumes_annual_final_v3['2015'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2016 Rank'] = retail_market_volumes_annual_final_v3['2016'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2017 Rank'] = retail_market_volumes_annual_final_v3['2017'].rank(method='dense', ascending=False)
retail_market_volumes_annual_final_v3['2018 Rank'] = retail_market_volumes_annual_final_v3['2018'].rank(method='dense', ascending=False)

#final dataframe
#retail_market_volumes_annual_final_v3



###################################JOSH Volumes#################################################################
################################################################################################################

#Extract year and add column
josh_volumes_df['Year'] = josh_volumes_df['YYYYQQ'].str[:4]
#Extract quarter and add column
josh_volumes_df['Quarter'] = josh_volumes_df['YYYYQQ'].str[-2:]

#calculating retail investment volumes
josh_retail_volumes = josh_volumes_df.pivot_table(index=["Year"],values=["Retail"],
               columns=["Quarter"],aggfunc=[np.sum],fill_value=0)

###Shift pivot to normal dataframe
josh_retail_volumes.columns = josh_retail_volumes.columns.droplevel(0)
josh_retail_volumes.columns = josh_retail_volumes.columns.droplevel(0)
josh_retail_volumes.columns.name = None               #remove categories
josh_retail_volumes_billions = josh_retail_volumes.reset_index() 

josh_retail_volumes_billions['Q1'] = josh_retail_volumes_billions['Q1'].str.replace(',', '')
josh_retail_volumes_billions['Q2'] = josh_retail_volumes_billions['Q2'].str.replace(',', '')
josh_retail_volumes_billions['Q3'] = josh_retail_volumes_billions['Q3'].str.replace(',', '')
josh_retail_volumes_billions['Q4'] = josh_retail_volumes_billions['Q4'].str.replace(',', '')

josh_retail_volumes_billions.set_index('Year', inplace=True)

josh_retail_volumes_billions_v1 = josh_retail_volumes_billions[['Q1', 'Q2', 'Q3', 'Q4']].astype(float) / 1000000000

josh_retail_volumes_billions_v1 = josh_retail_volumes_billions_v1.fillna(0)

# josh_retail_volumes_billions_v1



################################### INVESTOR RANKING, annual and quarterly #####################################
################################################################################################################

# Investor by Investor Annual Summary
investor_rank_df = retail_buyer_df.pivot_table(index=["Name"],values=['JV_Price'],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

#Convert investor by investor annual summary
investor_rank_df.columns = investor_rank_df.columns.droplevel(0)
investor_rank_df.columns = investor_rank_df.columns.droplevel(0)
investor_rank_df.columns.name = None               #remove categories
investor_rank_df_final = investor_rank_df.reset_index()  

#programattic sort of last column (most recent time period)
investor_rank_df_final_v2 = investor_rank_df_final.sort_values(investor_rank_df_final.columns[-1], ascending = False)


#Add in column that concatenates Quarter and Investor Name for better table parsing
retail_buyer_df["QQ_Name"] = retail_buyer_df["Quarter"].map(str) + "_" + retail_buyer_df["Name"]

# Investor by Investor Annual Summary
investor_rank_df_qtrs = retail_buyer_df.pivot_table(index=["Name", "QQ_Name", "Quarter"],values=['JV_Price'],
               columns=["Year of transaction"],aggfunc=[np.sum],fill_value=0)

#Convert investor by investor quarterly summary
investor_rank_df_qtrs.columns = investor_rank_df_qtrs.columns.droplevel(0)
investor_rank_df_qtrs.columns = investor_rank_df_qtrs.columns.droplevel(0)
investor_rank_df_qtrs.columns.name = None               #remove categories
investor_rank_df_qtrs_final = investor_rank_df_qtrs.reset_index()  


#investor_rank_df_final_v2
#investor_rank_df_final
#investor_rank_df
#investor_rank_df_qtrs_final


###################### Primary v Secondary v Tertiary ##################################
########################################################################################

#MarketType Annual Summary
market_type_volumes_annual = retail_full_df.pivot_table(index=["Year of transaction"],values=["Price ($)"],
               columns=["MarketType"],aggfunc=[np.sum],fill_value=0)


#Convert MarketType annual summary to normal DF
market_type_volumes_annual.columns = market_type_volumes_annual.columns.droplevel(0)
market_type_volumes_annual.columns = market_type_volumes_annual.columns.droplevel(0)
market_type_volumes_annual.columns.name = None               #remove categories
market_type_volumes_annual_v2 = market_type_volumes_annual.reset_index()
market_type_volumes_annual_v2

#MarketType Quarterly Summary
market_type_volumes_qtrly = retail_full_df.pivot_table(index=["Quarter of transaction"],values=["Price ($)"],
               columns=["MarketType"],aggfunc=[np.sum],fill_value=0)

#convert MarketType quarterly summary
market_type_volumes_qtrly.columns = market_type_volumes_qtrly.columns.droplevel(0)
market_type_volumes_qtrly.columns = market_type_volumes_qtrly.columns.droplevel(0)
market_type_volumes_qtrly.columns.name = None               #remove categories
market_type_volumes_qtrly_v2 = market_type_volumes_qtrly.reset_index()

#Extract year and add column
market_type_volumes_qtrly_v2['Year'] = market_type_volumes_qtrly_v2['Quarter of transaction'].str[:4]
#Extract quarter and add column
market_type_volumes_qtrly_v2['Quarter'] = market_type_volumes_qtrly_v2['Quarter of transaction'].str[-2:]

#add total figure
market_type_volumes_annual_v2['Total'] = (market_type_volumes_annual_v2['Primary'] + market_type_volumes_annual_v2['Secondary']) +  market_type_volumes_annual_v2['Tertiary']
market_type_volumes_annual_v2['Primary %'] = (market_type_volumes_annual_v2['Primary'] / market_type_volumes_annual_v2['Total'])
market_type_volumes_annual_v2['Secondary&Tertiary %'] = ((market_type_volumes_annual_v2['Secondary'] + market_type_volumes_annual_v2['Tertiary']) / market_type_volumes_annual_v2['Total'])
market_type_volumes_annual_v2['Secondary %'] = (market_type_volumes_annual_v2['Secondary'] / market_type_volumes_annual_v2['Total'])
market_type_volumes_annual_v2['Tertiary %'] = (market_type_volumes_annual_v2['Tertiary'] / market_type_volumes_annual_v2['Total'])
# market_type_volumes_annual_v2



###################### Historical Cap Rate Visual ##############
retail_cap_rates_overall_v2 = retail_cap_rates_overall.set_index('Market Type').transpose()
retail_cap_rates_overall_v2
retail_cap_rates_overall_v3 = retail_cap_rates_overall_v2.iloc[2:]
retail_cap_rates_overall_v4 = retail_cap_rates_overall_v3[['Primary', 'Ten-Year Treasury', 'Secondary']]
#main dataframe
# retail_cap_rates_overall_v4


###################### Historical Cap Rate RANGES ##############

cap_rates_overall_range = cap_rates[~cap_rates['Market'].isin(['Overall', 'Ten-Year Treasury'])]

retail_cap_rates_overall_range = cap_rates_overall_range[cap_rates_overall_range['Sector'].isin(['Retail'])]
retail_cap_rates_overall_range_primary = retail_cap_rates_overall_range[retail_cap_rates_overall_range['Market Type'].isin(['Primary'])]
retail_cap_rates_overall_range_secondary = retail_cap_rates_overall_range[retail_cap_rates_overall_range['Market Type'].isin(['Secondary'])]

# min and max values
retail_primary_max = retail_cap_rates_overall_range_primary.agg({'max'})
retail_primary_min = retail_cap_rates_overall_range_primary[retail_cap_rates_overall_range_primary > 0].agg({'min'})

retail_secondary_max = retail_cap_rates_overall_range_secondary.agg({'max'})
retail_secondary_min = retail_cap_rates_overall_range_secondary[retail_cap_rates_overall_range_secondary > 0].agg({'min'})

#concatenates seperated primary & secondary DFs
retail_cap_rate_ranges_overall = pd.concat([retail_primary_max, retail_primary_min, retail_secondary_max, retail_secondary_min])

#removes erronious columns that were held inplace through primary & secondary separation
retail_cap_rate_ranges_overall.drop(retail_cap_rate_ranges_overall.columns[[0, 1]], axis=1, inplace=True)

#concatenates new column to set as index to help with row subtraction
retail_cap_rate_ranges_overall['index'] = retail_cap_rate_ranges_overall.index+retail_cap_rate_ranges_overall['Market Type']
retail_cap_rate_ranges_overall_v2 = retail_cap_rate_ranges_overall.set_index('index')

#remove remaining string columns
retail_cap_rate_ranges_overall_v2.drop(retail_cap_rate_ranges_overall.columns[[0]], axis=1, inplace=True)

#add in primary & secondary diff column
retail_cap_rate_ranges_overall_v2.loc['primary_diff'] = retail_cap_rate_ranges_overall_v2.loc['maxPrimary'] - retail_cap_rate_ranges_overall_v2.loc['minPrimary']
retail_cap_rate_ranges_overall_v2.loc['secondary_diff'] = retail_cap_rate_ranges_overall_v2.loc['maxSecondary'] - retail_cap_rate_ranges_overall_v2.loc['minSecondary']
retail_cap_rate_ranges_overall_v3 = retail_cap_rate_ranges_overall_v2.reindex(['minPrimary', 'maxPrimary', 'primary_diff', 'minSecondary', 'maxSecondary', 'secondary_diff'])


#main DFs
#retail_cap_rate_ranges_overall_v3


############################## Write data to excel file ###############


#Write dataframe manipulations to excel file
writer = pd.ExcelWriter('USIO_DataBook_retail.xlsx')

#Josh's overall volumes
josh_volumes_df.to_excel(writer, 'Josh Overall Volumes - all')

#Josh's volumes
josh_retail_volumes_billions_v1.to_excel(writer, 'Josh Overall Volumes - retail')

#High level retail volumes
retail_volumes_final.to_excel(writer, 'Lantern Overall Volumes')

#primary v secondary v tertiary - annual
market_type_volumes_annual_v2.to_excel(writer, 'MarketType Comparison - Annual')

#primary v secondary v tertiary - quarterly
market_type_volumes_qtrly_v2.to_excel(writer, 'MarketType Comparison - Qtrly')

#Volume slices
retail_single_asset_volumes_final.to_excel(writer, 'Single Asset Volumes')
retail_recap_volumes_final.to_excel(writer, 'Recap Volumes')
retail_port_volume_final.to_excel(writer, 'Portfolio Volumes')

#Market by market volumes
retail_market_volumes_qtrly_final.to_excel(writer, 'Market Volumes Qtrly')
retail_market_volumes_annual_final.to_excel(writer, 'Market Volumes Annual')

#Product volumes
retail_product_volumes_annual_final.to_excel(writer, 'Product Volumes Annual')

#buyer volumes
buyer_volumes_final_v3.to_excel(writer, 'Buyer Breakout Annual')

#regional/country volumes analysis
regional_country_volumes_final.to_excel(writer, 'Region_Country_Annual')
regional_country_volumes_QQ_final.to_excel(writer, 'Region_Country_QQ')
regional_volumes_final.to_excel(writer, 'Region_Volumes_Annual')
regional_volumes_QQ_final.to_excel(writer, 'Region_Volumes_QQ')

regional_country_volumes_market_final.to_excel(writer, 'Region_Country_MKT_Annual')
regional_country_volumes_QQ_market_final.to_excel(writer, 'Region_Country_MKT_QQ')
regional_volumes_market_final.to_excel(writer, 'Region_Market_Annual')
regional_volumes_QQ_market_final.to_excel(writer, 'Region_Market_QQ')

#percentage breakout
regional_volumes_final_transform.to_excel(writer, 'Annual_Regional_Percentage')

#Quarterly Markets Ranking - all
quarterly_market_rankings.to_excel(writer, 'Quarterly Market Rankings - All')

#Annual Market Rankings - all
retail_market_volumes_annual_final_v3.to_excel(writer, 'Annual Market Rankings - All')

#Quarterly Markets Ranking PPT table format - top 10
quarterly_market_rankings_ppt_v2.to_excel(writer, 'Qtrly Market Rankings - Top 10')

#Quarterly Markets Ranking PPT table format - top 20
quarterly_market_rankings_ppt_v3.to_excel(writer, 'Qtrly Market Rankings - Top 20')

#Annual Investor Ranking
investor_rank_df_final_v2.head(500).to_excel(writer, 'Investor Ranking - Annual')

#historical cap rates
retail_cap_rates_overall_v4.to_excel(writer, 'Annual Cap Rates')

#historical cap rate ranges
retail_cap_rate_ranges_overall_v3.to_excel(writer, 'Cap Rate Range History')
#Quarterly investor breakout ### Increases file size significantly
# investor_rank_df_qtrs_final.head(2000).to_excel(writer, 'Investor Ranking - Quarterly')

writer.save()




################ Send ppt slide as email attachment #################################
#####################################################################################

import win32com.client as win32
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'xxx.xxx@am.jll.com' 
mail.Subject = 'USIO Retail Data Book'
mail.Body = 'See attached for your quarterly USIO Data Book for the retail sector'

# To attach a file to the email (optional):
attachment  = r"C:\Users\David.Hoebbel\Desktop\Projects\5. Data Requests\2018.06.12_USIO Python Automation\USIO_DataBook_retail.xlsx"
mail.Attachments.Add(attachment)

mail.Send()

