class Aznuke < Formula
  include Language::Python::Virtualenv

  desc "A powerful CLI tool for scanning and cleaning up Azure resources"
  homepage "https://github.com/sojay/azure-nuke"
  url "https://github.com/sojay/azure-nuke/archive/v0.1.7.tar.gz"
  sha256 "96171ad6a0218f74f8829a3bcdb36dfdd2a4fce45e1f0b0203a774876ec71d41"
  license "MIT"

  depends_on "python@3.11"

  def install
    # Create version file since setuptools_scm can't determine version from tarball
    (buildpath/"aznuke/_version.py").write "version = '0.1.7'\n"
    
    # Use modern Homebrew virtualenv syntax
    virtualenv_install_with_resources using: "python@3.11"
  end

  test do
    system "#{bin}/aznuke", "--version"
  end
end 