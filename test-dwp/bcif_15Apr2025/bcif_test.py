import requests
from rcsb.utils.io.MarshalUtil import MarshalUtil

print("hello")

# r = requests.get("https://models.rcsb.org/5JYQ.bcif.gz")
# print(r.status_code)
# with open("5JYQ.bcif.gz", "wb") as f:
#     f.write(r.content)

mU = MarshalUtil()

# bcif_file = "https://models.rcsb.org/5JYQ.bcif.gz"
bcif_file = "5JYQ.bcif.gz"

dcL = mU.doImport(bcif_file, fmt="bcif")

dc = dcL[0]
print(dc.getName())

## Run length takes an integer (x or y) and repeats it (n or m) times, such as for '_entity_poly_seq' in 5JYQ:
# colDataList = [x, n, y, m]
# colDataList = [1, 20, 2, 23]
# for ii in range(0, len(colDataList), 2):
#     for _ in range(colDataList[ii + 1]):
#         print(colDataList[ii])

print(" \n\n\n DOING EXPORT \n\n\n")
dcL = mU.doImport("https://files.rcsb.org/download/5JYQ.cif.gz", fmt="mmcif")

out_bcif_file = "5JYQ_out.bcif"

mU.doExport(out_bcif_file, dcL, fmt="bcif")
dcL2 = mU.doImport(out_bcif_file, fmt="bcif")

dc2 = dcL2[0]
print(dc2.getName())
