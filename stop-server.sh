echo $(pgrep python2.6)
echo $(kill -9 "$(pgrep python2.6)")
exit

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
#kill -SIGINT  $(cat ./running.pid)
# killall -SIGTERM python2.6

KillChilds() {
        local pid="${1}"
        local self="${2:-false}"

        if children="$(pgrep -P "$pid")"; then
                for child in $children; do
                        KillChilds "$child" true
                done
        fi

        if [ "$self" == true ]; then
                kill -s SIGTERM "$pid" || (sleep 10 && kill -9 "$pid" &)
        fi
}

echo $(pgrep python2.6)
KillChilds "$(pgrep python2.6)" true