import pymongo

myClient = pymongo.MongoClient('')

accountDb = myClient['f_account']

commissDetailsimplCol = accountDb['commissdetailsimpl']

accountData = commissDetailsimplCol.find_one({"vo.tag_id" : '1810685'})
print(accountData)

# accountData = commissDetailsimplCol.find()
#
# for i in accountData:
#     print(i)


