const express = require("express");
const app = express();
const port = 3000;
const public = __dirname + "/public/";

var output_authorize_py;
var output_authenticate_py;
var python;

app.use(express.static(public));

app.listen(port, () => {
  console.log("server running on port ", port);
});

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/public/index.html");
});

app.get("/authorizethelp/", (req, res) => {
  const { spawn } = require("child_process");
  python = spawn("python3", ["thelp_authorize.py"]);
  python.stdout.on("data", (data) => {
    output_authorize_py = data.toString();

    //output_authorize_py=output_authorize_py.replace(/\r?\n|\r/g,"");
    output_authorize_py = JSON.parse(output_authorize_py);
    console.log(output_authorize_py);
  });
  python.on("close", (code) => {
    console.log(`child process closing all stdio with ${code}`);
    res.redirect(encodeURI(output_authorize_py.authorize_url));
  });
});

app.get("/authenticate/", (req, res) => {
  const { spawn } = require("child_process");
  python = spawn("python3", [
    "thelp_authenticate.py",
    output_authorize_py.temp_access_key,
    output_authorize_py.temp_access_secret,
    req.query.oauth_verifier,
  ]);
  python.stdout.on("data", (data) => {
    output_authenticate_py = data.toString();
    output_authenticate_py = JSON.parse(output_authenticate_py);
    console.log(output_authenticate_py);
  });
  python.on("close", (code) => {
    console.log(`child process closing all the stdio with ${code}`);
    res.redirect("/bot");
  });
});

app.get("/bot", (req, res) => {
  if (req.query != {}) {
    if (req.query.stop == "true") {
      python.kill();
      res.redirect("/");
      return;
    }
  }
  const { spawn } = require("child_process");
  python = spawn("python3", [
    "thelp_bot.py",
    output_authenticate_py.access_key,
    output_authenticate_py.access_secret,
  ]);
  var bot_data;
  python.stdout.on("data", (data) => {
    bot_data = data.toString();
    console.log(bot_data);
  });
  python.on("close", (code) => {
    console.log("test");
    console.log(`child process closing all the stdio with ${code}`);
  });
  res.sendFile(public + "bot.html");
});
