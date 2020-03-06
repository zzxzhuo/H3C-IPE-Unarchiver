# H3C IPE Unarchiver

##### 基于Python编写的IPE文件解包程序



<h4 style="color:red">注意：该项目当前仍处于开发状态，在未验证bin文件完整性前请暂时不要将拉取的文件直接应用到网络设备中</h4>

该项目实现了无须使用指定设备，将经过打包的设备bin文件提取出ipe压缩档案。拥有完整的bin文件可以用于救援因误格式化闪存后缺失系统文件而无法启动的H3C网络设备，特别是没有备用设备可用于解包ipe文件的情况。



#### 系统要求

* RAM > 256MB (解包时，需要可用运行内存大于ipe文件本身)
* Python (Version >= 3.7.0)



#### 如何使用

```
python3 unarchive_ipe.py xxxx.ipe
```

解压后的文件会存储于同目录中的`out`文件夹下



#### 许可

GPLv3