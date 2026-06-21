dir="fvc2002"
rm -rf "$dir"
mkdir -p "$dir"
cd "$dir" || exit 1
wget http://bias.csr.unibo.it/FVC2002/Downloads/DB3_B.zip
unzip DB3_B.zip