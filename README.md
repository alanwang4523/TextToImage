Mac、Windows、Linux 电脑都可以，只要安装配置好 python 环境(3.x 版本)即可

主要流程如下：
<br/>一、phthon 环境安装配置（只需配置一次，后续生成只执行 二 的流程）：
<br/>1、安装 python 并配置环境变量（否则命令行提示找不到 python），安装教程可参考：https://www.runoob.com/python/python-install.html
<br/>2、配置好后，可以在命令行输入：python --version 命令试下有没有输出版本号，输出了说明装好了
<br/>3、命令行执行：pip3 install Pillow

<br/>
<br/>二、为小说生成图片
<br/>4、命令行进入到 create_img_for_story.py 脚本所在目录（否则提示找不到：create_img_for_story.py）
<br/>        cd C:\Users\Administrator\Desktop\小说图文生成脚本
<br/><br/>5、将要生成图片的小说内容（可以是改文后的）保存到一个 txt 文件，如 /User/AlanWang4523/TextToImage/test/story_1.txt
<br/>6、执行命令行：python create_img_for_story.py <小说文本路径>
<br/>        python create_img_for_story.py C:\Users\Administrator\Desktop\小说图文生成脚本\test\story_1.txt
<br/>(如果是 MacOS 系统，上面命令中的 python 换成 python3)

<br/>三、效果截图
<div align="left">
<img src=./Screenshots/image_out_log.png width=30% />
</div>
<div align="left">
<img src=./Screenshots/image_out_list.png width=30% />
</div>
<div align="left">
<img src=./Screenshots/img_1.png width=30% />
</div>
