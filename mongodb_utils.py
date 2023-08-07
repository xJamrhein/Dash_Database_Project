import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["academicworld"]

def get_keywords(univ_id, name):
    faculty = db["faculty"]
    filter = {"affiliation.id": univ_id, "name": name}
    fields = {"keywords.name": 1, "_id": 0}
    cursor = faculty.find(filter, fields)
    keywords_list = []
    for document in cursor:
        keywords = document.get("keywords", [])
        for keyword in keywords:
            keyword_name = keyword.get("name")
            if name:
                keywords_list.append(keyword_name)
    keywords_text = ','.join(keywords_list)
    if not keywords_list:
        return "No Keywords"
    else:
        return keywords_text