# 如何使用git克隆仓库

## 1\. 初始化 Git 仓库

&#x20;   cd \~/ros2\_ws\_gazebo
    git init


## 2\. 配置 .gitignore 文件

&#x20;   touch.gitignore

    将以下内容添加到.gitignore 文件中：

    build/
    install/
    log/

    这些文件都是编译生成的临时文件和环境缓存，不应该被纳入版本管理。


## 3\. 保存本地仓库

&#x20;   git status # 查看当前仓库状态
    git add . # 添加所有文件到暂存区
    git commit -m "Initial commit" # 提交本地仓库
    

注意：以上命令是在本地仓库进行的操作，并没有与远程仓库进行交互。

## 4\. 克隆远程仓库

### 第一步，先在github上创建一个空仓库。

### 第二步，在本地仓库中执行以下命令：

&#x20;   git remote add origin https://github.com/你的用户名/ros2\_ws\_gazebo.git
    # 注意：origin 是远程仓库的别名，可以自定义。


### 第三步，执行以下命令：

&#x20;   git push -u origin master # 推送本地仓库到远程仓库

    后面只需要在终端输入：git push 即可将代码推送到远程仓库。

