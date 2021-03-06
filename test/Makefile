# amibuild.make
#
# build programs with the following compilers:
# VBCC, GCC, AROS_GCC, SASC

SOURCES_C = dos_readargs.c dos_findarg.c
SOURCES_C += vprintf.c mem.c
SOURCES_C += util_muldiv.c util_date.c
SOURCES_C += math_double.c math_double_trans.c
SOURCES_C += math_single.c math_single_trans.c
SOURCES_C += math_fast.c math_fast_trans.c
SROUCES_C += test_hello.c test_raise.c

LIB_SOURCES_C = simple.c
LIB_SRC_DIR = libs

VPATH = src

# directories
BUILD_DIR ?= bin
LIB_BUILD_DIR = $(BUILD_DIR)/libs

# external data
SASC_INSTALL_DIR ?= $(HOME)/amiga/shared/sc
export SASC_INSTALL_DIR
NDK_DIR ?= /opt/m68k-amigaos/m68k-amigaos/ndk

# compilers
VBCC_EXE = vc
GCC = m68k-amigaos-gcc
AROS_GCC = m68k-aros-gcc
AROS_ELF2HUNK = elf2hunk
SASC = ../bin/vamos -c sasc.vamosrc sc

# options
VBCC_OPTS = +aos68k -I$(NDK_DIR)/include -Iinclude
GCC_OPTS  = -noixemul -Iinclude
GCC_OPTS_LIB = -ramiga-lib -fbaserel
GCC_OPTS_LIB_RES = -ramiga-libr -fbaserel
AROS_GCC_OPTS = -Iinclude
SASC_OPTS = SMALLDATA SMALLCODE NOSTKCHK NOCHKABORT NOICONS STRICT ANSI \
            INCDIR=include

# optimize options
VBCC_OPTI = -O2
GCC_OPTI = -O2
AROS_GCC_OPTI = -O2
SASC_OPTI = PARAMETERS=REGISTERS OPT OPTTIME OPTINLINE DEBUG=F \
            OPTSCHEDULE STRINGMERGE STRUCTUREEQUIVALENCE

# debug options
VBCC_DEBUG = -g
GCC_DEBUG = -g
AROS_GCC_DEBUG = -g
SASC_DEBUG = DEBUG=F

# libs
VBCC_LIBS = -lamiga

# binary extensions
VBCC_EXT = _vc
GCC_EXT = _gcc
AROS_GCC_EXT = _agcc
SASC_EXT = _sc
DBG_EXT = _dbg

# source to program mapping
PROGS_VBCC = $(patsubst %.c,$(BUILD_DIR)/%$(VBCC_EXT),$(SOURCES_C))
PROGS_GCC  = $(patsubst %.c,$(BUILD_DIR)/%$(GCC_EXT),$(SOURCES_C))
PROGS_AROS = $(patsubst %.c,$(BUILD_DIR)/%$(AROS_GCC_EXT),$(SOURCES_C))
PROGS_SASC = $(patsubst %.c,$(BUILD_DIR)/%$(SASC_EXT),$(SOURCES_C))

PROGS = $(PROGS_VBCC) $(PROGS_GCC) $(PROGS_AROS) $(PROGS_SASC)

PROGS_VBCC_DBG = $(patsubst %.c,$(BUILD_DIR)/%$(VBCC_EXT)$(DBG_EXT),$(SOURCES_C))
PROGS_GCC_DBG  = $(patsubst %.c,$(BUILD_DIR)/%$(GCC_EXT)$(DBG_EXT),$(SOURCES_C))
PROGS_AROS_DBG = $(patsubst %.c,$(BUILD_DIR)/%$(AROS_GCC_EXT)$(DBG_EXT),$(SOURCES_C))
PROGS_SASC_DBG = $(patsubst %.c,$(BUILD_DIR)/%$(SASC_EXT)$(DBG_EXT),$(SOURCES_C))

PROGS_DBG = $(PROGS_VBCC_DBG) $(PROGS_GCC_DBG) $(PROGS_AROS_DBG) $(PROGS_SASC_DBG)

# libraries (gcc only for now)
LIBS_GCC = $(patsubst %.c,$(LIB_BUILD_DIR)/%.library,$(LIB_SOURCES_C))
LIBS_GCC += $(patsubst %.c,$(LIB_BUILD_DIR)/%-res.library,$(LIB_SOURCES_C))
LIBS = $(LIBS_GCC)

LIBS_GCC_DBG  = $(patsubst %.c,$(LIB_BUILD_DIR)/%-dbg.library,$(LIB_SOURCES_C))
LIBS_GCC_DBG += $(patsubst %.c,$(LIB_BUILD_DIR)/%-res-dbg.library,$(LIB_SOURCES_C))
LIBS_DBG = $(LIBS_GCC_DBG)

# --- rules ---

all: $(PROGS) $(PROGS_DBG) $(LIBS) $(LIBS_DBG)

opt: $(PROGS)
debug: $(PROGS_DBG)

libs: $(LIBS)
libs-debug: $(LIBS_DBG)

$(PROGS): $(BUILD_DIR)
$(LIBS): $(LIB_BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)

# dir rules
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(LIB_BUILD_DIR):
	mkdir -p $(LIB_BUILD_DIR)

# rules for opt
$(BUILD_DIR)/%$(VBCC_EXT) : %.c
	$(VBCC_EXE) $(VBCC_OPTS) $(VBCC_OPTI) -o $@ $< $(VBCC_LIBS)

$(BUILD_DIR)/%$(GCC_EXT) : %.c
	$(GCC) $(GCC_OPTS) $(GCC_OPTI) -o $@ $<

$(BUILD_DIR)/%$(AROS_GCC_EXT) : %.c
	$(AROS_GCC) $(AROS_GCC_OPTS) $(AROS_GCC_OPTI) -o $@ $<

$(BUILD_DIR)/%$(SASC_EXT) : %.c
	$(SASC) $(SASC_OPTS) $(SASC_OPTI) LINK TO $@ $<


# rules for dbg
$(BUILD_DIR)/%$(VBCC_EXT)$(DBG_EXT) : %.c
	$(VBCC_EXE) $(VBCC_OPTS) $(VBCC_DEBUG) -o $@ $< $(VBCC_LIBS)

$(BUILD_DIR)/%$(GCC_EXT)$(DBG_EXT) : %.c
	$(GCC) $(GCC_OPTS) $(GCC_DEBUG) -o $@ $<

$(BUILD_DIR)/%$(AROS_GCC_EXT)$(DBG_EXT) : %.c
	$(AROS_GCC) $(AROS_GCC_OPTS) $(AROS_GCC_DEBUG) -o $@ $<

$(BUILD_DIR)/%$(SASC_EXT)$(DBG_EXT) : %.c
	$(SASC) $(SASC_OPTS) $(SASC_DEBUG) LINK TO $@ $<


# lib rules
$(LIB_BUILD_DIR)/%.library : $(LIB_SRC_DIR)/%.c
	$(GCC) $(GCC_OPTS) $(GCC_OPTI) $(GCC_OPTS_LIB) -o $@ $<

$(LIB_BUILD_DIR)/%-res.library : $(LIB_SRC_DIR)/%.c
	$(GCC) $(GCC_OPTS) $(GCC_OPTI) $(GCC_OPTS_LIB_RES) -o $@ $<

$(LIB_BUILD_DIR)/%-dbg.library : $(LIB_SRC_DIR)/%.c
	$(GCC) $(GCC_OPTS) $(GCC_DEBUG) $(GCC_OPTS_LIB) -o $@ $<

$(LIB_BUILD_DIR)/%-res-dbg.library : $(LIB_SRC_DIR)/%.c
	$(GCC) $(GCC_OPTS) $(GCC_DEBUG) $(GCC_OPTS_LIB_RES) -o $@ $<


# special flags
$(BUILD_DIR)/math_double_sc: SASC_OPTS += Math=i
$(BUILD_DIR)/math_double_sc$(DBG_EXT): SASC_OPTS += Math=i
$(BUILD_DIR)/math_double_trans_sc: SASC_OPTS += Math=i
$(BUILD_DIR)/math_double_trans_sc$(DBG_EXT): SASC_OPTS += Math=i

$(BUILD_DIR)/math_single_sc: SASC_OPTS += Math=i
$(BUILD_DIR)/math_single_sc$(DBG_EXT): SASC_OPTS += Math=i
$(BUILD_DIR)/math_single_trans_sc: SASC_OPTS += Math=i
$(BUILD_DIR)/math_single_trans_sc$(DBG_EXT): SASC_OPTS += Math=i

$(BUILD_DIR)/math_fast_sc: SASC_OPTS += Math=f
$(BUILD_DIR)/math_fast_sc$(DBG_EXT): SASC_OPTS += Math=f
$(BUILD_DIR)/math_fast_trans_sc: SASC_OPTS += Math=f
$(BUILD_DIR)/math_fast_trans_sc$(DBG_EXT): SASC_OPTS += Math=f
