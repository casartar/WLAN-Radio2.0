const char MAIN_page[] PROGMEM = R"=====(
<!DOCTYPE html>
<html>
  <style>
  body {
    text-align:center;
    font-family: helvetica;
  }
  </style>
  <head>
    <title>
      Webradio
    </title>
  <head>
  <body>
    <h1>Webradio WLAN-Einstellung</h1>
    *mark1begin*
    <h3>WLAN-Einstellungen</h3>
    <form method="POST">
      <p>
        <h4>WLAN-Name (SSID):</h4>
        <input type="text" name="ssid" value="*ssid*">
      </p>
      <p>
        <h4>WLAN-Passwort:</h4>
        <input type="password" name="password" value="*password*">
      </p>
      <!--<p>
        <h4>Zeitserver (NTP):</h4>
        Falls nicht klar ist, was das ist,<br/>dann sollte es <b>at.pool.ntp.org</b> bleiben.<br/>
        <input type="text" name="ntpserver" value="*ntpserver*">
      </p>-->
      <input type="submit" value="speichern">
    </form>
    *mark1end*
    <p>
      *feedback*
    </p>
  </body>
</html>
)=====";
