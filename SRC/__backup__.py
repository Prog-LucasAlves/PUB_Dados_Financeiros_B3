import __conectdb__
import __query__

csv_file_name = "../Backup/some_file.csv"
bk = __query__.backup_query
with open(csv_file_name, "w") as f:
    __conectdb__.bk(bk, f)

#####
