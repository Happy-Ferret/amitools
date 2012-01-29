from ..Block import *

class PartitionDosEnv:
  def __init__(self, size=0, block_size=0, sec_org=0, surfaces=0, sec_per_blk=0, blk_per_trk=0,
               reserved=0, pre_alloc=0, interleave=0, low_cyl=0, high_cyl=0, num_buffer=0,
               buf_mem_type=0, max_transfer=0, mask=0, boot_pri=0, dos_type=0,
               baud=0, control=0, boot_blocks=0):
    self.size = size
    self.block_size = block_size
    self.sec_org = sec_org
    self.surfaces = surfaces
    self.sec_per_blk = sec_per_blk
    self.blk_per_trk = blk_per_trk
    self.reserved = reserved
    self.pre_alloc = pre_alloc
    self.interleave = interleave
    self.low_cyl = low_cyl
    self.high_cyl = high_cyl
    self.num_buffer = num_buffer
    self.buf_mem_type = buf_mem_type
    self.max_transfer = max_transfer
    self.mask = mask
    self.boot_pri = boot_pri
    self.dos_type = dos_type
    self.baud = baud
    self.control = control
    self.boot_blocks = boot_blocks
  
  def dump(self):
    print "DosEnv"
    print " size:           %d" % self.size
    print " block_size:     %d" % self.block_size
    print " sec_org:        %d" % self.sec_org
    print " surfaces:       %d" % self.surfaces
    print " sec_per_blk:    %d" % self.sec_per_blk
    print " blk_per_trk:    %d" % self.blk_per_trk
    print " reserved:       %d" % self.reserved
    print " pre_alloc:      %d" % self.pre_alloc
    print " interleave:     %d" % self.interleave
    print " low_cyl:        %d" % self.low_cyl
    print " high_cyl:       %d" % self.high_cyl
    print " num_buffer:     %d" % self.num_buffer
    print " buf_mem_type:   0x%08x" % self.buf_mem_type
    print " max_tramsfer:   0x%08x" % self.max_transfer
    print " mask:           0x%08x" % self.mask
    print " boot_pri:       %d" % self.boot_pri
    print " dos_type:       0x%08x = %s" % (self.dos_type, dostype_long_to_tag(self.dos_type))
    print " baud:           %d" % self.baud
    print " control:        %d" % self.control
    print " boot_blocks:    %d" % self.boot_blocks
  
  def read(self, blk):
    self.size = blk._get_long(32)
    self.block_size = blk._get_long(33)
    self.sec_org = blk._get_long(34)
    self.surfaces = blk._get_long(35)
    self.sec_per_blk = blk._get_long(36)
    self.blk_per_trk = blk._get_long(37)
    self.reserved = blk._get_long(38)
    self.pre_alloc = blk._get_long(39)
    self.interleave = blk._get_long(40)
    self.low_cyl = blk._get_long(41)
    self.high_cyl = blk._get_long(42)
    self.num_buffer = blk._get_long(43)
    self.buf_mem_type = blk._get_long(44)
    self.max_tranfser = blk._get_long(45)
    self.mask = blk._get_long(46)
    self.boot_pri = blk._get_long(47)
    self.dos_type = blk._get_long(48)
    self.baud = blk._get_long(49)
    self.control = blk._get_long(50)
    self.boot_blocks = blk._get_long(51)
    
  def write(self, blk):
    blk._put_long(32, self.size)
    blk._put_long(33, self.block_size)
    blk._put_long(34, self.sec_org)
    blk._put_long(35, self.surfaces)
    blk._put_long(36, self.sec_per_blk)
    blk._put_long(37, self.blk_per_trk)
    blk._put_long(38, self.reserved)
    blk._put_long(39, self.pre_alloc)
    blk._put_long(40, self.interleave)
    blk._put_long(41, self.low_cyl)
    blk._put_long(42, self.high_cyl)
    blk._put_long(43, self.num_buffer)
    blk._put_long(44, self.buf_mem_type)
    blk._put_long(45, self.max_transfer)
    blk._put_long(46, self.mask)
    blk._put_long(47, self.boot_pri)
    blk._put_long(48, self.dos_type)
    blk._put_long(49, self.baud)
    blk._put_long(50, self.control)
    blk._put_long(51, self.boot_blocks)

class PartitionBlock(Block):
  no_blk = 0xffffffff
  
  def __init__(self, blkdev, blk_num):
    Block.__init__(self, blkdev, blk_num, chk_loc=2, is_type=Block.PART)
  
  def create(self, host_id=0, next=0, flags=0, dev_flags=0, drv_name="",
             size=64, dos_env=None):
    Block.create(self)
    self.size = size
    self.host_id = host_id
    self.next = next
    self.flags = flags
    
    self.dev_flags = dev_flags
    self.drv_name = drv_name
    
    if dos_env == None:
      dos_env = PartitionDosEnv()
    self.dos_env = dos_env
      
  def write(self):
    self._create_data()
    
    self._put_long(1, self.size)
    self._put_long(3, self.host_id)
    self._put_long(4, self.next)
    self._put_long(5, self.flags)
    
    self._put_long(8, self.dev_flags)
    self._put_bstr(9, 31, self.drv_name)
    
    self.dos_env.write(self)
    
    Block.write(self)
  
  def read(self):
    Block.read(self)
    if not self.valid:
      return False
    
    self.size = self._get_long(1)
    self.host_id = self._get_long(3)
    self.next = self._get_long(4)
    self.flags = self._get_long(5)
    
    self.dev_flags = self._get_long(8)
    self.drv_name = self._get_bstr(9, 31)
    
    self.dos_env = PartitionDosEnv()
    self.dos_env.read(self)
    
    return self.valid
  
  def _dump_ptr(self, ptr):
    if ptr == self.no_blk:
      return "none"
    else:
      return "%d" % ptr
  
  def dump(self):
    Block.dump(self, "Partition")
    
    print " size:           %d" % self.size
    print " host_id:        %d" % self.host_id
    print " next:           %s" % self._dump_ptr(self.next)
    print " flags:          0x%08x" % self.flags
    print " dev_flags:      0x%08x" % self.dev_flags
    print " drv_name:       '%s'" % self.drv_name 
    
    self.dos_env.dump()
