class Aznuke < Formula
  desc "A powerful CLI tool for scanning and cleaning up Azure resources"
  homepage "https://github.com/sojay/azure-nuke"
  url "https://github.com/sojay/azure-nuke/archive/v0.1.7.tar.gz"
  sha256 "96171ad6a0218f74f8829a3bcdb36dfdd2a4fce45e1f0b0203a774876ec71d41"
  license "MIT"

  depends_on "python@3.11"

  def install
    venv = virtualenv_create(libexec, "python3.11")
    
    # Install the package and its dependencies
    venv.pip_install_and_link buildpath
    
    # Alternatively, install dependencies first then the package
    # venv.pip_install "colorama==0.4.6", "pyfiglet==0.8.post1", "tqdm==4.66.1"
    # venv.pip_install buildpath
  end

  test do
    system "#{bin}/aznuke", "--version"
  end
end 