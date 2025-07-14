import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

# Inicialização do Glue Job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Caminhos ajustados (único bucket com duas pastas)
input_path = "s3://weather-pipeline-raw-alex/raw/"
output_path = "s3://weather-pipeline-raw-alex/processed/"

# Esquema explícito para evitar erro de inferência
raw_schema = StructType([
    StructField("city", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("temperature", FloatType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("wind_speed", FloatType(), True),
    StructField("raw", StringType(), True)
])

# Leitura dos dados JSON
df_raw = spark.read.schema(raw_schema).json(input_path, multiLine=True)

# Transformações simples: filtrando campos e convertendo timestamp
df_transformed = df_raw.select(
    col("city"),
    col("timestamp"),
    col("temperature"),
    col("humidity"),
    col("wind_speed")
)

# Escrita no path de saída (processed)
df_transformed.write.mode("overwrite").json(output_path)

job.commit()
