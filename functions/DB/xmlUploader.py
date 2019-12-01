from pymongo import MongoClient
import xmltodict
import pprint
import json
import xml.etree.ElementTree as ET

# sets path to connect to DB
def connection_project_path():
    client = MongoClient('localhost', 27017)
    db = client.beat
    posts = db.Project
    return posts

def connection_poi_path():
    client = MongoClient('localhost', 27017)
    db = client.beat
    posts = db.pointOfInterestDataSet
    return posts

def connection_plugin_path():
    client = MongoClient('localhost', 27017)
    db = client.beat
    posts = db.Plugin
    return posts

def uploadXML(xml):
    my_dict = xmltodict.parse(xml)
    posts = connection_project_path()
    result = posts.insert_one(my_dict)

def uploadDataSet(xml):
    client = MongoClient('localhost', 27017)
    db = client.pymongo_test
    my_dict = xmltodict.parse(xml)
    dataSet = db.dataSet
    result = dataSet.insert_one(my_dict)

def uploadPlugin(xml):
    my_dict = xmltodict.parse(xml)
    posts = connection_plugin_path()
    result = posts.insert_one(my_dict)

def retrievePoiInProject():
    poiFileConnection = connection_poi_path()
    listofPois = poiFileConnection.find()
    poiList = []
    for item in listofPois:
        poiList.append(item['PointOfInterestDataSet']['stringHolder']['stringPointOfInterest'])
    return poiList

#B
def retrieveSpecificProject(name):
    projects = connection_project_path()
    projectsList = projects.find()
    list_of_projects = []
    for item in projectsList:
        if name == item['Project']['Project_name']['#text']:
            list_of_projects.append(item)
            # list_of_projects.append(item['Project']['Project_name']['#text']) # gets name of project
    return list_of_projects
#B
def retrieve_list_of_plugin():
    plugins = connection_plugin_path()
    pluginList = plugins.find()

    list_of_plugins = []
    for item in pluginList:
        list_of_plugins.append(item['Plugin']['Plugin_name']['#text'])
    print('hello')
    return list_of_plugins

def retrieve_list_of_projects():
    projects = connection_project_path()
    projectsList = projects.find()

    list_of_projects = []
    for item in projectsList:
        list_of_projects.append(item['Project']['Project_name']['#text'])

    return list_of_projects

def retrieve_selected_project(project_name):
    projects = connection_project_path()
    projectsList = projects.find()

    for item in projectsList:
        if item['Project']['Project_name']['#text'] == project_name:
            return item
def retrieve_selected_plugin(plugin_name):
    plugin = connection_plugin_path()
    pluginList = plugin.find()

    for item in pluginList:
        if item['Plugin']['Plugin_name']['#text'] == plugin_name:
            return item

def retrieve_selected_project_path(project_name):
    projects = connection_project_path()
    projectsList = projects.find()

    for item in projectsList:
        if item['Project']['BinaryFilePath']['#text'] == project_name:
            return item

def delete_selected_project(nameofProject):
    projects = connection_project_path()
    myquery = {"Project.Project_name.#text": nameofProject}
    projects.delete_one(myquery)

def delete_selected_plugin(nameofProject):
    plugins = connection_plugin_path()
    myquery = {"Plugin.Plugin_name.#text": nameofProject}
    plugins.delete_one(myquery)

# holder element of where to place xml2
def xmlmerger(holder, xml1, xml2):
    print("+++++++++++++++++++++++++++++++++++++++++++++++")
    for element1 in xml1.findall(holder):
        element1.append(xml2)
    ET.dump(xml1)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')

    for elem in xml1:
        for subelem in elem:
            print(subelem.text)

    print('debuggin')
    print("+++++++++++++++++++++++++++++++++++++++++++++++")
    return xml1