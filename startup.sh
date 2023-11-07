#! 一键启动
echo '在运行前，请正确安装 python 和node 18'
echo 'sudo service nvargus-daemon restart'
python main.py &
cd platform && npm run dev