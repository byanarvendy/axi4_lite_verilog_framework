# Makefile for AXI4-Lite Interconnect Simulation
# this Makefile generates the AXI4-Lite interconnect module and its testbench,
# compiles the testbench, runs the simulation, and opens the waveform viewer
# it supports different configurations specified by the user.

.PHONY: all sim clean wave interconnect help

# top level #
TOP         			= axi4_lite_interconnect

# define tools #
IVERILOG    			= iverilog
VVP         			= vvp
PYTHON      			= python3

# directory structure #
RTL                 	= logical/rtl
TB                  	= logical/tb
SIM                 	= logical/sim
INTERCONNECT_DIR    	= $(RTL)/axi4_lite_interconnect
WRAPPER_DIR    			= $(RTL)/wrapper/interconnect
WRAPPER_TB 				= $(TB)/tb_wrapper

# source files #
INC     				= $(RTL)/include.vh
SRC     				= $(INC) $(TB)/tb_$(TOP)_$(CONFIG).v
OUT     				= $(SIM)/tb_$(TOP)_$(CONFIG).vvp
VCD     				= $(SIM)/tb_$(TOP)_$(CONFIG).vcd

# generator scripts #
GENERATOR_INTERCONNECT	= $(INTERCONNECT_DIR)/$(TOP)_generator.py
GENERATOR_WRAPPER 		= $(WRAPPER_DIR)/wrapper_$(TOP)_generator.py
GENERATOR_TB    		= $(TB)/tb_$(TOP)/tb_$(TOP)_generator.py
GENERATOR_WRAPPER_TB	= $(WRAPPER_TB)/interconnect/tb_wrapper_$(TOP)_generator.py

# default configuration #
CONFIG ?= m1s2


all: sim

# generate interconnect module and testbench #
ifneq ($(filter m% s%,$(MAKECMDGOALS)),)
CONFIG := $(lastword $(MAKECMDGOALS))
$(eval $(CONFIG): ;@:)
interconnect: $(CONFIG)
	@echo "Generating AXI4-Lite Interconnect $(CONFIG)"
	$(PYTHON) $(GENERATOR_INTERCONNECT) $(CONFIG)
	$(PYTHON) $(GENERATOR_WRAPPER) $(CONFIG)
	$(PYTHON) $(GENERATOR_TB) $(CONFIG)
	$(PYTHON) $(GENERATOR_WRAPPER_TB) $(CONFIG)
else
interconnect:
	@echo "Error: Please specify configuration (e.g., 'make interconnect m2s2')"
	@exit 1
endif

# targets configuration #
ifneq ($(filter m% s%,$(MAKECMDGOALS)),)
RUN_CONFIG := $(lastword $(MAKECMDGOALS))
$(eval $(RUN_CONFIG): ;@:)

sim: $(RUN_CONFIG)
	@echo "\ncompiling testbench for $(RUN_CONFIG)"
	$(IVERILOG) -o $(SIM)/$(TOP)/$(TOP)_$(RUN_CONFIG).vvp $(INC) $(TB)/tb_$(TOP)/tb_$(TOP)_$(RUN_CONFIG).v
	@echo "\nrunning simulation for $(RUN_CONFIG)"
	$(VVP) $(SIM)/$(TOP)/$(TOP)_$(RUN_CONFIG).vvp

wave: $(RUN_CONFIG)
	@echo "\nopening waveform for $(RUN_CONFIG)"
	gtkwave $(SIM)/$(TOP)/$(TOP)_$(RUN_CONFIG).vcd &

wrappersim: $(RUN_CONFIG)
	@echo "\ncompiling testbench for wrapper $(RUN_CONFIG)"
	$(IVERILOG) -o $(SIM)/wrapper/wrapper_$(TOP)_$(RUN_CONFIG).vvp $(INC) $(WRAPPER_TB)/interconnect/tb_wrapper_$(TOP)_$(RUN_CONFIG).v
	@echo "\nrunning simulation for wrapper $(RUN_CONFIG)"
	$(VVP) $(SIM)/wrapper/wrapper_$(TOP)_$(RUN_CONFIG).vvp

wrapperwave: $(RUN_CONFIG)
	@echo "\nopening waveform for wrapper $(RUN_CONFIG)"
	gtkwave $(SIM)/wrapper/wrapper_$(TOP)_$(RUN_CONFIG).vcd &

else

sim:
	@echo "\ncompiling testbench for $(CONFIG)"
	$(IVERILOG) -o $(SIM)/$(TOP)/$(TOP)_$(CONFIG).vvp $(INC) $(TB)/tb_$(TOP)/tb_$(TOP)_$(CONFIG).v
	@echo "\nrunning simulation for $(CONFIG)"
	$(VVP) $(SIM)/$(TOP)/$(TOP)_$(CONFIG).vvp

wave:
	@echo "\nopening waveform for $(CONFIG)"
	gtkwave $(SIM)/$(TOP)/$(TOP)_$(CONFIG).vcd &

wrappersim:
	@echo "\ncompiling testbench for wrapper $(CONFIG)"
	$(IVERILOG) -o $(SIM)/wrapper/wrapper_$(TOP)_$(CONFIG).vvp $(INC) $(WRAPPER_TB)/interconnect/tb_wrapper_$(TOP)_$(CONFIG).v
	@echo "\nrunning simulation for wrapper $(CONFIG)"
	$(VVP) $(SIM)/wrapper/wrapper_$(TOP)_$(CONFIG).vvp

wrapperwave:
	@echo "\nopening waveform for wrapper $(CONFIG)"
	gtkwave $(SIM)/wrapper/wrapper_$(TOP)_$(CONFIG).vcd &
endif


clean:
	rm -f $(SIM)/*.vvp $(SIM)/*.vcd


help:
	@echo "to run the simulation for a specific configuration, use:"
	@echo "   make interconnect m2s2"
	@echo "   notes:"
	@echo "      handle both formats:	  1. make interconnect m2s2"
	@echo "                                  2. make interconnect CONFIG=m2s2"
	@echo ""
	@echo "available targets:"
	@echo "   interconnect mXsY   -> generate interconnect module and testbench (e.g., make interconnect m2s2)"
	@echo "   sim mXsY            -> compile testbench and run simulation for specific configuration"
	@echo "   wave mXsY           -> open waveform viewer for specific configuration"
	@echo "   clean               -> clean simulation files"
	@echo ""
	@echo "usage examples:"
	@echo "   make interconnect m2s2"
	@echo "   make sim m1s2"
	@echo "   make wave m1s2"