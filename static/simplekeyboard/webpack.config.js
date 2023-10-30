const path = require("path");
const webpack = require("webpack");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  mode: "production",
  entry: "./src/lib/index.modern.ts",
  target: ["web", "es2020"],
  output: {
    filename: "index.modern.js", // Changed filename for clarity
    path: path.resolve(__dirname, "build"),
    globalObject: "this",
    hashFunction: "xxhash64",
    library: {
      name: "SimpleKeyboard", // Specify the library name here
      type: "var", // Adjusted to "var"
    },
  },
  // Removed experiments section
  devtool: "source-map",
  optimization: {
    minimize: false,
    minimizer: [new TerserPlugin({ extractComments: false })],
  },
  module: {
    rules: [
      {
        test: /\.m?(j|t)s$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [["@babel/env"]],
            plugins: [
              ["@babel/plugin-proposal-class-properties"],
              ["@babel/plugin-transform-typescript"],
            ],
          },
        },
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: path.resolve("scripts/loaderMock.js"),
      },
    ],
  },
  resolve: {
    extensions: [".ts", ".js", ".json"],
  },
};
