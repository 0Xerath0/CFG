import re,os
from re import *
path = os.getcwd()

testPath = path+"/test/"
SourceFiles = sorted(os.listdir(testPath))
os.chdir(testPath)
for i in os.listdir(testPath):
    if i[-2:] != ".c":
        SourceFiles.remove(i)  

SourceFiles.sort()

for src in SourceFiles:
    source_file_name=src
    #源文件文件名
    tu_file_name=source_file_name+".001t.tu"
    #gcc生成的tu文件文件名
    normal_AST_file_name="normal_AST"
    #保存规范化AST的文件名
    finalAST = source_file_name + ".finalAST"
    #保存最终化简后的AST
    dot_file_name = source_file_name + ".dot"
    #保存用于生成图像的dot文件
    png_file_name = source_file_name + ".png"
    pdf_file_name = source_file_name + ".pdf"
    symbol_of_useful="srcp:"+source_file_name
    useful_nodes="useful_nodes"

    with open(tu_file_name, "r") as f_in:
        l = f_in.readlines()

        cnt = len(l)
        #统计行数

        with open(normal_AST_file_name,"w") as f_out:
            for i in range(cnt):
                tmp=l[i]
                tmp=re.sub('\s*:\s*' , ':', tmp)
                #将与空格相连的冒号替换为无空格冒号
                #min,max,low等关键词之后的冒号前后均有空格，也需将其替换为无空格的冒号
                tmp=re.sub('\s*\n', '' ,tmp)
                #部分行结尾时为一些空格再加上换行符，若以"\s+"模式去匹配，则若其后一行并非新结点，则开头亦为空格，最后仍有一部分两个空格相连的情况，
                #而若其后一行为一个新的结点，则依照本程序的规定，该行行末会输出一个换行符，不会与下一个信息相连
                tmp=re.sub('\s+', ' ', tmp)
                #将多个空格更换为单个

                
                if i<cnt-1 and l[i+1][0] == '@':
                #以“@”符号开头的行即为一个节点信息的起始，若该行的下一行为一个新节点，则该行输出后应有换行符
                    #print(tmp)
                    f_out.write(tmp+"\n")
                else:
                #若不以“@”符号开头，则其应为上个节点的延续信息，不输出换行符
                    f_out.write(tmp)
                    #print(tmp,end="")
        f_out.close()
            
    f_in.close()
    #对tu文件进行规范化处理

    with open(normal_AST_file_name,"r") as f_in:
        is_useful=[]
        #用于标记结点是否有用的数组，0为待定，1为无用，3为有用
        l=f_in.readlines()
        cnt=0
        #统计规范化后行数
        for i in l:
            cnt+=1
            is_useful.append(int(0))

        really_useful=[]
        not_useful=[]
        #保存有用节点和无用节点

        for i in range(cnt):
            searchObj = re.search("srcp:\S*",l[i])
            #先找到包含关键字“srcp”的结点
            if searchObj :
            #找到后再考虑其是否为“srcp:+文件名”
                if re.search(symbol_of_useful,l[i]):
                    is_useful[i]=3
                    #若是，则其为有用节点
                else:
                    is_useful[i]=1
                    #否则标记为无用结点

        for i in l:
            tmp = re.findall("@\d+",i)
            if tmp:
                father_node = int(tmp.pop(0).replace("@","")) - 1
                #该结点本身标号
                if is_useful[father_node] == 3:
                    for j in tmp:
                        one_child_of_useful=int(j.replace("@","")) - 1
                        #有用结点的子结点，若其为待定结点则也将转变为有用节点
                        is_useful[one_child_of_useful] = 3
                
                elif is_useful[father_node] == 1:
                    for j in tmp:
                        one_child_of_useful=int(j.replace("@",""))-1
                        #无用结点的子结点，若其为待定结点则也将转变为有用节点
                        is_useful[one_child_of_useful] |= 1

            
        
        for i in l:
            searchObj = re.search("call_expr",i)
            if searchObj:
                tmp = re.findall("@\d+",i)
                tmp.pop(0)
                for j in tmp:
                    one_child_of_useful=int(j.replace("@",""))-1
                    is_useful[one_child_of_useful] = 3
        #遍历call_expr结点并将其子结点标记为有用结点



        for i in range(len(l)):
            if is_useful[i] == 3:
                really_useful.append(l[i])
                #将所有的有用结点存入一个list中



    f_in.close()
    #所有有用节点的信息

    cnt = len(really_useful)

    for i in range(cnt) :
        
        if re.search("\S*_type\\b",really_useful[i]):
            really_useful[i]=""
        #若此结点含有_type字段，即为简单类型结点

        if re.search("\\bidentifier_node\\b",really_useful[i]):
            really_useful[i]=re.sub("\\blngt:\d+","",really_useful[i])
            #若一个节点中含有identifier_node字段，则其为标识符结点，删除标识符长度信息

        if re.search("\\bscope_stmt\\b",really_useful[i]):
            tmp=really_useful[i].split(" ")
            for j in range(len(tmp)):
                if not re.search("'begin'|'end'|'next'|'line'",tmp[j]):
                    tmp[j]=""
            #删除该类节点中非此四类字段

            tmp2=[]
            for j in tmp:
                if j:
                    tmp2.append(j)
            #保留未被删除的字段
            
            really_useful[i]=" ".join(tmp2)
            #以空格链接这些字段

        
        really_useful[i]=re.sub("\\bsrcp:\S*","",really_useful[i])
        really_useful[i]=re.sub("\\balgn:\S*","",really_useful[i])
        #删除所有srcp和algn字段
        

        


    #将有用结点存入文件中
    with open(useful_nodes,"w") as f_out:
        whole_file = ""
        for i in really_useful:
            if i:
                whole_file += i
        whole_file = re.sub("op\s*","op",whole_file)
        f_out.write(whole_file)

    f_out.close()            
        



    with open(useful_nodes , "r") as f_in:
        
        whole_file=f_in.read()

        f_in.seek(0,0)
        l = f_in.readlines()
        cnt = 0
        for i in l:
            if i and i!="\n":
                cnt += 1
                num = re.match("@\d+",i).group()
                whole_file = re.sub(num, "#"+str(cnt),whole_file)
                #先用井号表示，方便下一步
        
        whole_file = whole_file.split(" ")
        for j in range(len(whole_file)):
            if re.search("@\d+",whole_file[j]):
                whole_file[j]=""
            elif re.match("#\d+",whole_file[j]):
                whole_file[j] ="\n"+whole_file[j]

        whole_file = " ".join(whole_file)
        whole_file = re.sub("#","@",whole_file)
        whole_file = re.sub("\n","",whole_file,1)


    f_in.close()

    with open(finalAST,"w") as f_out:
        f_out.write(whole_file)

    f_out.close()

    #CFG块内结点定义
    class CFGnode:
        def __init__(self,name,num):
            self.name = name
            self.num = num
        
        pass

    #CFG块的定义
    class CFGblock:
        def __init__(self) -> None:
            self.nodes = []
            self.children = []
            self.num = 0
            self.visited = 0
            self.printed = 0
        
        def insertChild(self,newCFGblock):
            self.children.append(newCFGblock)

        def isleaf(self):
            if self.children:
                return True
            else:
                return False

        def insertNode(self,newNode):
            self.nodes.append(newNode)

    class Table:
        def __init__(self):
            self.list = []

        def insert(self,num,CFGblock):
            self.list.append((num,CFGblock))

        def check(self,num):
            for i in self.list:
                if i[0] == num:
                    return i[1]

            return None
        #检查table中是否存在该标号，若存在则返回其cfg块的指针，否则返回假

    def getNum(str):
        numList = re.findall("@\d+",str)
        for i in range(len(numList)):
            numList[i] = int(numList[i].replace("@","")) -1

        return numList

    def getName(str):
        return str.split(" ")[1]

    gotoTable = Table()

    lableTable = Table()
    entry = CFGblock()
    entry.insertNode("entry")
    exit = CFGblock()
    exit.insertNode("exit")
    cfg_block = CFGblock()
    curCFG = CFGblock()
    curCFG = cfg_block
    entry.insertChild(cfg_block)
    cnt = 1

    NodeList=[]
    with open(finalAST,"r") as f:
        NodeList = f.readlines()
    f.close()





    def createCFG(node):
        global curCFG,exit, NodeList, cnt
        
        name = getName(node)
    
        if name == "function_decl" or name =="bind_expr":
            curCFG.insertNode(node.split(" ")[0]+node.split(" ")[1])
            if re.search("body",node):
                createCFG(NodeList[getNum(re.search("body:@\d+",node).group())[0]])
            
        elif name == "goto_expr":
            cnt+=1
            curCFG.insertNode(node.split(" ")[0]+node.split(" ")[1])
            labl = getNum(re.search("labl:@\d+",node).group())[0] 

            if lableTable.check(labl)!= None:
                curCFG.insertChild(lableTable.check(labl))
            else:
                gotoTable.insert(labl,curCFG)

            curCFG = None
            
        elif name == "label_expr":
            cnt+=1
            newCFG = CFGblock()
            newCFG.insertNode(node.split(" ")[0]+node.split(" ")[1])
            curCFG.insertChild(newCFG)
            curCFG = newCFG
            labl = getNum(re.search("name:@\d+",node).group())[0] 
            lableTable.insert(labl,curCFG)
            
            if gotoTable.check(labl) != None:
                gotoTable.check(labl).insertChild(curCFG)
                for i in range(len(gotoTable.list)):
                    if gotoTable.list[i][0] == labl:
                        del gotoTable.list[i]
            
        elif name == "statement_list":
            cnt+=1
            Nums = getNum(node)
            del Nums[0]
            for i in Nums:
                if curCFG == None:
                    newCFG = CFGblock()
        
                    curCFG = newCFG
                createCFG(NodeList[i])
                
        elif name == "cond_expr":
            condStart = curCFG
            cnt+=1
            opcnt = 0
            curCFG.insertNode(node.split(" ")[0]+node.split(" ")[1])
            curCFG.insertNode(getName(NodeList[getNum(re.search("op{}:\S*".format(opcnt),node).group())[0]]))
            opcnt += 1
            curCFG = None
            newCFG = CFGblock()
            curCFG = newCFG
            condEnd = CFGblock()
            condEnd.insertNode("CondEnd")
            condStart.insertChild(curCFG)
            
            
            #newCFG.insertChild(condEnd)

            
            

            createCFG(NodeList[getNum(re.search("op{}:\S*".format(opcnt),node).group())[0]])
            opcnt += 1
            

            if re.search("op{}:\S*".format(opcnt),node):
                opcnt += 1
                newCFG = CFGblock()

                condStart.insertChild(newCFG)
                curCFG = newCFG
                createCFG(NodeList[getNum(re.search("op{}:\S*".format(opcnt-1),node).group())[0]])
                
            for j in condStart.children:
                if j:
                    j.insertChild(condEnd)
                
            curCFG=condEnd

        elif re.search("return_expr",name):
            curCFG.insertChild(exit)
            curCFG.insertNode(node.split(" ")[0]+node.split(" ")[1])


        elif re.search("expr",name):
            cnt+=1
            curCFG.insertNode(node.split(" ")[0]+node.split(" ")[1])

    watingList=[]

    for i in NodeList:
        if re.search("function_decl.*body:@\d+",i):
            ASTroot = i
    createCFG(ASTroot)
    cnt = 1

    def BFS():
        global watingList,cnt,dotFile

        
        while watingList:
            tmpstr=""
            CFG = watingList.pop(0)

            l = 1

            while CFG == None:
                CFG = watingList.pop(0)

            if (CFG.visited == 0 and BFStime == 0) or CFG.printed == 0 and BFStime  == 1:
                watingList += CFG.children

            for i in CFG.nodes:
                if i:
                    tmpstr += i +"\\n"

            if BFStime == 0 and CFG.visited == 0:
                dotFile += "\tnode{}[label = \"{}\"]\n".format(cnt,tmpstr)
                CFG.visited = 1
                CFG.num = cnt
                cnt += 1
            elif BFStime == 1 and CFG.printed == 0 :
                CFG.printed = 1
                for j in CFG.children:
                    if j:
                        dotFile += "\tnode{} -> node{};\n" .format(CFG.num,j.num)
                """
                if tmpstr != "":
                    dotFile += "\tnode{}[label = \"{}\"]\n".format(cnt,tmpstr)
                    CFG.num = cnt
                    cnt += 1
                else :
                    CFG.num=-1
            elif CFG.num > 0:
                for j in CFG.children:
                    if j.num>0:
                        dotFile += "\tnode{} -> node{};\n" .format(CFG.num,j.num)
                """
            


    CFG = entry
    watingList.append(CFG)


    dotFile = ""
    dotFile += "digraph CFG {\n" + "\t node [shape = box]"

    BFStime = 0

    BFS()
    watingList = [entry]
    BFStime = 1
    BFS()


    dotFile+="}\n"
    with open(dot_file_name,"w") as f:
        f.write(dotFile)
    f.close()

    generatePNG = "dot -Tpng "+dot_file_name+" -o "+png_file_name
    generatePDF = "dot -Tpdf "+dot_file_name+" -o "+pdf_file_name

    os.system(generatePDF)
    os.system(generatePNG)
