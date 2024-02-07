sudo apt-get update -y && sudo apt-get -y install curl tar ca-certificates
curl -o apphub-linux-amd64.tar.gz https://assets.coreservice.io/public/package/60/app-market-gaga-pro/1.0.4/app-market-gaga-pro-1_0_4.tar.gz && tar -zxf apphub-linux-amd64.tar.gz && rm -f apphub-linux-amd64.tar.gz && cd ./apphub-linux-amd64 && sudo ./apphub service install
sudo ./apphub service start
sleep 20
sudo ./apps/gaganode/gaganode config set --token=khfcwpvgezcltibd4e97cb91f823baf3
./apphub restart