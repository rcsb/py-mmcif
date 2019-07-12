#
#
try:
    from mmcif.io.IoAdapterCore import IoAdapterCore as IoAdapter  # noqa: F401
except Exception:
    from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter  # noqa: F401
