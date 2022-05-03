import pymongo
import os



client = pymongo.MongoClient(os.environ["MONGODB_URL"])
pdb = client.People
otp = client.Otp["otp_verification"]
