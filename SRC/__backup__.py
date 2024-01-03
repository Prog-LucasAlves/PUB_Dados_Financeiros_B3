import __conectdb__
import __query__

# Script backup dos dados do banco de dados.
# O arquivo csv será salvo na pasta Backup.
csv_file_name = "../Backup/some_file.csv"
bk = __query__.backup_query
with open(csv_file_name, "w") as f:
    __conectdb__.bk(bk, f)

#####
