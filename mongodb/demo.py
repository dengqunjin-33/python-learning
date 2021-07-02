import pymongo

myClient = pymongo.MongoClient('mongodb://data:80zC7dmVeRxETPyE@172.16.10.102:20024')

accountDb = myClient['f_account']

commissDetailsimplCol = accountDb['commissdetailsimpl']

accountData = commissDetailsimplCol.find_one({"vo.tag_id" : '1810685'})
print(accountData)

# accountData = commissDetailsimplCol.find()
#
# for i in accountData:
#     print(i)


