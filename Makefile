# New Makefile for building a standard apt repository

# Directories
POOL_DIR := debian/pool/main
DIST_DIR := debian/dists/universal-apt/main/binary-amd64

# Automatically find all .deb files in the pool
DEB_FILES := $(wildcard $(POOL_DIR)/*.deb)

# Default target: generate both Packages and Packages.gz
all: packages packages.gz

# Generate the Packages file from all .deb files in the pool
$(DIST_DIR)/Packages: $(DEB_FILES)
	@mkdir -p $(DIST_DIR)
	dpkg-scanpackages $(POOL_DIR) /dev/null "pool/main" > $(DIST_DIR)/Packages

.PHONY: packages
packages: $(DIST_DIR)/Packages

# Compress the Packages file to create Packages.gz
.PHONY: packages.gz
packages.gz: $(DIST_DIR)/Packages
	gzip -9c $(DIST_DIR)/Packages > $(DIST_DIR)/Packages.gz

# Clean generated files
.PHONY: clean
clean:
	rm -f $(DIST_DIR)/Packages $(DIST_DIR)/Packages.gz
