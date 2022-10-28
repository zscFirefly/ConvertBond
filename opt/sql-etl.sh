declare -r CURR_DIR=$(cd `dirname $0`;pwd)
declare -r DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" 


JOB_NAME=`basename $0 .sh`

if [ $# -lt 1 ];then
	echo "Please enter the parameter and retry again"
	exit;
fi

python3 $DIR/sql-etl.py --file "$1"