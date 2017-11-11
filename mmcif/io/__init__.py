#
#
try:
    from mmcif.io.IoAdapterCore import IoAdapterCore as IoAdapter
except:
    from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter
