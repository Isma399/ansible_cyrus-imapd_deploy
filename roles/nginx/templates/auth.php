<?php
/*
NGINX sends headers as
Auth-User: somuser
Auth-Pass: somepass
On my php app server these are seen as
HTTP_AUTH_USER and HTTP_AUTH_PASS
*/
define ("LDAPSERVER", "{{ ldap_server_vip }}");
if (!isset($_SERVER["HTTP_AUTH_USER"] ) || !isset($_SERVER["HTTP_AUTH_PASS"] )){
  fail();
}

$username=$_SERVER["HTTP_AUTH_USER"] ;
$password=$_SERVER["HTTP_AUTH_PASS"] ;
$protocol=$_SERVER["HTTP_AUTH_PROTOCOL"] ;

// default backend port
$backend_port=110;

if ($protocol=="imap") {
  $backend_port=143;
}
// NGINX likes ip address so if your
// application gives back hostname, convert it to ip address here
$backend_ip["{{ legacy_imap }}"] ="{{ legacy_imap_ip}}";
$backend_ip["{{ new_imap }}"] ="{{ new_imap_ip }}";

// Authenticate the user or fail
//if (!authuser($username,$password)){
//  fail();
//  exit;
//}
// Get the server for this user if we have reached so far
$userserver=getmailserver($username);

// Get the ip address of the server
// We are assuming that you backend returns hostname
// We try to get the ip else return what we got back
$server_ip=(isset($backend_ip[$userserver]))?$backend_ip[$userserver] :$userserver;

// Pass!
pass($server_ip, $backend_port);
//END

function authuser($username,$password){
  // password characters encoded by nginx:
  // " " 0x20h (SPACE)
  // "%" 0x25h
  // see nginx source: src/core/ngx_string.c:ngx_escape_uri(...)
  $password = str_replace('%20',' ', $password);
  $password = str_replace('%25','%', $password);
  // put your logic here to authen the user to any backend
  // you want (datbase, ldap, etc)
  $auth_user="uid=".$username.",ou=people,dc=univ-brest,dc=fr";
  //Check to see if LDAP module is loaded.
  if (extension_loaded('ldap')) {
    if($connect=@ldap_connect(LDAPSERVER)){
       ldap_set_option($connect, LDAP_OPT_PROTOCOL_VERSION, 3);
      //echo "connection ($ldap_server): ";
      if($bind=@ldap_bind($connect, $auth_user, $password)){
        //  echo "true";
        @ldap_close($connect);
        return true;
      } else {
        // echo "send error message - password incorrect";
        @ldap_close($connect);
        return false;
      }
    } else {
      //echo "send message - could not connect to domain";
      @ldap_close($connect);
      return false;
    }
}
//echo "send message - ldap module not loaded";
@ldap_close($connect);
return(false);
}

function getmailserver($username){
  // put the logic here to get the mailserver
  // backend for the user. You can get this from
  // some database or ldap etc
  $filter = "(uid=$username)";
  if($connect=@ldap_connect(LDAPSERVER)){
    $search = ldap_search($connect, "ou=people,dc=univ-brest,dc=fr", $filter);
    $info = ldap_get_entries($connect, $search);
    $mailserver = $info[0]["mailhost"][0];
    @ldap_close($connect);
    return $mailserver;
  } else {
    //echo "send message - could not connect to domain";
    @ldap_close($connect);
    return false;
  }
}

function fail(){
  header("Auth-Status: Invalid login or password");
  exit;
}

function pass($server,$port){
  header("Auth-Status: OK");
  header("Auth-Server: $server");
  header("Auth-Port: $port");
  exit;
}

