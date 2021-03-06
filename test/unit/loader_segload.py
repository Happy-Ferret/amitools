from amitools.vamos.loader import SegmentLoader
from amitools.vamos.machine import MockMemory
from amitools.vamos.mem import MemoryAlloc


def loader_segload_test(binbuild):
  lib_file = binbuild.make_lib('simple')
  mem = MockMemory(fill=23)
  alloc = MemoryAlloc(mem)
  loader = SegmentLoader(mem, alloc)
  seg_list = loader.load_seg(lib_file)
  assert seg_list is not None
