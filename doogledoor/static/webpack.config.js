const webpack = require("webpack");
const config = {
  mode: "production",
  entry: __dirname + "/scripts/index.tsx",
  devtool: "eval-cheap-module-source-map",
  output: {
    path: __dirname + "/dist",
    filename: "bundle.js",
  },
  resolve: {
    extensions: [".ts", ".tsx", ".js", ".jsx"],
    modules: [__dirname + "/node_modules"],
  },
  module: {
    rules: [
      {
        test: /.tsx?$/,
        exclude: /node_modules/,
        use: "ts-loader",
      },
    ],
  },
};
module.exports = config;
