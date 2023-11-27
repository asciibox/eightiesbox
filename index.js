const fs = require("fs");
const { JSDOM } = require("jsdom");
const { exec } = require("child_process");

// Replace with your HTML file path
const htmlFilePath = "templates/index.html";

// Function to read HTML and find script tags
function extractScriptsFromHTML(filePath) {
  const html = fs.readFileSync(filePath, "utf8");
  const dom = new JSDOM(html);
  const scripts = dom.window.document.querySelectorAll(
    'script[src^="./static/bassoontracker"]'
  );
  return Array.from(scripts).map((script) => script.src);
}

// Function to compile scripts using Closure Compiler
function compileScripts(scripts, outputPath) {
  const command = `npx google-closure-compiler --js=${scripts.join(
    " "
  )} --compilation_level SIMPLE --js_output_file ${outputPath}`;
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Compilation error: ${error}`);
      return;
    }
    if (stderr) {
      console.error(`Compilation stderr: ${stderr}`);
      return;
    }
    console.log(`Compilation stdout: ${stdout}`);
    console.log("Compilation complete. Output saved to " + outputPath);
  });
}

// Main process
const scriptSources = extractScriptsFromHTML(htmlFilePath);
const outputFilePath = "static/bundle.js";
compileScripts(scriptSources, outputFilePath);
