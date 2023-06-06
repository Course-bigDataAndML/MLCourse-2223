# Implementing custom magics

from IPython.core.magic import (register_line_magic, register_cell_magic, register_line_cell_magic)
from pyspark import SparkContext,SparkConf
import os

# This is the JupyterHub login username 
# (it might not correspond to the OS username, 
# which is tipycally Jovyan)
def user():
   
    path=os.environ['JUPYTERHUB_SERVICE_PREFIX']
    path_list = path.split(os.sep)
    username=path_list[2]
    
    return username

@register_line_magic
def login_user(self):
    
    username=user()
    
    return username

# Define the Spark context
@register_line_magic
def sc(num_workers):
    
    # set default number of workers
    if not num_workers:
        num_workers=25
    # ser max number of workers 
    max_workers=25
    #if int(num_workers) > max_workers:
    #    num_workers=max_workers
        
    username=user()
    
    sconf=SparkConf()
    # add sparkmonitor extension
    sconf.set("spark.extraListeners", "sparkmonitor.listener.JupyterSparkMonitorListener")
    sconf.set("spark.driver.extraClassPath","/opt/conda/lib/python3.9/site-packages/sparkmonitor/listener_2.12.jar")
    sconf.set("spark.master", "k8s://https://192.168.2.39:6443")
    sconf.set("spark.name", "spark-"+username)
    sconf.set("spark.submit.deployMode", "client")
    sconf.set("spark.kubernetes.namespace", username)
    sconf.set("spark.executor.instances", num_workers)
    sconf.set("spark.kubernetes.container.image", "svallero/sparkpy:3.2.1")
    sconf.set("spark.driver.host", "jupyter-"+username+".jhub.svc.cluster.local")
    #sconf.set("spark.driver.host", "192.168.149.9")
    sconf.set('spark.app.name', "jupyter-"+username)
    sconf.set('spark.kubernetes.pyspark.pythonVersion', "3")
    sconf.set("spark.driver.port", 34782)
    sconf.set("spark.executorEnv.HADOOP_USER_NAME", "jovyan")
    sconf.set("spark.driver.memory", "10g")
    sconf.set("spark.executor.memory", "10g")
    sconf.set("spark.executor.cores", "5") # magic number to achieve maximum HDFS throughtput 
    #sconf.set("spark.kubernetes.container.image.pullPolicy", "Always")
    
    # for spark-tensorflow?
    #    sconf.set("spark.task.cpus", num_workers)
    #    sconf.set("spark.dynamicAllocation.enabled", "false")

    # to land on particular nodes
    #sconf.set("spark.kubernetes.node.selector.kubernetes.io/hostname","t2-mlwn-02.to.infn.it")    
    #sconf.set("spark.kubernetes.node.selector.cluster", "yoga-priv")

    context=SparkContext(conf=sconf)   
    context.setLogLevel("DEBUG")
    context._conf.getAll()
    
    return context

# Define the Spark context for bigDL
# bigDL forces number of cores = 1
# needs at least 6 GB/executor
# resources as default spark config - 60 GB memory = 10 (driver)+5x10 (executor) /student , 25 cores
# try with 7*8 GB (executor) +4 GB (driver) = 60 GB

@register_line_magic
def sc_bigDL(num_workers):
    
    # set default number of workers
    if not num_workers:
        num_workers=5
    # ser max number of workers 
    max_workers=5
    #if int(num_workers) > max_workers:
    #    num_workers=max_workers
        
    username=user()
    
    sconf=SparkConf()
    # add sparkmonitor extension
    sconf.set("spark.extraListeners", "sparkmonitor.listener.JupyterSparkMonitorListener")
    sconf.set("spark.driver.extraClassPath","/opt/conda/lib/python3.9/site-packages/sparkmonitor/listener_2.12.jar")
    sconf.set("spark.master", "k8s://https://192.168.2.39:6443")
    sconf.set("spark.name", "spark-"+username)
    sconf.set("spark.submit.deployMode", "client")
    sconf.set("spark.kubernetes.namespace", username)
    sconf.set("spark.executor.instances", num_workers)
    sconf.set("spark.kubernetes.container.image", "svallero/sparkpy:3.2.1")
    sconf.set("spark.driver.host", "jupyter-"+username+".jhub.svc.cluster.local")
    #sconf.set("spark.driver.host", "192.168.149.9")
    sconf.set('spark.app.name', "jupyter-"+username)
    sconf.set('spark.kubernetes.pyspark.pythonVersion', "3")
    sconf.set("spark.driver.port", 34782)
    sconf.set("spark.executorEnv.HADOOP_USER_NAME", "jovyan")
    sconf.set("spark.driver.memory", "4g") #works already with 2
    sconf.set("spark.executor.memory", "8g") #works already with 6 
    #sconf.set("spark.kubernetes.container.image.pullPolicy", "Always")

    # to land on particular nodes
    #sconf.set("spark.kubernetes.node.selector.kubernetes.io/hostname","t2-mlwn-02.to.infn.it")    
    #sconf.set("spark.kubernetes.node.selector.cluster", "yoga-priv")
 
    #bigDL
    sconf.set("spark.jars","/opt/conda/lib/python3.9/site-packages/bigdl/share/dllib/lib/bigdl-dllib-spark_3.1.2-2.0.0-jar-with-dependencies.jar")
    sconf.set("spark.executor.extraClassPath","/opt/conda/lib/python3.9/site-packages/bigdl/share/dllib/lib/bigdl-dllib-spark_3.1.2-2.0.0-jar-with-dependencies.jar")
    sconf.set("spark.executor.cores", "1")
    sconf.set("spark.cores.max", "1")

# increasing memoryOverhead reduces errors, but makes it slower    
#    sconf.set("spark.executor.memoryOverhead", "512m")  
#    sconf.set("spark.driver.memoryOverhead", "512m")    
#    sconf.set("spark.kubernetes.memoryOverheadFactor","0.5")
#    sconf.set("spark.default.parallelism", "250")
#    sconf.set("spark.sql.shuffle.partitions", "100")
#    sconf.set("spark.shuffle.io.retryWait", "180s")  
#    sconf.set("spark.network.timeout", "800s")     
#    sconf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
#    sconf.set("spark.dynamicAllocation.enabled", "false")
    
    sconf.set("spark.shuffle.reduceLocality.enabled", "false")
    sconf.set("spark.shuffle.blockTransferService", "nio")
    sconf.set("spark.scheduler.minRegisteredResourcesRatio", "1.0")
    sconf.set("spark.speculation", "false")    
    
    context=SparkContext(conf=sconf)   
    context.setLogLevel("DEBUG")
    context._conf.getAll()
    
    return context

# Path to the user's home dir on HDFS
@register_line_magic
def hdfs_path(self):
    
    username=user()
    path="hdfs://192.168.2.39/user/"+username
    
    return path
    
