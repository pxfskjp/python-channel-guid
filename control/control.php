<?php

switch ($_GET["action"]) {
    case "test":
        echo exec('whoami');
        break;
    case "start":
        shell_exec("bash ../server/start-server.sh 2>&1");
        echo "done";
        break;
    case "stop":
        echo shell_exec("bash ../server/stop-server.sh 2>&1");
        echo "done";
        break;
    case "update":
        echo shell_exec("bash ../server/do_scrape.sh 2>&1");
        echo "done";
        break;
    default:
        ;
}

?>