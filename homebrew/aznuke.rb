class Aznuke < Formula
  desc "A powerful CLI tool for scanning and cleaning up Azure resources"
  homepage "https://github.com/sojay/azure-nuke"
  url "https://github.com/sojay/azure-nuke/archive/v0.1.5.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"

  depends_on "python@3.11"

  def install
    venv = virtualenv_create(libexec, "python3.11")
    venv.pip_install buildpath
    
    # Create wrapper script
    (bin/"aznuke").write <<~EOS
      #!/usr/bin/env bash
      exec "#{libexec}/bin/python" -m aznuke "$@"
    EOS
  end

  test do
    system "#{bin}/aznuke", "--version"
  end
end 