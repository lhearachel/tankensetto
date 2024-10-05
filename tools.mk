TOOLS := tools
NDSTOOL := $(TOOLS)/ndstool

tools: ndstool

ndstool:
	@cd $(NDSTOOL) ; sh autogen.sh
	@cd $(NDSTOOL) ; sh configure
	@cd $(NDSTOOL) ; make
