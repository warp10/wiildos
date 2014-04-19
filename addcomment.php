<?php
/*
 * WiildOS Packages Health Status Report Generator
 *
 * Copyright © 2014 Mattia Rizzolo <mattia@mapreri.org>
 *
 * This work is free. You can redistribute it and/or modify it under the
 * terms of the Do What The Fuck You Want To Public License, Version 2,
 * as published by Sam Hocevar. The full text of the license is available at:
 * http://www.wtfpl.net/txt/copying/
 *
 */

    $COMMENTS_FILE ="/home/groups/ubuntu-dev/htdocs/wiildos/comments.json";
    $pyscript = "/srv/home/users/mapreri-guest/wiildos/wiildos.py";

    $package = $_GET['package'];
    $comment = addslashes($_GET['comment']);
    $the_comment = str_replace( "\n", " ", $comment );
    $command = "python ".$pyscript;

    $json = json_decode(file_get_contents($COMMENTS_FILE), true);

    $json[$package] = $the_comment;

    file_put_contents($COMMENTS_FILE, json_encode($json, JSON_PRETTY_PRINT));

    system($command);
    header('Location: '.$_SERVER['HTTP_REFERER']);

?>
