#### 使用

​		本程序需需支持python3，使用时需要有源文件与GCC生成的文本抽象语法树。默认状态下为对test目录中的所有测试文件进行测试，若需指定单个文件，将程序最外层的for循环移除，并在代码开头部分指定文件名即可。

​		需要安装python3，画图需要安装graphviz。win下请注释掉程序最后的两个系统调用，利用生成的.dot文件使用grapviz画图即可。

#### 文件说明

​		没有后缀的文件均为中间文件，可以忽略。
示例
![img](https://github.com/0Xerath0/CFG/blob/main/test/test1.c.png)
