class Aznuke < Formula
  desc "A powerful CLI tool for scanning and cleaning up Azure resources"
  homepage "https://github.com/sojay/azure-nuke"
  url "https://github.com/sojay/azure-nuke/archive/v0.1.8.tar.gz"
  sha256 "dbd8fd029c720df808beb9cb05ee5ae8cb1648406d2bae82715382ee0283b799"
  license "MIT"

  depends_on "python@3.11"

  def install
    venv_root = libexec/"venv"
    system "python3.11", "-m", "venv", venv_root
    
    system venv_root/"bin/pip", "install", "azure-identity>=1.10.0"
    system venv_root/"bin/pip", "install", "azure-mgmt-resource>=22.0.0"
    system venv_root/"bin/pip", "install", "azure-mgmt-subscription>=3.1.1"
    system venv_root/"bin/pip", "install", "azure-mgmt-compute>=27.0.0"
    system venv_root/"bin/pip", "install", "azure-mgmt-network>=22.0.0"
    system venv_root/"bin/pip", "install", "azure-mgmt-storage>=20.0.0"
    system venv_root/"bin/pip", "install", "azure-mgmt-keyvault>=10.0.0"
    system venv_root/"bin/pip", "install", "azure-mgmt-monitor>=5.0.0"
    system venv_root/"bin/pip", "install", "pyyaml>=6.0"
    system venv_root/"bin/pip", "install", "colorama==0.4.6"
    system venv_root/"bin/pip", "install", "pyfiglet==0.8.post1"
    system venv_root/"bin/pip", "install", "tqdm==4.66.1"
    
    libexec.install Dir["*"]
    (libexec/"aznuke/_version.py").write "version = '0.1.8'\n"
    
    (bin/"aznuke").write <<~EOS
      #!/usr/bin/env bash
      export PYTHONPATH="#{libexec}:$PYTHONPATH"
      exec "#{venv_root}/bin/python" -c "from aznuke import main; main()" "$@"
    EOS
  end

  test do
    system "#{bin}/aznuke", "--version"
  end
end 