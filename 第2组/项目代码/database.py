""" 
根据 tsg.txt 构建图书关系图
已完工
""" 

import re 
from py2neo import Graph
from py2neo import Node, Relationship
# from n06_basis_of_neo import CreateNodes, subclassRelationship

## 1 启动数据库
graph = Graph("http://localhost:7474",username="neo4j", password="1234")

## 1 读取文本数据
lib=[]
count = 0
#------------------------------------------------------------------此处修改路径-----------------------------------------------------------------------
with open(r"C:\Users\Desjajja\Documents\Workspace\Python\AdvancedBootCamp\Code\Team_2_temp\data\tsg.txt", encoding='utf-8', errors='ignore') as f:
#-------------------------------------------------------------------到这里为止------------------------------------------------------------------------    
    for line in f.readlines():
        if count != 0:
            rela_array = line.strip("\n").strip(" ").split("，")
            lib.append(rela_array)
            count += 1
        else: 
            count += 1
            continue
print("完成读取信息，总共读取%s条\
    "%(count-1))
print("******************************")


# 2 批量创建节点和关系
#---------------------------------------------------该函数实现创建含有四个properties的单个节点的功能--------------------------------------------------------------
def CreateNode4Pro(className, value_list):

    # 指定节点类、名字
    # 创建节点

    test_node= Node(className, Name = value_list[0], author=value_list[1],\
        series_num=value_list[2],site="".join(value_list[3].strip()))
    graph.create(test_node)
#--------------------------------------------------------------------到此为止-----------------------------------------------------------------------------------
#----------------------------------------------------------以书名，馆藏地为键值对返回一个字典---------------------------------------------------------------------
def siteDict(node_list,bookDict):
    i = 0
    for i in range(len(node_list)):
        book = node_list[i]
        bookDict[book[0]] = book[3].strip()
    return bookDict
#---------------------------------------------------------------------到此为止----------------------------------------------------------------------------------


#-----------------------------------------------------------调用单节点创建方法，批量创建节点，并打印创建数量-------------------------------------------------------------------
def CreateNodes(ClassName, node_list):

    # 批量创建节点

    nums = 0
    for nums in range(len(node_list)):
        CreateNode4Pro(ClassName,node_list[nums])
        nums+=1
    print("创建节点成功，总计创建%s个\
        "%(nums))
    print("******************************")
#----------------------------------------------------------------------------到此为止--------------------------------------------------------------------------------------    
#----------------------------------------------创建馆藏实体，sites，同时生成以出现过的以馆藏地、是否出现过（1或0）位键值对的字典-------------------------------------------------
def CreateSites(bookDict):
    countDict = {}
    for i in bookDict.values():
        if countDict.get(i) == None:
            n = Node('Sites', siteName=i)
            graph.create(n)
            countDict[i] = 1
        else:
            continue
    print("创建馆藏点成功，总共创建%s个\
        "%(len(countDict.keys())))
    print("******************************")
#----------------------------------------------------------------------------创建关系-------------------------------------------------------------------------------------
def CreateRelation():
    graph.run('Match(L:Library) match (S:Sites) \
            where (L.site = S.siteName)\
            create(L)-[:藏于]->(S)')
    print("成功创建馆藏数据库")

#----------------------------------------------------------------------------开始执行--------------------------------------------------------------------------------------
def main():
    bookDict = {}
    CreateNodes('Library',lib)
    siteDict(lib, bookDict)
    CreateSites(bookDict)
    CreateRelation()

#-------------------------------------------------------------------------主函数入口-------------------------------------------------------------------
if __name__ == "__main__":
    main()

