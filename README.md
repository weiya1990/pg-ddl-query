# 可连接多个PG数据源批量执行sql文件

## 使用方式

docker方式启动

构建镜像：

```bash
cd /opt
git clone xxxx
cd pg-ddl-query
docker build -t ddl-sync:alpine .
```

启动容器测试：

```bash
 #把sql文件和数据库配置文件挂载到容器中

 docker run -it --rm -v /opt/pg-ddl-sync:/opt/python/etc  ddl-sync:alpine
```



