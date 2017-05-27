# coding=utf-8
"""
民族首页搜索：
//视频栏 rc:label1=990000 type=1 mediaAlbum:type=1 state=DOWN
List<MediaAlbum> videoMediaAlbumList = rcSearchService.findTopVideoAlbumByRc(5, LABEL1_990000);
//音频栏 rc:label1=990000 type=1 mediaAlbum:type=2 state=DOWN
List<MediaAlbum> audioMediaAlbumList = rcSearchService.findTopAudioByRc(5, LABEL1_990000);
//图片栏 rc:label1=990000 type=2 imageAlbum:state=DOWN
List<ImageAlbum> imageAlbumList = rcSearchService.findTopImageAlbumByRc(4, LABEL1_990000);
//文档栏 rc:label1=990000 type=3 document:state=DOWN
List<Document> documentList = rcSearchService.findTopDocumentByRc(8, LABEL1_990000);
机构首页搜索：

"""
import pymongo
from elasticsearch import Elasticsearch


def get_collection(collection):
    # 选择集合（mongo中collection和database都是延时创建的）
    coll = db[collection]
    return coll


def insert_one_doc(db):
    # 插入一个document
    coll = db['informations']
    information = {"name": "quyang", "age": "25"}
    information_id = coll.insert(information)
    print information_id


def insert_multi_docs(db):
    # 批量插入documents,插入一个数组
    coll = db['informations']
    information = [{"name": "xiaoming", "age": "25"}, {"name": "xiaoqiang", "age": "24"}]
    information_id = coll.insert(information)
    print information_id


def get_one_doc(coll):
    # 有就返回一个，没有就返回None
    print coll.find_one()  # 返回第一条记录
    # print coll.find_one({"name": "quyang"})
    # print coll.find_one({"name": "none"})


def get_one_by_id(coll, doc_id):
    # 通过document id来查找一个doc
    import bson
    return coll.find_one({"_id": bson.ObjectId(str(doc_id))})


def get_many_docs(db):
    # mongo中提供了过滤查找的方法，可以通过各种条件筛选来获取数据集，还可以对数据进行计数，排序等处理
    coll = db['informations']
    # ASCENDING = 1 升序;DESCENDING = -1降序;default is ASCENDING
    for item in coll.find().sort("age", pymongo.DESCENDING):
        print item

    count = coll.count()
    print "集合中所有数据 %s个" % int(count)

    # 条件查询
    count = coll.find({"name": "quyang"}).count()
    print "quyang: %s" % count


def clear_all_datas(db):
    # 清空一个集合中的所有数据
    db["informations"].remove()


client = pymongo.MongoClient(host="192.168.0.115", port=27017)
db = client['xfile']
mediaAlbum = db['mediaAlbum']
es = Elasticsearch('192.168.0.115')
mediaAlbums_mongo = db['mediaAlbum'].find({'label1': 990000})
for i in mediaAlbums_mongo:
    print i['title']
a = get_one_by_id()
mediaAlbums_es = es.search('media-album-index', 'media-album', {"query": {"match": {'label1': 990000}}})
for i in mediaAlbums_es['hits']['hits']:
    print i['_source']['title']
