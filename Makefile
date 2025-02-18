# Define directories
POOL_DIR := debian/pool/main
DIST_DIR := debian/dists/universal-apt/main/binary-amd64
DISTS := debian/dists/universal-apt

# Default target: generate Packages, Packages.gz, and Release files
all: packages packages.gz release

# Generate Packages file with correct prefix
$(DIST_DIR)/Packages: $(wildcard $(POOL_DIR)/*.deb)
	@mkdir -p $(DIST_DIR)
	dpkg-scanpackages $(POOL_DIR) /dev/null "pool/main" > $(DIST_DIR)/Packages

.PHONY: packages
packages: $(DIST_DIR)/Packages

.PHONY: packages.gz
packages.gz: $(DIST_DIR)/Packages
	gzip -9c $(DIST_DIR)/Packages > $(DIST_DIR)/Packages.gz

# Generate the Release file in the correct directory
$(DISTS)/Release:
	@echo "Generating Release file..."
	apt-ftparchive release $(DISTS) > $(DISTS)/Release

# Sign the Release file with GPG using your key
$(DISTS)/Release.gpg: $(DISTS)/Release
	cd $(DISTS) && rm -f Release.gpg && \
		(echo "${KEY_PASSPHRASE}" | gpg --pinentry-mode loopback --passphrase-fd 0 -abs -o Release.gpg --local-user "Nicholas Disalvio" Release)

.PHONY: release
release: $(DISTS)/Release.gpg

.PHONY: clean
clean:
	rm -f $(DIST_DIR)/Packages $(DIST_DIR)/Packages.gz $(DISTS)/Release $(DISTS)/Release.gpg