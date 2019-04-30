## 简介
Tiger_MAX是一个hadoop大数据集群管理工具，包含以下功能：
* 大数据集群主机初始化


## 安装
1. 克隆代码
```
git clone https://github.com/TigerTORA/Tiger-Max.git /user/local/tiger
ln -sv /usr/share/tiger/Tiger_max.py  /usr/bin/Tiger_max
```

2. 安全必要的依赖包
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py; python get-pip.py
pip install paramiko pexpect prettytable
```
3. 创建主机列表文件(/etc/hosts_list)文件
```
 * 此文件默认路径: /etc/hosts_list
 * 支持注释,任意行首#时,此行内容不被读取
 * 文件每行定义一个主机相关信息(ip,port,user,passwd,pkey),其中pkey为ssh使用key认证时,私钥文件的绝对路径
 * 每行多个字段之间以一个空格隔开,字段内容由冒号定义属性. 例如: ip:192.168.1.10 port:22 pkey:/opt/id_rsa
 * 除ip字段外,其它属性都有默认值,可不填写.
 * ip [必填项]可以是ip和fqdn. 例: ip:192.168.1.10 或: ip:node1.bw-y.com
 * port [可选项]调用ssh所需端口号. 例: port:1022 默认值: port:22
 * user [可选项]调用ssh所需用户名. 例: user:bw_y 默认值: user:root
 * passwd [可选项]调用ssh所需密码. 例: passwd:ssh_password 默认值: passwd:key(使用pkey对应的值,passwd不等于key时,则直接使用密码)
 * pkey [可选项]调用ssh所需私钥. 例: pkey:/opt/pro/id_rsa 默认值: 当前用户家目录下的.ssh目录中的id_rsa, 此文件不存在时直接报错.
 ```
## 具体使用
### 1.大数据集群主机初始化
#### 00.初始化集群服务器
  * 必要软件包检测
  * step(0):Plesse keyin the NTP server hostname or ip:
  * step(1):配置/etc/hosts文件
  * step(2):确认配置主机对象
  * step(3):配置hostname
  * step(4):关闭SElinux
  * step(5):关闭firewall
  * step(6):调整swap参数
  * step(7):关闭transparent hugepage
  * step(8):配置NTP server
  
### 后面继续更新
