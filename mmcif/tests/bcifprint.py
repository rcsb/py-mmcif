import argparse
import msgpack
import sys
import logging


class BcifPrint:
    def __init__(self, storebytes=False):
        self.__indent = 0
        self.__storeStringsAsBytes = storebytes
        self.__defaultStringEncoding = "utf-8"
        self.__error = False

    def __getindent(self, indent):
        return " " * indent

    def dump(self, bD):
        """Recursively parse"""
        self.__decodeFile(bD, 0)

    def getError(self):
        """Returns the error flag"""
        return self.__error

    def __decodeFile(self, bD, indent):
        pindent = self.__getindent(indent)
        indent += 2
        pindent2 = self.__getindent(indent)

        print("%s File {" % pindent)
        # print(bD.keys())
        print("%s version: %s" % (pindent2, bD[self.__toBytes("version")]))
        print("%s encoder: %s" % (pindent2, bD[self.__toBytes("encoder")]))
        print("%s datablocks: [ (len=%s)" % (pindent2, len(bD[self.__toBytes("dataBlocks")])))
        self.__decodeDataBlocks(bD[self.__toBytes("dataBlocks")], indent + 2)
        print("%s ]" % pindent2)
        print("%s }" % pindent)

    def __decodeDataBlocks(self, dbs, indent):
        pindent = self.__getindent(indent)
        indent += 2
        pindent2 = self.__getindent(indent)
        for db in dbs:
            print("%s DataBlock {" % pindent)
            print("%s header: %s" % (pindent2, db[self.__toBytes("header")]))
            print("%s categories: [ (len=%s)" % (pindent2,
                                                 len(db[self.__toBytes("categories")])))
            self.__decodeCategories(db[self.__toBytes("categories")], indent + 2)
            print("%s ]" % pindent2)
            print("%s }" % pindent)

    def __decodeCategories(self, cats, indent):
        pindent = self.__getindent(indent)
        indent += 2
        pindent2 = self.__getindent(indent)
        for cat in cats:
            print("%s Category {" % pindent)
            print("%s name: %s" % (pindent2, cat[self.__toBytes("name")]))
            print("%s rowcount: %s" % (pindent2, cat[self.__toBytes("rowCount")]))
            print("%s columns: [" % pindent2)
            self.__decodeColumns(cat[self.__toBytes("columns")], indent + 2)
            print("%s ]" % pindent2)
            print("%s }" % pindent)

    def __decodeColumns(self, cols, indent):
        pindent = self.__getindent(indent)
        indent += 2
        pindent2 = self.__getindent(indent)
        for col in cols:
            print("%s Column {" % pindent)
            print("%s name: %s" % (pindent2, col[self.__toBytes("name")]))
            print("%s data: {" % pindent2)
            self.__decodeData(col[self.__toBytes("data")], indent + 6)
            print("%s }" % pindent2)

            val = col[self.__toBytes("mask")]
            if val:
                print("%s mask: {" % pindent2)
                self.__decodeData(col[self.__toBytes("mask")], indent + 6)
                print("%s }" % pindent2)
            else:
                print("%s mask: %s" % (pindent2, val))

            print("%s }" % pindent)

    def __decodeData(self, data, indent):
        pindent = self.__getindent(indent)
        indent += 2
        pindent2 = self.__getindent(indent)
        val = data[self.__toBytes("data")]

        val = val[:30] + b"..." if len(val) > 30 else val
        print("%s data: %s" % (pindent2, val))
        print("%s encoding: [" % pindent2)
        self.__decodeEncodings(data[self.__toBytes("encoding")], indent + 2)

        print("%s }" % pindent)

    def __decodeEncodings(self, encs, indent):
        self.__verifyEncodings(encs, indent)
        for enc in encs:
            self.__decodeEncoding(enc, indent)

    def __decodeEncoding(self, enc, indent):
        pindent = self.__getindent(indent)
        indent += 2
        kind = enc[self.__toBytes("kind")]
        if kind == self.__toBytes("ByteArray"):
            etype = enc[self.__toBytes("type")]
            detype = self.__decodeType(etype)
            print(f"{pindent} ByteArray {{type: {etype} ({detype})}}")
        elif kind == self.__toBytes("FixedPoint"):
            stype = enc[self.__toBytes("srcType")]
            dstype = self.__decodeType(stype)
            factor = enc[self.__toBytes("factor")]
            print(f"{pindent} FixedPoint {{factor: {factor}, srcType: {stype} ({dstype})}}")
        elif kind == self.__toBytes("IntervalQuantization"):
            stype = enc[self.__toBytes("srcType")]
            dstype = self.__decodeType(stype)
            minv = enc[self.__toBytes("min")]
            maxv = enc[self.__toBytes("max")]
            numsteps = enc["numSteps"]
            print(f"{pindent} IntervalQuantization {{min: {minv}, max: {maxv}, numSteps: {numsteps}, srcType: {stype} ({dstype})}}")
        elif kind == self.__toBytes("RunLength"):
            stype = enc[self.__toBytes("srcType")]
            dstype = self.__decodeType(stype)
            srcsize = enc[self.__toBytes("srcSize")]
            print(f"{pindent} RunLength {{srcType: {stype} ({dstype}), srcSize={srcsize}}}")
        elif kind == self.__toBytes("Delta"):
            stype = enc[self.__toBytes("srcType")]
            dstype = self.__decodeType(stype)
            origin = enc[self.__toBytes("origin")]
            print(f"{pindent} Delta {{origin: {origin}, srcType: {stype} ({dstype})}}")
        elif kind == self.__toBytes("IntegerPacking"):
            byteCount = enc[self.__toBytes("byteCount")]
            srcSize = enc[self.__toBytes("srcSize")]
            isUnsigned = enc[self.__toBytes("isUnsigned")]
            print(f"{pindent} IntegerPacking {{byteCount: {byteCount}, srcSize: {srcSize}, isUnsigned: {isUnsigned}}}")
        elif kind == self.__toBytes("StringArray"):
            sdata = enc[self.__toBytes("stringData")]
            sdata_trim = sdata[:60] + self.__toBytes("...") if len(sdata) > 60 else sdata

            offsets = enc[self.__toBytes("offsets")]
            offset_list = self.__Uint8ArrayToList(offsets)
            print(f"{pindent} StringArray {{stringData: \"{sdata_trim}\"")
            pindent_tmp = self.__getindent(indent + 11)
            print(f"{pindent_tmp} offsets: {offset_list}")

            pindent_tmp = self.__getindent(indent + 11)
            print(f"{pindent_tmp} dataEncoding: [")
            self.__decodeEncodings(enc[self.__toBytes("dataEncoding")],
                                   indent + 28)
            print(f"{pindent_tmp}               ]")

            pindent_tmp = self.__getindent(indent + 11)
            print(f"{pindent_tmp} offsetEncoding: [")
            self.__decodeEncodings(enc[self.__toBytes("offsetEncoding")],
                                   indent + 30)
            print(f"{pindent_tmp}                 ]")

        else:
            print(f"{pindent} UNKNOWN ENCODING {enc}")

    def __decodeType(self, typ):
        tmap = {1: "int8",
                2: "int16",
                3: "int32",
                4: "uint8",
                5: "uint16",
                6: "uint32",
                32: "float32",
                33: "float64"
                }

        val = tmap.get(typ, "unknown")
        return val

    def __Uint8ArrayToList(self, bdata):
        rlist = []
        for pos in range(len(bdata)):
            rlist.append(bdata[pos])
        return rlist

    def __verifyEncodings(self, encs, indent, ctx=""):
        """Verify the encodings data types"""
        btype = "UNKNOWN"
        pindent = self.__getindent(indent)

        for enc in reversed(encs):
            kind = enc[self.__toBytes("kind")]
            if kind == self.__toBytes("ByteArray"):
                # Do not care about incoming type
                etype = enc[self.__toBytes("type")]
                btype = self.__decodeType(etype)
            elif kind == self.__toBytes("IntegerPacking"):
                if btype not in ("int8", "int16", "uint8", "uint16"):
                    print(f"{pindent} ERROR IntegerPacking {btype}{ctx} input not allowed")
                    self.__error = True
                    break
                btype = "int32"

            elif kind == self.__toBytes("Delta"):
                if btype not in ("int8", "int16", "int32"):
                    print(f"{pindent} ERROR DeltaPacking {btype}{ctx} input not allowed")
                    self.__error = True
                    break
                stype = enc[self.__toBytes("srcType")]
                btype = self.__decodeType(stype)

            elif kind == self.__toBytes("RunLength"):
                if btype not in ("int32"):
                    print(f"{pindent} ERROR RunLength {btype}{ctx} input not allowed")
                    self.__error = True
                    break
                stype = enc[self.__toBytes("srcType")]
                btype = self.__decodeType(stype)

            elif kind == self.__toBytes("FixedPoint"):
                if btype not in ("int32"):
                    print(f"{pindent} ERROR FixedPoint {btype}{ctx} input not allowed")
                    self.__error = True
                    break
                stype = enc[self.__toBytes("srcType")]
                btype = self.__decodeType(stype)

            elif kind == self.__toBytes("StringArray"):
                # Test subsets
                self.__verifyEncodings(enc[self.__toBytes("dataEncoding")],
                                       indent, "(StringArray/dataEncoding)")
                self.__verifyEncodings(enc[self.__toBytes("offsetEncoding")],
                                       indent, "(StringArray/offsetEncoding)")

            elif kind == self.__toBytes("IntervalQuantization"):
                if btype not in ("int32"):
                    print(f"{pindent} ERROR IntervalQuantization {btype}{ctx} input not allowed")
                    self.__error = True
                    break
                stype = enc[self.__toBytes("srcType")]
                btype = self.__decodeType(stype)
            else:
                print(f"{pindent} ERROR UNKNOWN KIND {kind}")
                self.__error = True
                break

    def __toBytes(self, strVal):
        """Optional conversion of the input string to bytes according to the class setting (storeStringsAsBytes).

        Args:
            strVal (string): input string

        Returns:
            string or bytes: optionally converted string.
        """
        try:
            return strVal.encode(self.__defaultStringEncoding) if self.__storeStringsAsBytes else strVal
        except (UnicodeDecodeError, AttributeError):
            logging.exception("Bad type for %r", strVal)
            return strVal


def main():

    parser = argparse.ArgumentParser(
        prog="bcifprint",
        description="Dumps contents of binary cif"
    )

    parser.add_argument('filename')
    parser.add_argument('--storestringsasbytes', dest="storebytes", action="store_true")
    args = parser.parse_args()

    with open(args.filename, "rb") as fin:
        bD = msgpack.unpack(fin)

    # print(bD)
    bc = BcifPrint(args.storebytes)
    bc.dump(bD)
    err = 1 if bc.getError() else 0
    # print("XXX", err)
    sys.exit(err)


if __name__ == "__main__":
    main()
