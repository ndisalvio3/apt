# Makefile for building a standard APT repository with release signing

# Directories
POOL_DIR := debian/pool/main
DIST_DIR := debian/dists/universal-apt/main/binary-amd64

# Automatically find all .deb files in the pool
DEB_FILES := $(wildcard $(POOL_DIR)/*.deb)

# Default target: generate Packages, Packages.gz, and Release files
all: packages packages.gz release

# Generate the Packages file from all .deb files in the pool,
# and force the filenames to be prefixed correctly.
$(DIST_DIR)/Packages: $(DEB_FILES)
	@mkdir -p $(DIST_DIR)
	dpkg-scanpackages $(POOL_DIR) /dev/null "pool/main" > $(DIST_DIR)/Packages

.PHONY: packages
packages: $(DIST_DIR)/Packages

# Compress the Packages file to create Packages.gz
.PHONY: packages.gz
packages.gz: $(DIST_DIR)/Packages
	gzip -9c $(DIST_DIR)/Packages > $(DIST_DIR)/Packages.gz

# Generate the Release file using apt-ftparchive
debian/Release: 
	@echo "Generating Release file..."
	apt-ftparchive release debian/dists/universal-apt > debian/Release

# Sign the Release file with GPG using your key (Nicholas Disalvio)
debian/Release.gpg: debian/Release
	cd debian && rm -f Release.gpg && \
		(echo "${KEY_PASSPHRASE}" | gpg --pinentry-mode loopback --passphrase-fd 0 -abs -o Release.gpg --local-user "Nicholas Disalvio" Release)

.PHONY: release
release: debian/Release.debian/Release.gpg

# Clean generated files
.PHONY: clean
clean:
	rm -f $(DIST_DIR)/Packages $(DIST_DIR)/Packages.gz debian/Release debian/Release.gpg
