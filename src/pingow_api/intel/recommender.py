from pingow_api  import models as m

########################## NOTE 1 - SUMMARY FOR DUONG ##########################

#### [logic 1] Objective 1, Type 1 (input in based on product categories) :
####                - results found in #Function 4 : recommendation_by_pdt_cat()
#### [logic 2] Objective 1, Type 2 (input in based on names) :
####                - results found in #Function 8 : recommendation_by_shop_names(cust_selected_shop)
#### [logic 3] Objective 2, (match sales assistent) :
####                - results found in #Function 11 : recommend_shop_asst ()

#### please write YOUR OWN CODE to return crowd data.
####            note that crowd data not included in logic because it will lead to <3 returns
####            hence, do return the crowd info as FYI (in mobile display -alerted JQ)

#### Note 2 & 3 contains items that you will need to re-link to
####                                                either mobile or database

########################## NOTE 2 ##############################################

#input from mobile interface (temp : need to replace with actual)
#note: either cust_selected_pdt_cat or #cust_selected_shop will be selected.

#cust_id = 2 #avoid using cust_id = 8 (logic got issue). advise to use 1, 2, 3, 4
#cust_selected_pdt_cat = 3 #or use 9, 1, 2, 3
#cust_selected_shop = 17 #use electronics shop -  1,2,3,12,13,15,16 or watch - 10, 17, 18 , 19, 20
#cust_destination = 17 #use electronics shop -  1,2,3,12,13,15,16 or watch - 10, 18 , 17,19, 20

######################## NOTE 3 ################################################

#A. Assume Database connection established. Import temp database files & libraries
#Note : This is a temporary database, each of the table has to be replaced
#       or connected to the actual table in the tb later on.

#A import libraries
import pandas as pd
#Import Temp Database
#cust_table = pd.read_csv('database_temp/CUST_TABLE.csv', header = 0)

#
# cust_trans_table = pd.read_csv('database_temp/CUST_TRANSACTION_TABLE.csv', header = 0)
# shop_table = pd.read_csv('database_temp/SHOP_TABLE.csv', header = 0)
# shop_ref_table = pd.read_csv('database_temp/SHOP_REFERENCE_TABLE.csv', header = 0)
# sub_cat_table = pd.read_csv('database_temp/SUB_CAT_1.csv', header = 0)
# shop_asst_table = pd.read_csv('database_temp/SHOP_ASST_TABLE.csv', header = 0)
# shop_asst_avail_table = pd.read_csv('database_temp/SHOP_ASST_AVAIL_TABLE.csv', header = 0)
#
#

global cust_trans_table , shop_table , shop_ref_table , sub_cat_table , shop_asst_table , shop_asst_avail_table
def load_data():
    global cust_trans_table , shop_table , shop_ref_table , sub_cat_table , shop_asst_table , shop_asst_avail_table
    cust_trans_table = pd.DataFrame(list(m.CustomerTransaction.objects.all().values()))
    shop_table =  pd.DataFrame(list(m.Shop.objects.all().values()))
    shop_ref_table =  pd.DataFrame(list(m.ShopSubCatReference.objects.all().values()))
    sub_cat_table =  pd.DataFrame(list(m.SubCategory.objects.all().values()))
    shop_asst_table =  pd.DataFrame(list(m.Assistance.objects.all().values()))
    shop_asst_avail_table =  pd.DataFrame(list(m.AssistanceAvail.objects.all().values()))
    #print(shop_ref_table, "ShopSubCatReference pg_shop_subcat_ref")


##################### Note 4 Do not remove anything below here ##################

#################################################################
# Objective 1 of 2: Recommendation of shopnames to the users
#################################################################

#################################################################
# Type 1 of 2: User to input in based on product categories
#################################################################

#A. Business Logics in english, as below - in order of ranking  -

#1. Product Categories : 1 - available , 0 - not available
#2. Wheelchair Friendly :1 - Yes, 0 - No
#                    (Output) Based on rule 1 & 2: return a list of shop names
#                    (Output) Work on this list for the remaining logics

#3. Type of user: New or Existing Customer:
#      - Define by any transaction in the shopnames by this user.
#               (do so by counting the transactions by user in each shop)
#      - Yes - go to path 4A: Score function formula 4A
#                               (based on user only)
#                               (moving avg. of past 3 visits: for each of top 2 store)
#                               (moving avg. of past 3 visits: for the 3rd recommendation)
#                                       (Rationale: So that it return popular but "new" to existing user - more choices)
#      - No - go to path 4B : Score function formula 4B
#                             (base on moving average of
#                                       past 20 transactions (or less) from
#                                       at least 5 different wheelchair users - need)
#                             (average from users)

#4A. Score function for existing users:
#      - return a list of transaction grp by (1) existing user + shop names selected
#      - No. of past visits by users(sum)
#      - Rank by total sum of visits
#      - Top 2 : condition as below:
#                   - at least 2 visits
#                   - if 2 or less visits <=

#      - Return top 2 popular store
#      - Base on shops not from top 2,
#               --> from past 20 transactions or less (moving average)
#               --> return the top from this list

#4B. Score function for New users:
#      - return the list of transactions by at least 5 distinct users
#      - Rank by total sum of visits

#########################start here #############################################
import pandas as pd

#FUNCTION 01
#[1][2] Step 1 - return shop with product category & wheelchair friendly

def shop_matched_pdt_cat(cust_selected_pdt_cat):
    # print ('************************************************')
    shop_selected_pdt_cat = shop_ref_table[shop_ref_table.SUB_CAT_ID == cust_selected_pdt_cat].drop('SUB_CAT_ID', axis = 1)
    # print('----------- shop_selected_pdt_cat --------------')
    # print(shop_selected_pdt_cat)
    shop_shortlisted = pd.merge(shop_table, shop_selected_pdt_cat, how = 'inner', on=['SHOP_ID', 'SHOP_ID'])
    shop_shortlisted2 = pd.DataFrame(shop_shortlisted[shop_shortlisted.W_FRIENDLY =="Y"])
    return shop_shortlisted2

#print(shop_matched_pdt_cat(cust_selected_pdt_cat))

#FUNCTION 02
#[3] total count of transactions by customers by product categories selected
#    rule : only transaction with at least 1 visit, and mean rating >2 is included
def total_trans_by_cust_per_pdt_cat(cust_id, cust_selected_pdt_cat):
    shopper_trans = cust_trans_table[(cust_trans_table.CUSTOMER_ID == cust_id) & (cust_trans_table.SUB_CAT_ID == cust_selected_pdt_cat)]
    shopper_trans_1 = pd.DataFrame(shopper_trans.groupby(shopper_trans.SHOP_ID).SHOP_ID.count())
    shopper_trans_1['Total_Count']= shopper_trans_1.SHOP_ID
    shopper_trans_1['SHOP_ID']= shopper_trans_1.index
    shopper_trans_2 = pd.DataFrame(shopper_trans.groupby(shopper_trans.SHOP_ID).OVERALL_RATE.sum())
    #TO_DO chage to MEAN
    #shopper_trans_2 = pd.DataFrame(shopper_trans.groupby(shopper_trans.SHOP_ID).OVERALL_RATE.mean())
    shopper_trans_2['SHOP_ID']= shopper_trans_2.index
    shopper_trans_3 = pd.merge(shopper_trans_1,shopper_trans_2, how ='inner', on = ['SHOP_ID', 'SHOP_ID'])
    #   Define transactions that are included for comparsion
    #   Check for total visit = 1, if yes; keep. if not = no.
    shopper_trans_final = pd.DataFrame(shopper_trans_3[shopper_trans_3.OVERALL_RATE > 2])
    #print('the shape : ', shopper_trans_final.shape)
    return shopper_trans_final

#print('')
#print(total_trans_by_cust_per_pdt_cat(cust_id, cust_selected_pdt_cat))

#FUNCTION 03
#[3] total score of stores by average rating by product categories selected
def overall_rating_of_shops_by_pdt_type_selected (cust_selected_pdt_cat):
    shops = shop_matched_pdt_cat(cust_selected_pdt_cat)
    overall_rating_trans = pd.merge(shops,cust_trans_table, how = 'inner', on = ['SHOP_ID', 'SHOP_ID'])
    overall_rating_trans = overall_rating_trans[overall_rating_trans.SUB_CAT_ID == cust_selected_pdt_cat]
    # print(">>>overall_rating_trans>>>")
    # print(overall_rating_trans)
    # print(">>>overall_rating_trans.groupby(overall_rating_trans.SHOP_ID.OVERALL_RATE)>>>")
    # print( overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE)
    # print('max')
    # print( overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE.max())
    # print('sum')
    # print( overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE.sum())
    # print('count')
    # print( overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE.count())
    #change to mean() TO_DO
    overall_rating_by_shops = pd.DataFrame(overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE.sum())
    overall_rating_by_shops['SHOP_ID'] = overall_rating_by_shops.index
    overall_rating_by_shops = overall_rating_by_shops.sort_values(by = 'OVERALL_RATE', axis=0, ascending=False)
    return overall_rating_by_shops

#print('')
#print(overall_rating_of_shops_by_pdt_type_selected(cust_selected_pdt_cat))

#FUNCTION 04
#[4] return recommendation
def recommendation_by_pdt_cat(cust_id, cust_selected_pdt_cat):
    load_data()
    y = overall_rating_of_shops_by_pdt_type_selected (cust_selected_pdt_cat)
    z = total_trans_by_cust_per_pdt_cat(cust_id, cust_selected_pdt_cat)
    if z.shape[0] == 0:
        recomm1 = y.iloc[0,1]
        recomm2 = y.iloc[1,1]
        recomm3 = y.iloc[2,1]
    elif z.shape[0] ==1:
        recomm1 = z.iloc[0,0]
        if z.iloc[0,0] == y.iloc[0,1]:
            recomm2 = y.iloc[1,1]
            recomm3 = y.iloc[2,1]
        else:
            recomm2 = y.iloc[0,1]
            recomm3 = y.iloc[2,1] #dirty code
    elif z.shape[0] == 2:
        recomm1 = z.iloc[0,0]
        recomm2 = z.iloc[1,0]
        if z.iloc[0,0] == y.iloc[0,1]:
            recomm3 = y.iloc[2,1]
#            if z.iloc[0.0] ==y.iloc[1,1]:
#                recomm3 = y.iloc[2,1]
        else:
            recomm3 = y.iloc[1,1]
#        elif z.iloc[1,0] ==y.iloc[0,1]:
#            recomm3 = y.iloc[1,1]
#        else:
#            recomm3 = y.iloc[0,1]
    else:
        recomm1 = z.iloc[0,0]
        recomm2 = z.iloc[1,0]
        recomm3 = z.iloc[2,0]

    return [int(recomm1),int(recomm2),int(recomm3)]

# print('logic 1 below - to remove at line 176 - 177')
#print(recommendation_by_pdt_cat())

#################################################################
# Type 2 of 2: User to input in based on shop names
#################################################################

#A. Business Logics in english, as below - in order of ranking  -

#5. Wheelchair Friendly :1 - Yes, 0 - No, and shop with the same product categories
#                    (Output) Based on rule 1 return a list of shop names
#                    (Output) Work on this list for the remaining logics

#6. Count overall shop performance by average rating
#      - Define by any transaction in the shopnames by the same shop categories
#               (do so by counting the transactions by user (assume all wheelchairs) in each shop)

#7. Recommendation:
#      - recommendation 1 - always the selected
#      - recommendation 2 - the top rating not same as recommendation 1
#      - recommendation 3 - the 2nd top rating not same as recommendation 1

#########################start here #############################

### input from mobile in line 23
#Function 5
# [5]   return the shop names based on customer selection Part 1
def shop_matched_shop_name(cust_selected_shop):
    shop_selected = shop_table[shop_table.SHOP_ID == cust_selected_shop]
    return shop_selected

#print(shop_matched_shop_name(cust_selected_shop))

#Function 6
# [5]   return the shop names based on customer selection Part 2
def similar_shop_by_shop_names(cust_selected_shop):

    #Identify the current type of shop by selection
    x = shop_matched_shop_name(cust_selected_shop)
    # print('shop_matched_shop_name(cust_selected_shop)')
    # print(x)
    # print('shop_ref_table.SHOP_ID ')
    # print(shop_ref_table.SHOP_ID)
    # print('x.iloc[0,0]')
    # print(x.iloc[0,4])
    # print('shop_ref_table[shop_ref_table.SHOP_ID == x.iloc[0,0]])', shop_ref_table[shop_ref_table.SHOP_ID == x.iloc[0,4]])
    shop_type_by_pdt_cat = shop_ref_table[shop_ref_table.SHOP_ID == x.iloc[0,4]].drop('SHOP_ID', axis = 1)
    # print('shop_type_by_pdt_cat')
    shop_ID_same_pdt_cat = pd.merge (shop_ref_table, shop_type_by_pdt_cat, how = 'inner', on = ['SUB_CAT_ID', 'SUB_CAT_ID']).drop('SUB_CAT_ID', axis = 1).drop_duplicates('SHOP_ID')
    # print('shop_ID_same_pdt_cat')
    shop_name_same_pdt_cat = pd.merge(shop_ID_same_pdt_cat, shop_table, how = 'inner', on = ['SHOP_ID', 'SHOP_ID'])
    # print('shop_name_same_pdt_cat')
    #shop_name_same_pdt_cat
    return shop_name_same_pdt_cat

#print('###############',similar_shop_by_shop_names())

#Function 7
# [6]   overall_scoring of shops by similar shop names
def overall_rating_of_shops_by_shop_name_selected (cust_selected_shop):
    shops = similar_shop_by_shop_names(cust_selected_shop)
    overall_rating_trans = pd.merge(shops,cust_trans_table, how = 'inner', on = ['SHOP_ID', 'SHOP_ID'])
    #Use SUM
    #overall_rating_by_shops = pd.DataFrame(overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE.mean())
    overall_rating_by_shops = pd.DataFrame(overall_rating_trans.groupby(overall_rating_trans.SHOP_ID).OVERALL_RATE.sum())
    overall_rating_by_shops['SHOP_ID'] = overall_rating_by_shops.index
    overall_rating_by_shops = overall_rating_by_shops.sort_values(by = 'OVERALL_RATE', axis=0, ascending=False)
    return overall_rating_by_shops

#print(overall_rating_of_shops_by_shop_name_selected())

#Function 8
# [7]   match recommendations to users
def recommendation_by_shop_names(cust_selected_shop):
    load_data()
    x = overall_rating_of_shops_by_shop_name_selected(cust_selected_shop)
    shops_selected = x[x.SHOP_ID != cust_selected_shop]

    recomm1 = cust_selected_shop
    recomm2 = shops_selected.iloc[0,1]
    recomm3 = shops_selected.iloc[1,1]
    print('recommendation_by_shop_names', [int(recomm1),int(recomm2),int(recomm3)])
    return [int(recomm1),int(recomm2),int(recomm3)]

# print('logic 2 below - to remove at line 246 - 247')
#print (recommendation_by_shop_names(cust_selected_shop))


#################################################################
# Objective 2 of 2: Recommended Shop Assistant Names
#################################################################

# [1] identify destination
# [2] retrieve transactions with the shop selected
#                   - then; find the mean rating of shop assistant by rating
#                   - theortically should find the recent 5 (moving average, using rolling_mean function)
#                   - due to time constraint, we will use average of all transactions per user ID
# [3] return the shop_assistant availability for shop
#                   - match their availability with the rating school.
#                   - sort available by rating
#                   - theorically should match also the product cat with the SA's skill
#                           - due to time constraint, we will not return since it is mostly 1 to 1
#                           - and also, if shop is selected, there will be nth to match
#                           - in real implmenetation, need to differentate between both
# [4] from those available;
#                   - pick 1 (the top rated)
#                   - in implementation : need to code to take care of "new staff"
#                           - for instance,if not found in transaction, assign a 0 rating
#                   - for those with 0 rating, need to manage by matching skillset.
#                           - current assumption :all staff able to handle wheelchair
#                           - in real implementation, need to do 1 more filter in this

#########################start here #############################
#input from mobile in line 25

#Function 9
#[2] retrieve transactions and calculate SA with rating
def avg_rating_SA_by_des_shop (cust_destination):
    relv_trans =cust_trans_table[cust_trans_table.SHOP_ID == cust_destination]
    relv_SA_rating = pd.DataFrame(relv_trans.groupby(relv_trans.ASST_ID).ASST_SVC_RATE.mean())
    relv_SA_rating['ASST_ID'] = relv_SA_rating.index
    return relv_SA_rating

#print (avg_rating_SA_by_des_shop (cust_destination))

#Function 10
#[3] SA's availability in destination shop
def SA_availability_by_des_shop(cust_destination):
    rel_shop_ass_avail_only = shop_asst_table[shop_asst_table.SHOP_ID == cust_destination]
    rel_shop_ass_avail_only = pd.merge(shop_asst_avail_table,rel_shop_ass_avail_only , how = 'inner', on = ['ASST_ID','ASST_ID'])
    shop_ass_avail = pd.DataFrame(rel_shop_ass_avail_only[rel_shop_ass_avail_only.AVAILABILITY == True])
    return shop_ass_avail

#print (SA_availability_by_des_shop(cust_destination))

#Function 11
#[4] from those that are available, pick the one top rated
def recommend_shop_asst (cust_destination):
    load_data()
    x = SA_availability_by_des_shop(cust_destination)
    y = avg_rating_SA_by_des_shop (cust_destination)

    z = pd.merge(x, y, how = 'inner', on = ['ASST_ID','ASST_ID']).sort_values(by = 'ASST_SVC_RATE', axis=0, ascending=False)
    recomm_SA = z.iloc[0,0]
    return recomm_SA

# print('logic 2 below - to remove at line 307 - 308')
# print (recommend_shop_asst ())
