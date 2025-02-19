# Define directories
POOL_DIR := debian/pool/main
DIST_DIR := debian/dists/universal-apt/main/binary-amd64
DISTS := debian/dists/universal-apt

# Default target: generate Packages, Packages.gz, and Release files
all: packages packages.gz release

# Generate Packages file by running inside the debian folder
$(DIST_DIR)/Packages:
	@cd debian && mkdir -p dists/universal-apt/main/binary-amd64 && \
	    dpkg-scanpackages --multiversion pool/main /dev/null "" > dists/universal-apt/main/binary-amd64/Packages

.PHONY: packages
packages: $(DIST_DIR)/Packages

.PHONY: packages.gz
packages.gz: $(DIST_DIR)/Packages
	@cd debian && gzip -9c dists/universal-apt/main/binary-amd64/Packages > dists/universal-apt/main/binary-amd64/Packages.gz

# Generate the Release file using the configuration file.
$(DISTS)/Release:
	@echo "Generating Release file..."
	apt-ftparchive -c=apt-ftparchive.conf release $(DISTS) > $(DISTS)/Release

# Sign the Release file with GPG using your key.
$(DISTS)/Release.gpg: $(DISTS)/Release
	cd $(DISTS) && rm -f Release.gpg && \
		(echo "${KEY_PASSPHRASE}" | gpg --pinentry-mode loopback --passphrase-fd 0 -abs -o Release.gpg --local-user "YOUR_KEY_ID_OR_NAME" Release)

.PHONY: release
release: $(DISTS)/Release.gpg

.PHONY: clean
clean:
	rm -f $(DIST_DIR)/Packages $(DIST_DIR)/Packages.gz $(DISTS)/Release $(DISTS)/Release.gpg
